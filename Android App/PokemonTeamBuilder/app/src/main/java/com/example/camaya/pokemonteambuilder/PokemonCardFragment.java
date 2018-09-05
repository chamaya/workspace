package com.example.camaya.pokemonteambuilder;


import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.koushikdutta.async.future.FutureCallback;
import com.koushikdutta.ion.Ion;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import butterknife.BindView;
import butterknife.ButterKnife;


/**
 * A simple {@link Fragment} subclass.
 */


public class PokemonCardFragment extends Fragment {

    @BindView(R.id.pokemon_image)
    ImageView PokemonImage;
    @BindView(R.id.pokemon_name)
    TextView PokemonName;

    int PokemonId;

    final String POKEMON_IMAGE_URL = "https://www.serebii.net/art/th/%d.png";
    final String POKEMON_INFO_URL = "https://pokeapi.co/api/v2/pokemon/%d/";

    public PokemonCardFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_pokemon_card, container, false);
        ButterKnife.bind(this,view);
        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
    }

    @Override
    public void onViewStateRestored(@Nullable Bundle savedInstanceState) {
        super.onViewStateRestored(savedInstanceState);
        if(savedInstanceState == null){
            PokemonId = 25;
        }
        else{
            PokemonId = savedInstanceState.getInt("PokemonId", 25);
        }
        updateCardById(PokemonId);

    }

    @Override
    public void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putInt("PokemonId", PokemonId);
    }

    public void updateCardById(int id){
        PokemonId = id;
        final String pokemonImageUrlFormated = String.format(POKEMON_IMAGE_URL, PokemonId);
        Picasso.get()
                .load(pokemonImageUrlFormated)
                .resize(1000,1000)
                .placeholder(R.drawable.mystery)
                .into(PokemonImage);

        final String pokemonInfoUrlFormated = String.format(POKEMON_INFO_URL, PokemonId);
        Ion.with(this)
                .load(pokemonInfoUrlFormated)
                .asString()
                .setCallback(new FutureCallback<String>() {
                    @Override
                    public void onCompleted(Exception e, String result) {
                        try{
                            JSONObject pokemonJson = new JSONObject(result);
                            String pokemonName = pokemonJson.getJSONObject("species").getString("name");
                            pokemonName = pokemonName.substring(0,1).toUpperCase() +
                                    pokemonName.substring(1);
                            PokemonName.setText(pokemonName);

                        }catch(JSONException je){
                            Log.v("HELP", pokemonInfoUrlFormated);
                        }
                    }
                });

    }
}
