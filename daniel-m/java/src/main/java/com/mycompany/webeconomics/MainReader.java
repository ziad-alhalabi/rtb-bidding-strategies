/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.webeconomics;

import com.mycompany.webeconomics.models.Advertiser;
import com.mycompany.webeconomics.models.Impression;
import com.opencsv.CSVReader;
import java.io.File;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.CategoryLabelPositions;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.AbstractRenderer;
import org.jfree.chart.renderer.category.BarRenderer;
import org.jfree.chart.renderer.category.LineAndShapeRenderer;
import org.jfree.chart.renderer.category.StackedBarRenderer;
import org.jfree.chart.renderer.category.StandardBarPainter;
import org.jfree.data.category.DefaultCategoryDataset;

/**
 */
public class MainReader {
    
    private static List<Impression> impressions = new ArrayList<>();
    private static List<Advertiser> advertisers = new ArrayList<>();
    private static int[] advertisersToGraph = new int[]{1458,2997};//,3358};
    private static int singleAdvertiserToGraph = 2997;
//    Advertiser IDs - <rank by clicks>
//    1458 - 1
//    3386 - 2    
//    3427 - 3
//    2997 - 4
//    3358 - 5    
//    3476 - 6
//    2821 - 7
//    2259 - 8
//    2261 - 9

    public static void main(String[] args) throws IOException{
        process("we_data/train.csv");
        doStats();
    }
    
    private static void process(String filePath) throws IOException{
        Reader reader = Files.newBufferedReader(Paths.get(filePath));
        CSVReader csvReader = new CSVReader(reader);
        // test for coursework
        // Reading Records One by One in a String array
        String[] entry;
        int i = 0;
        HashSet<Integer> uniqueAdvertiserIds = new HashSet<>();
        while ((entry = csvReader.readNext()) != null) {
            if(i == 0){ i = 1; continue; }
            Impression imp = new Impression(entry);
            impressions.add(imp);
            uniqueAdvertiserIds.add(imp.getAdvertiser());
            i++;
        }
        for(Integer uniqueAdvertiserId : uniqueAdvertiserIds){
            advertisers.add(new Advertiser(uniqueAdvertiserId));
        }
        
        for(Impression impression : impressions){
            int advertiserId = impression.getAdvertiser();
            for(Advertiser advertiser : advertisers){
                if(advertiser.getId() == advertiserId) { advertiser.addImpression(impression); break; }
            }
        }
    }

    // analyse impressions here
    private static void doStats() throws IOException {
        makeTable();
        createCTRDistributions();
        createEcpcDistributions();
        createAvgBidPriceDistributions();
    }      

    private static boolean isWantedAdvertiser(int id){
        for(Integer advId : advertisersToGraph){
            if(advId == id) return true;
        }
        return false;
    }
    
