package com.example.camaya.pokemonteambuilder;

import android.graphics.drawable.GradientDrawable;
import android.support.v4.app.Fragment;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * A simple {@link Fragment} subclass.
 */

public class Pokemon implements Serializable{
    private int id;
    private String name;
    private ArrayList<Move> Moves;
    private String type;
    private String mainType;
    private String secondType;

    private static final long serialVersionUID = -7060210544600464481L;


    public Pokemon(){
        Moves = new ArrayList<Move>();
    }

    public void addMove(String name, int power, String type){
        Moves.add(new Move(name, power, type));
    }

    public void addMove(Move move){
        Moves.add(move);
    }

    public boolean hasMove(){
        return Moves != null && Moves.size() != 0;
    }

    public int movePoolSize(){
        return Moves.size();
    }

    public String moveName(int moveIndex){
        return Moves.get(moveIndex).getName();
    }

    public String moveType(int moveIndex){
        return Moves.get(moveIndex).getType();
    }

    public int movePower(int moveIndex){
        return Moves.get(moveIndex).getPower();
    }

    public String getName() {
        return name;
    }

    public void setMainType(String mainType) {
        this.mainType = mainType;
    }

    public String getMainType() {
        return mainType;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getSecondType() {
        return secondType;
    }

    public void setSecondType(String secondType) {
        this.secondType = secondType;
    }

    public boolean hasSecondType(){
        return secondType != null && !secondType.isEmpty();
    }

    public boolean hasDetails() {
        return name != null && !name.isEmpty();
    }

    public boolean isReady(){
        return hasDetails() && hasMove();
    }

    public String getSecondTypeIfNotMain() {
        if(hasSecondType()){
            return secondType;
        }else{
            return mainType;
        }
    }


    public class Move implements Serializable{
        private String name;
        private String type;
        private int power;

        private static final long serialVersionUID = -7060210544600464480L;

        public Move(String name, int power, String type){
            this.name = name;
            this.power = power;
            this.type = type;
        }

        public int getPower() {
            return power;
        }

        public String getName() {
            return name;
        }

        public String getType() {
            return type;
        }
    }

}
