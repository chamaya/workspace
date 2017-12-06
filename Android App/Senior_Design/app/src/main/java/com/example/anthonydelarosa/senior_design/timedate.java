package com.example.anthonydelarosa.senior_design;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.DatePicker;
import android.widget.Spinner;
import android.widget.TimePicker;

import java.util.Arrays;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.TimeUnit;

public class timedate extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_timedate);
    }

    public void startBrew(View view) {
        Intent next = new Intent(this, Settings.class);

        DatePicker datePicker = (DatePicker) findViewById(R.id.date_pick);
        long day = datePicker.getDayOfMonth();
        long month = datePicker.getMonth() + 1;
        long year = datePicker.getYear();

        TimePicker timePicker = (TimePicker) findViewById(R.id.time_pick);
        long hour = timePicker.getCurrentHour();
        long min = timePicker.getCurrentMinute();


        Date date = new Date();
        long curr_year = date.getYear() + 1900;
        long curr_month = date.getMonth() + 1;
        long curr_day = date.getDate();
        long curr_hour = date.getHours() + 1;
        long curr_min = date.getMinutes();
        long curr_sec = date.getSeconds();

        year = curr_year - year;
        TimeUnit.DAYS.toMillis(year * 365);

        Set m30 = new HashSet<Integer>(Arrays.asList(4,6,9,11));
        long mon = 0;
        long curr_mon = 0;
        if (curr_month != month){
            for(int i = 1; i <= curr_month; i++){
                if(i == 2){
                    curr_mon += TimeUnit.DAYS.toMillis(28);
                }
                else if(m30.contains(i)){
                    curr_mon += TimeUnit.DAYS.toMillis(31);
                }
                else{
                    curr_mon += TimeUnit.DAYS.toMillis(30);
                }

            }
            for(int i = 1; i <= month; i++){
                if(i == 2){
                    mon += TimeUnit.DAYS.toMillis(28);
                }
                else if(m30.contains(i)){
                    mon += TimeUnit.DAYS.toMillis(31);
                }
                else{
                    mon += TimeUnit.DAYS.toMillis(30);
                }

            }
            mon = (mon - curr_mon)% TimeUnit.DAYS.toMillis(365);
        }
        else{month = 0;}

        long day_mod = 28;
        if(m30.contains(month)){
            day_mod = 30;
        }
        else if(month != 2){
            day_mod = 31;
        }

        day = TimeUnit.DAYS.toMillis(day - curr_day % day_mod);
        hour =  TimeUnit.HOURS.toMillis((hour - curr_hour) % 24);
        min =  TimeUnit.MINUTES.toMillis((min - curr_min) % 60);
        curr_sec =  TimeUnit.SECONDS.toMillis(curr_sec);

        next.putExtra("date" , day + hour + min + curr_sec + year + mon);
        setResult(Activity.RESULT_OK,next);
        finish();
    }
}