    private static boolean isWantedSingleAdvertiser(int id){
        return id == singleAdvertiserToGraph;
    }    
     

    
    private static void createCTRDistributions() throws IOException{
        //xlabel, title, filename,
        String[] weekly_meta = new String[]{"Day of the week", "Weekly CTR distribution", "weeklyCTR_"};
        String[] hourly_meta = new String[]{"Hour of the day", "Hourly CTR distribution", "hourlyCTR_"};
        String[] browser_meta = new String[]{"Browser", "CTR distribution by browser", "browserCTR_"};
        String[] os_meta = new String[]{"Operating System", "CTR distribution by OS", "osCTR_"};
        String[] regional_meta = new String[]{"Region", "Regional CTR distribution", "regionalCTR_"};
        String yLabel = "CTR (%)";
        
        
        DefaultCategoryDataset weekly = new DefaultCategoryDataset();
        DefaultCategoryDataset hourly = new DefaultCategoryDataset();
        DefaultCategoryDataset brwsr = new DefaultCategoryDataset();
        DefaultCategoryDataset os = new DefaultCategoryDataset();
        DefaultCategoryDataset regional = new DefaultCategoryDataset();
        
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                double[] weeklyClickCount = new double[7]; // 7 days, 0 - 6
                double[] hourlyClickCount = new double[24];
                double[] regionalClickCount = new double[395 + 1];
                double[] weeklyImpCount = new double[7];
                double[] hourlyImpCount = new double[24];
                double[] regionalImpCount = new double[395+1];
                HashMap<String,Integer> browserClicks = new HashMap<>();
                HashMap<String,Integer> browserImps = new HashMap<>();
                HashMap<String,Integer> osClicks = new HashMap<>();
                HashMap<String,Integer> osImps = new HashMap<>();                
                for(Impression imp : advertiser.getImpressions()){
                    int day = imp.getTime().getDay();
                    int hour = imp.getTime().getHour();
                    int region = imp.getUser().getRegion();
                    int click = imp.isIsClicked() ? 1 : 0;
                    
                    weeklyClickCount[day] += click;
                    hourlyClickCount[hour] += click;
                    regionalClickCount[region] += click;
                    
                    weeklyImpCount[day] += 1;
                    hourlyImpCount[hour] += 1;
                    regionalImpCount[region] += 1;
                    
                    String[] userAgent = imp.getUser().getUserAgent().split("_");
                    browserClicks.merge(userAgent[1],click,Integer::sum);
                    browserImps.merge(userAgent[1],1,Integer::sum);
                    
                    osClicks.merge(userAgent[0],click,Integer::sum);
                    osImps.merge(userAgent[0],1,Integer::sum);                    
                }
                
                createDatasetFromClicksAndCosts(weeklyImpCount,weeklyClickCount,weekly,advertiser.getId(),true);
                createDatasetFromClicksAndCosts(hourlyImpCount,hourlyClickCount,hourly,advertiser.getId(),true);
                createDatasetFromClicksAndCosts(regionalImpCount,regionalClickCount,regional,advertiser.getId(),true);
                
                for(String browser : browserImps.keySet()){
                    double imps = (double) browserImps.get(browser);
                    if(imps <= 0) continue;
                    double clicks = ((double) browserClicks.get(browser));
                    double cpc = (clicks/imps); // avg bid price = total bid cost / total bids (won impressions)
                    brwsr.addValue(cpc, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
                
                for(String opsys : osImps.keySet()){
                    double imps = (double) osImps.get(opsys);
                    if(imps <= 0) continue;
                    double clicks = ((double) osClicks.get(opsys));
                    double cpc = (clicks/imps); // avg bid price = total bid cost / total bids (won impressions)
                    os.addValue(cpc, "Advertiser " + String.valueOf(advertiser.getId()), opsys);
                }                
            }
        }
        createChart(weekly_meta[0],yLabel,weekly,weekly_meta[1],weekly_meta[2],new StackedBarRenderer());
        createChart(hourly_meta[0],yLabel,hourly,hourly_meta[1],hourly_meta[2],new StackedBarRenderer());
        createChart(regional_meta[0],yLabel,regional,regional_meta[1],regional_meta[2],new StackedBarRenderer());
        createChart(browser_meta[0],yLabel,brwsr,browser_meta[1],browser_meta[2],new StackedBarRenderer());
        createChart(os_meta[0],yLabel,os,os_meta[1],os_meta[2],new StackedBarRenderer());
    }      
    
