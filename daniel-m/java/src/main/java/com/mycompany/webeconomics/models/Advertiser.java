/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.webeconomics.models;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author dani_
 */
public class Advertiser {
    private int id;
    private List<Impression> impressions;

    public Advertiser(int id) {
        this.id = id;
        this.impressions = new ArrayList<>();
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public List<Impression> getImpressions() {
        return impressions;
    }

    public void setImpressions(List<Impression> impressions) {
        this.impressions = impressions;
    }
    
    public void addImpression(Impression impression){
        this.impressions.add(impression);
    }
}
