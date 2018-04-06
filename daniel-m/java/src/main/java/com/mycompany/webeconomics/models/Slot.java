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
class Slot {
    private String id;
    private int width;
    private int height;
    private String visibility;
    private String format;
    private int price;

    public Slot(String id, int width, int height, String visibility, String format, int price) {
        this.id = id;
        this.width = width;
        this.height = height;
        this.visibility = visibility;
        this.format = format;
        this.price = price;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public String getVisibility() {
        return visibility;
    }

    public void setVisibility(String visibility) {
        this.visibility = visibility;
    }

    public String getFormat() {
        return format;
    }

    public void setFormat(String format) {
        this.format = format;
    }

    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "Slot{" + "id=" + id + ", width=" + width + ", height=" + height + ", visibility=" + visibility + ", format=" + format + ", price=" + price + '}';
    }
    
    
}