    private static void createAvgBidPriceDistributions() throws IOException{
        //xlabel, title, filename,
        String[] weekly_meta = new String[]{"Day of the week", "Weekly bid-price movements", "weeklyPRICE_"};
        String[] hourly_meta = new String[]{"Hour of the day", "Hourly bid-price movements", "hourlyPRICE_"};
        String[] browser_meta = new String[]{"Browser", "Bid-price movements per browser", "browserPRICE_"};
        String[] regional_meta = new String[]{"Region", "Regional bid-price movements", "regionalPRICE_"};
        String yLabel = "Average bid-price (CNY)";
        
        
        DefaultCategoryDataset weekly = new DefaultCategoryDataset();
        DefaultCategoryDataset hourly = new DefaultCategoryDataset();
        DefaultCategoryDataset brwsr = new DefaultCategoryDataset();
        DefaultCategoryDataset regional = new DefaultCategoryDataset();
        
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                double[] weeklyImpCount = new double[7]; // 7 days, 0 - 6
                double[] hourlyImpCount = new double[24];
                double[] regionalImpCount = new double[395 + 1];
                double[] weeklyBids = new double[7];
                double[] hourlyBids = new double[24];
                double[] regionalBids = new double[395+1];
                HashMap<String,Integer> browserImps = new HashMap<>();
                HashMap<String,Double> browserCost = new HashMap<>();
                for(Impression imp : advertiser.getImpressions()){
                    int day = imp.getTime().getDay();
                    int hour = imp.getTime().getHour();
                    int region = imp.getUser().getRegion();
                    double price = imp.getBidPrice() / 1000.0 / 100.0; // /1000 to convert to single price instead of price per mille (Cost Per Mille), /100 to convert the Fen to Yuan
                    
                    weeklyImpCount[day] += 1;
                    hourlyImpCount[hour] += 1;
                    regionalImpCount[region] += 1;
                    
                    String browser = imp.getUser().getUserAgent().split("_")[1];
                    browserImps.merge(browser,1,Integer::sum);
                    browserCost.merge(browser,price,Double::sum);
                    weeklyBids[day] += price;
                    hourlyBids[hour] += price;
                    regionalBids[region] += price;
                }
                
                createDatasetFromClicksAndCosts(weeklyImpCount,weeklyBids,weekly,advertiser.getId(),false);
                createDatasetFromClicksAndCosts(hourlyImpCount,hourlyBids,hourly,advertiser.getId(),false);
                createDatasetFromClicksAndCosts(regionalImpCount,regionalBids,regional,advertiser.getId(),false);
                
                for(String browser : browserImps.keySet()){
                    double imps = (double) browserImps.get(browser);
                    if(imps <= 0) continue;
                    double cost = ((double) browserCost.get(browser));
                    double cpc = (cost/imps); // avg bid price = total bid cost / total bids (won impressions)
                    brwsr.addValue(cpc, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
            }
        }
        createChart(weekly_meta[0],yLabel,weekly,weekly_meta[1],weekly_meta[2],new LineAndShapeRenderer());
        createChart(hourly_meta[0],yLabel,hourly,hourly_meta[1],hourly_meta[2],new LineAndShapeRenderer());
        createChart(regional_meta[0],yLabel,regional,regional_meta[1],regional_meta[2],new LineAndShapeRenderer());
        createChart(browser_meta[0],yLabel,brwsr,browser_meta[1],browser_meta[2],new LineAndShapeRenderer());
    }     

    
    private static void createEcpcDistributions() throws IOException{
        //xlabel, title, filename,
        String[] weekly_meta = new String[]{"Day of the week", "Weekly eCPC distribution", "weeklyECPC_"};
        String[] hourly_meta = new String[]{"Hour of the day", "Hourly eCPC distribution", "hourlyECPC_"};
        String[] browser_meta = new String[]{"Browser", "eCPC per browser", "browserECPC"};
        String[] regional_meta = new String[]{"Region", "Regional eCPC distribution", "regionalECPC"};
        String yLabel = "eCPC (CNY/Click)";
        
        
        DefaultCategoryDataset weekly = new DefaultCategoryDataset();
        DefaultCategoryDataset hourly = new DefaultCategoryDataset();
        DefaultCategoryDataset brwsr = new DefaultCategoryDataset();
        DefaultCategoryDataset regional = new DefaultCategoryDataset();
        
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                double[] weeklyClickCount = new double[7]; // 7 days, 0 - 6
                double[] hourlyClickCount = new double[24];
                double[] regionalClickCount = new double[395 + 1];
                double[] weeklyCost = new double[7];
                double[] hourlyCost = new double[24];
                double[] regionalCost = new double[395+1];
                HashMap<String,Integer> browserClicks = new HashMap<>();
                HashMap<String,Double> browserCost = new HashMap<>();
                for(Impression imp : advertiser.getImpressions()){
                    int day = imp.getTime().getDay();
                    int hour = imp.getTime().getHour();
                    int region = imp.getUser().getRegion();
                    if(imp.isIsClicked()){
                        weeklyClickCount[imp.getTime().getDay()] += 1;
                        hourlyClickCount[imp.getTime().getHour()] += 1;
                        regionalClickCount[imp.getUser().getRegion()] += 1;
                    }
                    String browser = imp.getUser().getUserAgent().split("_")[1];
                    browserClicks.merge(browser,((imp.isIsClicked()) ? 1 : 0),Integer::sum);
                    
                    double cost = imp.getPayPrice() / 1000.0 / 100.0; // e.g. payprice = 35, that's 35 fen per thousand imps, so it's actually 0.035 fen, which is 0.00035 CNY
                    weeklyCost[day] += cost;
                    hourlyCost[hour] += cost;
                    regionalCost[region] += cost;
                    browserCost.merge(browser,cost,Double::sum);
                }
                
                createDatasetFromClicksAndCosts(weeklyClickCount,weeklyCost,weekly,advertiser.getId(),false);
                createDatasetFromClicksAndCosts(hourlyClickCount,hourlyCost,hourly,advertiser.getId(),false);
                createDatasetFromClicksAndCosts(regionalClickCount,regionalCost,regional,advertiser.getId(),false);
                
                for(String browser : browserClicks.keySet()){
                    double clicks = (double) browserClicks.get(browser);
                    if(clicks <= 0) continue;
                    double cost = ((double) browserCost.get(browser));
                    double cpc = (cost/clicks); // avg bid price = total bid cost / total bids (won impressions)
                    brwsr.addValue(cpc, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
            }
        }
        createChart(weekly_meta[0],yLabel,weekly,weekly_meta[1],weekly_meta[2],new BarRenderer());
        createChart(hourly_meta[0],yLabel,hourly,hourly_meta[1],hourly_meta[2],new BarRenderer());
        createChart(regional_meta[0],yLabel,regional,regional_meta[1],regional_meta[2],new BarRenderer());
        createChart(browser_meta[0],yLabel,brwsr,browser_meta[1],browser_meta[2],new BarRenderer());
    }       
    
