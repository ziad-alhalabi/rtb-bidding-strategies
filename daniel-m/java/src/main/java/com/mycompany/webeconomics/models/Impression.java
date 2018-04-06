/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.webeconomics.models;

/**
 *
 * @author dani_
 */
public class Impression {
    private boolean isClicked;
    private int advertiser;
    private BasicTime time;
    private String bidId;
    private User user;
    private int adExchange;
    private String domain;
    private String url;
    private String urlId;
    private Slot slot;
    private String creative;
    private int bidPrice;
    private int payPrice; // paid price after winning the bid
    private String keyPage;

    public Impression(String[] entry) {

        this.isClicked = entry[0].equalsIgnoreCase("1");
        
        int day = -1;
        try{
            day = Integer.parseInt(entry[1]);
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }
        int hour = Integer.parseInt(entry[2]);
        this.time = new BasicTime(hour,day);
        
        this.bidId = entry[3];
        
        int uRegion = -1;
        int uCity = -1;
        try{
            uRegion = Integer.parseInt(entry[7]);        
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }
        
        try{
            uCity = Integer.parseInt(entry[8]);    
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }
        this.user = new User(entry[4],entry[5],entry[6],uRegion,uCity,entry[24]);
        
        this.adExchange = -1;
        try{
            this.adExchange = Integer.parseInt(entry[9]);
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }

        this.domain = entry[10];
        this.url = entry[11];
        this.urlId = entry[12];        
        
        int sWidth = -1;
        int sHeight = -1;
        int sPrice = -1;
     
        try{
            sWidth = Integer.parseInt(entry[14]);           
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }

        try{
            sHeight = Integer.parseInt(entry[15]);
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }

        try{
            sPrice = Integer.parseInt(entry[18]); 
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }
        this.slot = new Slot(entry[13],sWidth,sHeight,entry[16],entry[17],sPrice);  
        
        this.creative = entry[19];
        
        this.bidPrice = -1;
        try{
            this.bidPrice = Integer.parseInt(entry[20]);
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }

        this.payPrice = -1;
        try{
            this.payPrice = Integer.parseInt(entry[21]);
        }catch(java.lang.NumberFormatException ex){
            
        }
        
        this.keyPage = entry[22];

        this.advertiser = -1;
        
        try{
            this.advertiser = Integer.parseInt(entry[23]);
        }catch(java.lang.NumberFormatException ex){
            // do nothing
        }
       
    }
    
    public boolean isIsClicked() {
        return isClicked;
    }

    public void setIsClicked(boolean isClicked) {
        this.isClicked = isClicked;
    }

    public int getAdvertiser() {
        return advertiser;
    }

    public void setAdvertiser(int advertiser) {
        this.advertiser = advertiser;
    }

    public BasicTime getTime() {
        return time;
    }

    public void setTime(BasicTime time) {
        this.time = time;
    }

    public String getBidId() {
        return bidId;
    }

    public void setBidId(String bidId) {
        this.bidId = bidId;
    }

    public int getAdExchange() {
        return adExchange;
    }

    public void setAdExchange(int adExchange) {
        this.adExchange = adExchange;
    }

    public String getDomain() {
        return domain;
    }

    public void setDomain(String domain) {
        this.domain = domain;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getUrlId() {
        return urlId;
    }

    public void setUrlId(String urlId) {
        this.urlId = urlId;
    }

    public Slot getSlot() {
        return slot;
    }

    public void setSlot(Slot slot) {
        this.slot = slot;
    }

    public String getCreative() {
        return creative;
    }

    public void setCreative(String creative) {
        this.creative = creative;
    }

    public int getBidPrice() {
        return bidPrice;
    }

    public void setBidPrice(int bidPrice) {
        this.bidPrice = bidPrice;
    }

    public int getPayPrice() {
        return payPrice;
    }

    public void setPayPrice(int payPrice) {
        this.payPrice = payPrice;
    }

    public String getKeyPage() {
        return keyPage;
    }

    public void setKeyPage(String keyPage) {
        this.keyPage = keyPage;
    }
    
    public User getUser(){
        return user;
    }
    
    public void setUser(User user){
        this.user = user;
    }

    @Override
    public String toString() {
        return "Impression{" + "isClicked=" + isClicked + ", advertiser=" + advertiser + ", time=" + time + ", bidId=" + bidId + ", user=" + user + ", adExchange=" + adExchange + ", domain=" + domain + ", url=" + url + ", urlId=" + urlId + ", slot=" + slot + ", creative=" + creative + ", bidPrice=" + bidPrice + ", payPrice=" + payPrice + ", keyPage=" + keyPage + '}';
    }

    
}
