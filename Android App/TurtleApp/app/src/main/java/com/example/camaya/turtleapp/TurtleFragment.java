package com.example.camaya.turtleapp;


import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import butterknife.BindView;
import butterknife.ButterKnife;


/**
 * A simple {@link Fragment} subclass.
 */
public class TurtleFragment extends Fragment {

    @BindView(R.id.title)
    public TextView title;
    @BindView(R.id.turtle_image)
    public ImageButton img;

    public TurtleFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_turtle, container, false);
        ButterKnife.bind(this, view);
        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        View.OnClickListener listener = new View.OnClickListener(){
            @Override
            public void onClick(View v){
                        radioClick(v);
            }
        };
        RadioButton turtleChoice = getActivity().findViewById(R.id.leo_button);
        turtleChoice.setOnClickListener(listener);
        turtleChoice = getActivity().findViewById(R.id.mike_button);
        turtleChoice.setOnClickListener(listener);
        turtleChoice = getActivity().findViewById(R.id.don_button);
        turtleChoice.setOnClickListener(listener);
        turtleChoice = getActivity().findViewById(R.id.raph_button);
        turtleChoice.setOnClickListener(listener);

        img.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                turtlePictureClick(v);
            }
        });


    }

    @Override
    public void onViewStateRestored(@Nullable Bundle savedInstanceState) {
        super.onViewStateRestored(savedInstanceState);
        Log.v("RestoreState", "IN RESTORE STATE");
        String Turtle = "Leo";
        if(savedInstanceState != null) {
            Turtle = savedInstanceState.getString("Turtle", "Leo");
        }
        buildTurtleFragment(Turtle);
    }

    @Override
    public void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putString("Turtle", getActiveTurtle());
    }

    public void radioClick(View view) {
        buildTurtleFragment(getActiveTurtle());
    }

    public void turtlePictureClick(View view) {

        Intent intent = new Intent(getActivity(), TurtleDetailsActivity.class);
        Toast.makeText(getActivity(), title.getText(), Toast.LENGTH_SHORT).show();

        intent.putExtra("num", getTurtleNum());
        startActivity(intent);

    }

    private void buildTurtleFragment(String name){
        if(name.equals("Leo")){
            img.setImageResource(R.drawable.turtle1);
        } else if(name.equals("Mike")){
            img.setImageResource(R.drawable.turtle2);

        } else if (name.equals("Don")) {
            img.setImageResource(R.drawable.turtle3);

        } else if (name.equals("Raph")){
            img.setImageResource(R.drawable.turtle4);

        }

        title.setText(name);

        if(getResources().getConfiguration().orientation == Configuration.ORIENTATION_LANDSCAPE) {
            Log.v("Orientation", "Orientation is getting changed via name: " + name);
            TurtleDetailsFragment frag = (TurtleDetailsFragment) getActivity().getSupportFragmentManager().findFragmentById(R.id.fragment2);
            frag.setActiveTurtle(getTurtleNum());
        }
    }

    private String getActiveTurtle(){
        int [] turtleIds = {R.id.leo_button, R.id.mike_button, R.id.don_button, R.id.raph_button};
        for(int turtleId : turtleIds){
            RadioButton turtleRadio = getActivity().findViewById(turtleId);
            if(turtleRadio.isChecked()){
                String name = getResources().getResourceEntryName(turtleId).split("_button")[0];
                name = name.substring(0,1).toUpperCase() + name.substring(1);
                return name;
            }

        }
        return "Leo";

    }

    private int getTurtleNum(){
        String name = getActiveTurtle();
        int num = 0;
        if (name.equals("Leo")) {
            num = 0;
        }
        if (name.equals("Mike")) {
            num = 1;

        }
        if (name.equals("Don")) {
            num = 2;
        }
        if (name.equals("Raph")) {
            num = 3;
        }
        Log.v("getTrutleNum", "Getting the turtle NUM:  " + num);
        return num;
    }

}
