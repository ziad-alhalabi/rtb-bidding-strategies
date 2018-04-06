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
public class BasicTime {
    private int hour;
    private int day;
    
    public BasicTime(int hour, int day){
        this.hour = hour;
        this.day = day;
    }

    public int getHour() {
        return hour;
    }

    public void setHour(int hour) {
        this.hour = hour;
    }

    public int getDay() {
        return day;
    }

    public void setDay(int day) {
        this.day = day;
    }

    @Override
    public String toString() {
        return "BasicTime{" + "hour=" + hour + ", day=" + day + '}';
    }
    
    
}
