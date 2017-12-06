package com.example.anthonydelarosa.senior_design;

/**
 * Created by Anthony De La Rosa on 2/22/2017.
 */

public class Tea {

    private String tea;
    private String strength;

    public String getTea() {
        return tea;
    }

    public void setTea(String tea) {
        this.tea = tea;
    }

    public String getStrength() {
        return strength;
    }

    public void setStrength(String strength) {
        this.strength = strength;
    }

    @Override
    public String toString() {
        return "Person [Tea=" + tea + ", Strength=" + strength+"]";
    }


}