    private static void createDatasetFromClicksAndCosts(double[] denominator, double[] numerator, DefaultCategoryDataset dataset, int advertiserId, boolean isCtr){
        for(int i = 0; i < denominator.length; i++){
            String thing = String.valueOf(i+1); // +1 is only applicable to hourly or weekly analysis
            if(denominator[i] <= 0) continue;
            double value = numerator[i]/denominator[i]; // value = ecpc if count = clicks, value = avgBid/PayPrice if count = impressions
            if(isCtr) value = value * 100; // to turn it into percentage
            dataset.addValue(value, "Advertiser " + String.valueOf(advertiserId), thing);
        }
    }    
    
    
    private static void createChart(String xLabel, String yLabel, DefaultCategoryDataset dataset, String title, String fileName, AbstractRenderer renderer) throws IOException{
        CategoryAxis ca = new CategoryAxis(xLabel);
        ca.setCategoryLabelPositions(CategoryLabelPositions.UP_45);  
        ca.setCategoryMargin(0.01);
        CategoryPlot plot = null;
        if(renderer instanceof BarRenderer || renderer instanceof StackedBarRenderer){
            BarRenderer br = (BarRenderer) renderer;
            br.setBarPainter(new StandardBarPainter());
            br.setDrawBarOutline(false);
            br.setShadowVisible(false);
            br.setItemMargin(0.003);
            plot = new CategoryPlot(dataset,ca,new NumberAxis(yLabel),br);
        }else if(renderer instanceof LineAndShapeRenderer){
            LineAndShapeRenderer lasr = new LineAndShapeRenderer();
            lasr.setItemMargin(0.003);
            plot = new CategoryPlot(dataset,ca,new NumberAxis(yLabel),lasr);            
        }
        if(plot == null) return;
        plot.setOrientation(PlotOrientation.VERTICAL);
        makeChart(title,plot,fileName);
    }
    
