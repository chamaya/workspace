package com.example.camaya.pokemonteambuilder;


import android.content.res.Resources;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.ShapeDrawable;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.res.ResourcesCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.koushikdutta.async.future.Future;
import com.koushikdutta.async.future.FutureCallback;
import com.koushikdutta.ion.Ion;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Stack;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ThreadLocalRandom;

import butterknife.BindView;
import butterknife.ButterKnife;


public class PokemonCardFragment extends Fragment {

    @BindView(R.id.pokemon_image)
    ImageView PokemonImage;
    @BindView(R.id.pokemon_name)
    TextView PokemonName;
    @BindView (R.id.pokemon_type)
    TextView PokemonType;
    @BindView(R.id.pokemon_details_layout)
    LinearLayout PokemonDetailsLayout;


    int PokemonId;
    Future<String> PokemonNameThread;
    Pokemon CurrentPokemon;
    HashMap<Integer, Pokemon> PokemonBuilding = new HashMap<Integer,Pokemon>();
    Stack<Pokemon> PokemonReady = new Stack<Pokemon>();

    final String POKEMON_IMAGE_URL = "https://www.serebii.net/art/th/%d.png";
    final String POKEMON_INFO_URL = "https://pokeapi.co/api/v2/pokemon/%d/";
    final int NUMBER_OF_POKEMON_MOVES = 4;
    public static final HashMap<String, Integer> POKEMON_TYPE_COLORS = new HashMap<String, Integer>(){
        {
            put("Normal", R.color.NormalType);
            put("Fire", R.color.FireType);
            put("Water", R.color.WaterType);
            put("Electric", R.color.ElectricType);
            put("Grass", R.color.GrassType);
            put("Ice", R.color.IceType);
            put("Fighting", R.color.FightingType);
            put("Poison", R.color.PoisonType);
            put("Ground", R.color.GroundType);
            put("Flying", R.color.FlyingType);
            put("Psychic", R.color.PsychicType);
            put("Bug", R.color.BugType);
            put("Rock", R.color.RockType);
            put("Ghost", R.color.GhostType);
            put("Dragon", R.color.DragonType);
            put("Dark", R.color.DarkType);
            put("Steel", R.color.SteelType);
            put("Fairy", R.color.FairyType);
        }
    };

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
        if(savedInstanceState == null && CurrentPokemon == null){
            updateCardById(4);
        }
        else if(savedInstanceState == null && CurrentPokemon != null){
            updateCardByPokemon(CurrentPokemon);
        }
        else{
            Pokemon pokemon = (Pokemon) savedInstanceState.getSerializable("CurrentPokemon");
            updateCardByPokemon(pokemon);
        }

    }

    @Override
    public void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putInt("PokemonId", PokemonId);
        outState.putSerializable("CurrentPokemon", CurrentPokemon);
    }

    public void updateCardById(int id){
        CurrentPokemon = new Pokemon();
        CurrentPokemon.setId(id);
        PokemonId = id;
        final Pokemon pokemon = new Pokemon();
        pokemon.setId(id);
        PokemonBuilding.put((Integer) pokemon.getId(), pokemon);


        LinearLayout moveLayout = getActivity().findViewById(R.id.pokemon_move_layout);
        moveLayout.removeAllViews();

        resetLayout();


        final String pokemonImageUrlFormated = String.format(POKEMON_IMAGE_URL, PokemonId);
        Picasso.get()
                .load(pokemonImageUrlFormated)
                .placeholder(R.drawable.pikachu_sill)
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
                            setLayout(pokemonJson, pokemon.getId());

                        }catch(JSONException je) {
                            Log.v("HELP", pokemonInfoUrlFormated);
                        }
                    }

                });

    }

    public void updateCardByPokemon(Pokemon pokemon){
        LinearLayout moveLayout = getActivity().findViewById(R.id.pokemon_move_layout);
        moveLayout.removeAllViews();

        resetLayout();
        PokemonId = pokemon.getId();
        //will probably be removed when threading
        CurrentPokemon = pokemon;
        final String pokemonImageUrlFormated = String.format(POKEMON_IMAGE_URL, pokemon.getId());
        Picasso.get()
                .load(pokemonImageUrlFormated)
                .placeholder(R.drawable.pikachu_sill)
                .into(PokemonImage);

        //replace with function
        PokemonName.setText(pokemon.getName());
        PokemonType.setText(pokemon.getType());
        int color = POKEMON_TYPE_COLORS.get(pokemon.getMainType());
        PokemonDetailsLayout.setBackgroundColor(getResources().getColor(color));

        for(int moveIndex = 0; moveIndex < pokemon.movePoolSize(); moveIndex++) {
            setPokemonMoveLayout(pokemon.moveName(moveIndex), pokemon.movePower(moveIndex), pokemon.moveType(moveIndex));
        }


    }

    private void resetLayout() {
        PokemonName.setText("Loading...");
        PokemonType.setText("...");

    }

    private void setLayout(JSONObject pokemonJson, Integer pokemonId){
        String pokemonName = "";
        String pokemonType = "";
        String pokemonMoves = "";
        String mainType = "";
        Pokemon pokemon = PokemonBuilding.get(pokemonId);
        try {
            pokemonName = pokemonJson.getJSONObject("species").getString("name");
            pokemonName = capitalizeFirstLetter(pokemonName);

            JSONArray pokemonTypeArray;
            pokemonTypeArray = pokemonJson.getJSONArray("types");
            for(int type = 0; type < pokemonTypeArray.length(); type++){
                pokemonType += capitalizeFirstLetter(pokemonTypeArray.getJSONObject(type).getJSONObject("type").getString("name")) + "/";
                if(pokemonTypeArray.getJSONObject(type).getInt("slot") == 1){
                    mainType = capitalizeFirstLetter(pokemonType.split("/")[type]);
                }
            }
            pokemonType = pokemonType.substring(0,pokemonType.length() - 1);

            JSONArray pokemonMovesArray = pokemonJson.getJSONArray("moves");
            if(pokemonMovesArray.length() <= NUMBER_OF_POKEMON_MOVES){
                for(int move = 0; move < pokemonMovesArray.length(); move++){
                    addPokemonMove(pokemonMovesArray.getJSONObject(move).getJSONObject("move"), pokemon.getId());
                }
            }else{
                int move = ThreadLocalRandom.current().nextInt(pokemonMovesArray.length());
                for(int c =0; c < NUMBER_OF_POKEMON_MOVES; c++,
                    move = (move + 1) % pokemonMovesArray.length()){
                    addPokemonMove(pokemonMovesArray.getJSONObject(move).getJSONObject("move"), pokemon.getId());
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }

        pokemon = PokemonBuilding.get(pokemon.getId());


        pokemon.setName(pokemonName);
        pokemon.setType(pokemonType);
        pokemon.setMainType(mainType);

        finishThread(pokemon);


    }

    private void addPokemonMove(JSONObject move, final Integer pokemonId) {
        try {
            final String moveName = capitalizeFirstLetter(move.getString("name"));
            final String moveUrl = move.getString("url");
            Ion.with(this)
                .load(moveUrl)
                .asString()
                .setCallback(new FutureCallback<String>() {
                    @Override
                    public void onCompleted(Exception e, String result) {
                        try{
                            if(e instanceof CancellationException){
                                throw new CancellationException();
                            }
                            JSONObject pokemonJson = new JSONObject(result);
                            Integer power = pokemonJson.optInt("power");
                            String type = capitalizeFirstLetter(pokemonJson.getJSONObject("type").getString("name"));
                            Pokemon pokemon = PokemonBuilding.get(pokemonId);
                            pokemon.addMove(moveName, power, type);
                            PokemonBuilding.put(pokemonId, pokemon);
                            if(pokemon.movePoolSize() == NUMBER_OF_POKEMON_MOVES) {
                                finishThread(pokemon);
                            }

                        }catch(JSONException je) {
                            Log.v("HELP", moveUrl);
                        }catch(CancellationException ce){
                            return;
                        }
                    }

                });



        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private void finishThread(Pokemon pokemon) {
        if(pokemon.isReady()) {
            if (pokemon.getId() == CurrentPokemon.getId()) {
                //replace with function
                {
                    PokemonType.setText(pokemon.getType());
                    PokemonName.setText(pokemon.getName());
                    int color = POKEMON_TYPE_COLORS.get(pokemon.getMainType());
                    PokemonDetailsLayout.setBackgroundColor(getResources().getColor(color));
                    for (int moveIndex = 0; moveIndex < pokemon.movePoolSize(); moveIndex++) {
                        setPokemonMoveLayout(pokemon.moveName(moveIndex), pokemon.movePower(moveIndex), pokemon.moveType(moveIndex));
                    }
                }
                CurrentPokemon = pokemon;
            }

            PokemonBuilding.remove(pokemon.getId());
            PokemonReady.push(pokemon);
        }
    }

    private void setPokemonMoveLayout(String moveName, int power, String type) {

        LinearLayout moveLayout = getActivity().findViewById(R.id.pokemon_move_layout);
        View move = getLayoutInflater().inflate(R.layout.layout_move, moveLayout,false);
        TextView moveNameTv =  move.findViewById(R.id.move_name_tv);
        TextView movePowerTv =  move.findViewById(R.id.move_power_tv);
        moveNameTv.setText(moveName);
        movePowerTv.setText(power + "");
        int color = POKEMON_TYPE_COLORS.get(type);
        GradientDrawable bg = (GradientDrawable) move.getBackground();
        bg.setColor(getResources().getColor(color));

        moveLayout.addView(move);


    }

    private String capitalizeFirstLetter(String str){
        if(str.length() > 1) {
            return str.substring(0, 1).toUpperCase() + str.substring(1);
        }else{
            return str.toUpperCase();
        }
    }


    public Pokemon getPokemon() {
        if(PokemonReady.empty()){
            return null;
        }
        return PokemonReady.pop();
    }
}
//java.util.concurrent.CancellationException