package com.example.camaya.turtleapp;


import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


/**
 * A simple {@link Fragment} subclass.
 */
public class    TurtleDetailsFragment extends Fragment {

    private static final String[] TURTLE_INFO = {
            "Leonardo, or Leo is one of the four protagonists of the Teenage Mutant Ninja Turtles",
            "Michaelangelo, or Mike is one of the four protagonists of the Teenage Mutant Ninja Turtles",
            "Donatello, or Don is one of the four protagonists of the Teenage Mutant Ninja Turtles",
            "Raphael, or Raph is one of the four protagonists of the Teenage Mutant Ninja Turtles"
    };

    public TurtleDetailsFragment() {
        // Required empty public constructor
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        Intent intent = getActivity().getIntent();
        int num = intent.getIntExtra("num", /*default*/ -1);
        if(num != -1){
            setActiveTurtle(num);
        }

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_turtle_details, container, false);
    }

    public void setActiveTurtle(int num){
        String text = TURTLE_INFO[num];

        TextView theText = getActivity().findViewById(R.id.the_text);
        theText.setText(text);
    }

}
