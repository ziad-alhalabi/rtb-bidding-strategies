/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.webeconomics;

import com.mycompany.webeconomics.models.Advertiser;
import com.mycompany.webeconomics.models.Impression;
import java.io.File;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.CategoryLabelPositions;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.BarRenderer;
import org.jfree.chart.renderer.category.StackedBarRenderer;
import org.jfree.chart.renderer.category.StandardBarPainter;
import org.jfree.data.category.DefaultCategoryDataset;

/**
 *
 * @author 
 */
public class OldStatsMakers {
    
    private static List<Impression> impressions = new ArrayList<>();
    private static List<Advertiser> advertisers = new ArrayList<>();
    private static int[] advertisersToGraph = new int[]{1458,3386,3427};
    private static int singleAdvertiserToGraph = 3358;    
    
    public static void main_old(){
        //makeTable();
//        createWeeklyCTRDistributionChart();
//        createBrowserCTRDistributionChart();
//        createBrowserBidPriceDistributionChart();
//        createBrowserExpenditureDistributionChart();
//        createHourlyExpenditureDistributionChart();
//        createHourlyCTRDistributionChart();
//        createRegionalCTRDistributionChart(true);
//        createRegionalCTRDistributionChart(false);
//        createRegionalClickDistributionChart(true);
//        createRegionalClickDistributionChart(false);
//        createHourlyClickDistributionChart(true);
//        createHourlyClickDistributionChart(false);
//        createClicksPerAdvertiserChart();    
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
    
    private static void createBrowserEcpcDistribution() throws IOException{
        String title = "CPC per browser";
        String xLabel = "Browser";
        String fileName = "browserECPC_";
        String yLabel = "CPC";
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                HashMap<String,Integer> browserClicks = new HashMap<>();
                HashMap<String,Double> browserCost = new HashMap<>();
                for(Impression imp : advertiser.getImpressions()){
                    int click = 0;
                    if(imp.isIsClicked()) click = 1;
                    String browser = imp.getUser().getUserAgent().split("_")[1];
                    browserClicks.merge(browser,click,Integer::sum);
                    browserCost.merge(browser,((imp.getPayPrice()/1000.0)/100.0),Double::sum);
                }
                
                for(String browser : browserClicks.keySet()){
                    double clicks = (double) browserClicks.get(browser);
                    double cost = ((double) browserCost.get(browser));
                    double cpc = (cost/clicks); // avg bid price = total bid cost / total bids (won impressions)
                    dataset.addValue(cpc, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new BarRenderer());
    }  

    private static void createWeeklyCTRDistributionChart() throws IOException{
        String title = "Weekly CTR distribution";
        String xLabel = "Weekday";
        String fileName = "weeklyCTR_";
        String yLabel = "CTR (%)";
        int maxCityRegionInt = 399 + 1;
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                int[] dailyClickCount = new int[maxCityRegionInt]; // 7 days, 0 - 6
                int[] dailyImpCount = new int[maxCityRegionInt];
                for(Impression imp : advertiser.getImpressions()){
                    if(imp.isIsClicked()){
                        dailyClickCount[imp.getTime().getDay()] += 1;
                    }
                    dailyImpCount[imp.getTime().getDay()] += 1;
                }
                
                for(int i = 0; i < dailyImpCount.length; i++){
                    if(dailyImpCount[i] == 0) continue;
                    double ctr = ((double)dailyClickCount[i]/(double)dailyImpCount[i])*(double)100;
                    String regionalCtr = String.valueOf(i+1);
                    dataset.addValue(ctr, "Advertiser " + String.valueOf(advertiser.getId()), regionalCtr);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }       
    
    private static void createBrowserCTRDistributionChart() throws IOException{
        String title = "CTR distribution by browser";
        String xLabel = "Browser";
        String yLabel = "CTR (%)";
        String fileName = "browserCTR_";
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                HashMap<String,Integer> browserClicks = new HashMap<>();
                HashMap<String,Integer> browserImps = new HashMap<>();
                for(Impression imp : advertiser.getImpressions()){
                    int click = 0;
                    if(imp.isIsClicked()) click = 1;
                    String browser = imp.getUser().getUserAgent().split("_")[1];
                    browserClicks.merge(browser,click,Integer::sum);
                    browserImps.merge(browser,1,Integer::sum);
                }
                
                for(String browser : browserClicks.keySet()){
                    double ctr = ((double)browserClicks.get(browser) / (double)browserImps.get(browser)) * 100d; // avg bid price = total bid cost / total bids (won impressions)
                    dataset.addValue(ctr, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }      
    
    private static void createBrowserBidPriceDistributionChart() throws IOException{
        String title = "Bid price distribution by browser";
        String xLabel = "Browser";
        String yLabel = "Average bid-price (CNY per mille)";
        String fileName = "browserBID_";
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                HashMap<String,Double> browserBids = new HashMap<>();
                HashMap<String,Integer> browserImps = new HashMap<>();
                for(Impression imp : advertiser.getImpressions()){
                    double pp = ((double)imp.getBidPrice()/ 100d);
                    String browser = imp.getUser().getUserAgent().split("_")[1];
                    browserBids.merge(browser,pp,Double::sum);
                    browserImps.merge(browser,1,Integer::sum);
                }
                
                for(String browser : browserBids.keySet()){
                    double bid = browserBids.get(browser) / (double)browserImps.get(browser); // avg bid price = total bid cost / total bids (won impressions)
                    dataset.addValue(bid, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }         
    
    private static void createBrowserExpenditureDistributionChart() throws IOException{
        String title = "Expenditure distribution by Operating System";
        String xLabel = "Browser";
        String yLabel = "Expenditure (CNY)";
        String fileName = "browserCOST_";
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                HashMap<String,Double> osExp = new HashMap<>();
                for(Impression imp : advertiser.getImpressions()){
                    double cost = (((double)imp.getPayPrice()/1000d)/100d); // bid price ~ 200 fen, but this is perr 1000, so real bid price is 0.200 fen, which is 0.2/100 CNY (Yuan)
                    String browser = imp.getUser().getUserAgent().split("_")[1];
                    osExp.merge(browser,cost,Double::sum);
                }
                
                for(String browser : osExp.keySet()){
                    double cost = osExp.get(browser);
                    dataset.addValue(cost, "Advertiser " + String.valueOf(advertiser.getId()), browser);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }     
    
    private static void createHourlyExpenditureDistributionChart() throws IOException{
        String title = "Hourly expenditure distribution";
        String xLabel = "Hour of the day";
        String yLabel = "Expenditure (CNY)";
        String fileName = "hourlyCOST_";
        
        // clicks per advertiser:
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                double[] hourlyCosts = new double[24];
                for(Impression imp : advertiser.getImpressions()){
                    hourlyCosts[imp.getTime().getHour()] += (((double)imp.getPayPrice()/(double)1000))/(double)100;
                }
                
                for(int i = 0; i < hourlyCosts.length; i++){
                    String hour = String.valueOf(i); // don't -1, hour "0" might really mean midnight, and not 1am, abd time matters! 
                    dataset.addValue(hourlyCosts[i], "Advertiser " + String.valueOf(advertiser.getId()), hour);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }      
    
    private static void createHourlyCTRDistributionChart() throws IOException{
        String title = "Hourly CTR distribution";
        String xLabel = "Hour of the day";
        String fileName = "hourlyCTR_";
        String yLabel = "CTR (%)";
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                int[] hourClickCount = new int[24];
                int[] hourImpCount = new int[24];
                for(Impression imp : advertiser.getImpressions()){
                    if(imp.isIsClicked()) hourClickCount[imp.getTime().getHour()] += 1;
                    hourImpCount[imp.getTime().getHour()] += 1;
                }
                
                for(int i = 0; i < hourImpCount.length; i++){
                    double ctr = ((double)hourClickCount[i]/(double)hourImpCount[i])*(double)100;
                    String hourlyCtr = String.valueOf(i+1); //to turn min of 0 to 1 and 23 into 24, although it doesn't matter 
                    dataset.addValue(ctr, "Advertiser " + String.valueOf(advertiser.getId()), hourlyCtr);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }   
    
    private static void createRegionalCTRDistributionChart(boolean regionMode) throws IOException{
        String title = regionMode ? "Regional CTR distribution" : "CTR distribution by city";
        String xLabel = regionMode ? "Regions" : "Cities";
        String fileName = regionMode ? "regionCTR_" : "cityCTR_";
        String yLabel = "CTR (%)";
        int maxCityRegionInt = regionMode ? (395 + 1) : (399 + 1);
 
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                int[] regionClickCount = new int[maxCityRegionInt]; // 7 days, 0 - 6
                int[] regionImpCount = new int[maxCityRegionInt];
                for(Impression imp : advertiser.getImpressions()){
                    int id = (regionMode) ? imp.getUser().getRegion() : imp.getUser().getCity();
                    if(imp.isIsClicked()){
                        regionClickCount[id] += 1;
                    }
                    if(id < 0) System.out.println("region or city is empty/missing!!!");
                    if(id < 0) continue; //i.e if region or city has no/missing value (-1)
                    regionImpCount[id] += 1;
                }
                
                for(int i = 0; i < regionImpCount.length; i++){
                    if(regionImpCount[i] == 0) continue;
                    double ctr = ((double)regionClickCount[i]/(double)regionImpCount[i])*(double)100;
                    String regionalCtr = String.valueOf(i+1);
                    dataset.addValue(ctr, "Advertiser " + String.valueOf(advertiser.getId()), regionalCtr);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new StackedBarRenderer());
    }    
    

    
    /**
     * Visualise regional click distribution.
     * @param regionMode should be true if distribution to be shown regionally, false if shown by specific city
     * @throws IOException 
     */
    private static void createRegionalClickDistributionChart(boolean regionMode) throws IOException{
        String title = regionMode ? "Regional click distribution" : "Click distribution by city";
        String xLabel = regionMode ? "Regions" : "Cities";
        String fileName = regionMode ? "regionCLICK_" : "cityCLICK_";
        String yLabel = "Number of Clicks";
        int maxCityRegionInt = regionMode ? (395 + 1) : (399 + 1);
        
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                int[] regionClickCount = new int[maxCityRegionInt]; // 7 days, 0 - 6
                for(Impression imp : advertiser.getImpressions()){
                    if(imp.isIsClicked()){
                        int id = imp.getUser().getCity();
                        if(regionMode){
                            id = imp.getUser().getRegion();
                        }
                        if(id < 0) continue; //i.e if region or city has no/missing value (-1)
                        regionClickCount[id] += 1;
                    }
                }
                for(int i = 0; i < regionClickCount.length; i++){
                    if(regionClickCount[i] == 0 && regionMode) continue;
                    if(regionClickCount[i] < 3 && !regionMode) continue;
                    String weekday = String.valueOf(i+1);
                    dataset.addValue(regionClickCount[i], "Advertiser " + String.valueOf(advertiser.getId()), weekday);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new BarRenderer());
    }
    
    private static void createHourlyClickDistributionChart(boolean isHourly) throws IOException{
        String title = isHourly ? "Hourly Click distribution" : "Weekly Click distribution";
        String xLabel = isHourly ? "Hour of the day" : "Day of the week";
        String fileName = isHourly ? "hourlyCLICK_" : "weeklyCLICK_";
        String yLabel = "Number of clicks";
 
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            if(isWantedAdvertiser(advertiser.getId())){
                int size = isHourly ? 24 : 7;
                int[] clickCount = new int[size];
                for(Impression imp : advertiser.getImpressions()){
                    int index = isHourly ? imp.getTime().getHour() : imp.getTime().getDay();
                    if(imp.isIsClicked()){
                        clickCount[index] += 1;
                    }
                }
               
                for(int i = 0; i < clickCount.length; i++){
                    String weekday = String.valueOf(i+1);
                    dataset.addValue(clickCount[i], "Advertiser " + String.valueOf(advertiser.getId()), weekday);
                }
            }
        }
        createChart(xLabel,yLabel,dataset,title,fileName,new BarRenderer());
    }       
    
    private static void createClicksPerAdvertiserChart() throws IOException{
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for(Advertiser advertiser : advertisers){
            String category = String.valueOf(advertiser.getId());
            int clickCount = 0;
            for(Impression imp : advertiser.getImpressions()){
                clickCount += (imp.isIsClicked()) ? 1 : 0;
            }
            dataset.addValue(clickCount, "Clicks", category);
        }
        createChart("Advertisers", "Clicks", dataset, "Advertiser click distribution", "advertiserCLICK_", new BarRenderer());         
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
                cost += impression.getPayPrice() / 1000.0;
                bid += impression.getBidPrice() / 1000.0;
            }
            double avgBid = bid/(double)impCount;
            double avgPay = cost/(double)impCount;
            double cpm = (cost/(double)impCount)*1000;
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
    
    private static void createChart(String xLabel, String yLabel, DefaultCategoryDataset dataset, String title, String fileName, BarRenderer renderer) throws IOException{
        renderer.setBarPainter(new StandardBarPainter());
        renderer.setDrawBarOutline(false);
        renderer.setShadowVisible(false);
        renderer.setItemMargin(0.003);
        CategoryAxis ca = new CategoryAxis(xLabel);
        ca.setCategoryLabelPositions(CategoryLabelPositions.UP_45);  

        CategoryPlot plot = new CategoryPlot(dataset,ca,new NumberAxis(yLabel),renderer);

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
    
    private static String createHeaderFormatString(int headerLength){
        String s = "";
        for(int i = 0; i < headerLength; i++) s += "%5s";
        return s;
    }
    
    private static String createRowFormatString(String[] header){
        String s = "";
        for(int i = 0; i < header.length; i++){
            s += "%" + header[i].length() + "s";
        }
        return s;
    }   
}