    private static void makeChart(String title, CategoryPlot plot, String fileName) throws IOException{
        JFreeChart barChart = new JFreeChart( title,JFreeChart.DEFAULT_TITLE_FONT,plot,true);        
        int width = 640;
        int height = 480;
        File BarChart = new File(fileName + "distrib.jpeg"); 
        ChartUtils.saveChartAsJPEG(BarChart,barChart,width,height);    
    }
    
    private static void makeTable(){
        // insufficient data for 'bids, conversions, win ratio and conversion ratio', these are ommitted for the coursework dataset
        //String[] header = {"Advertiser | ", "Impressions | ", "Clicks | ", "Total Cost (CNY) | ", "CTR (%) | ", "CPM | ", "eCPC | ", "Avg. bid price | ", "Avg. pay price"};
        //System.out.format(createHeaderFormatString(header.length), header[0], header[1], header[2], header[3], header[4], header[5], header[6], header[7], header[8]);
        //System.out.println();
        System.out.println("Advertiser,Impressions,Clicks,Total Cost (CNY),CTR (%),CPM,eCPC,Avg. bid price,Avg. pay price");
        for(Advertiser advertiser : advertisers){
            int clickCount = 0;
            int impCount = advertiser.getImpressions().size();
            double cost = 0.0; // in Fen, not Yuan, 1 Yuan = 100 Fen
            double bid = 0.0;
            for(Impression impression : advertiser.getImpressions()){
            // note:
            // e.g. when payprice is 322 Chinese fen, it actually means the cost is 0.322 Chinese fen
            // this is because the data is based on CPM (Cost Per Mille / Cost Per Thousand)
            //
                if(impression.isIsClicked()) clickCount += 1;
                cost += impression.getPayPrice() / 1000.0; // devide by 1000 to get actual payprice (in fen)
                bid += impression.getBidPrice() / 1000.0;
            }
            double avgBid = bid/(double)impCount;
            double avgPay = cost/(double)impCount;
            double cpm = (cost/(double)impCount)*1000; // multiply by 1000 to get cost per thousand impressions
            double ctr = ((double)clickCount/(double)impCount)*(double)100;
            double ecpc = (double)cost/(double)clickCount;
            //cost = cost / 100; // to turn into Yuan [edit: just leave it as Fen, that's how it is in the research paper as well]
            //System.out.format(createRowFormatString(header),
            System.out.println(
            /*0*/   advertiser.getId() + "," +
            /*1*/   impCount + "," +
            /*2*/   clickCount + "," + 
            /*3*/   formatTo(cost,2) + "," + 
            /*4*/   formatTo(ctr,3) + "," +
            /*5*/   formatTo(cpm,2) + "," +
            /*6*/   formatTo(ecpc,2) + "," +
            /*7*/   formatTo(avgBid,3) + "," +
            /*8*/   formatTo(avgPay,3)); // printed as CSV for importing into Excel
        }        
    } 
        /**
     * Format given double to number of decimal places specified by 'decimals'.
     * @param d double to format
     * @param decimals the number of decimal places to format d to
     * @return the formatted string
     */
    private static String formatTo(double d, int decimals){
        String decimalPlaces = "#.";
        for(int i = 0; i < decimals; i++) decimalPlaces += "#";
        return new DecimalFormat(decimalPlaces).format(d);
    }
}
