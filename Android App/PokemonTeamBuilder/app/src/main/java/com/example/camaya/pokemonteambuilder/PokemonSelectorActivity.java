package com.example.camaya.pokemonteambuilder;

import android.content.Intent;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

import butterknife.BindView;
import butterknife.ButterKnife;

public class PokemonSelectorActivity extends AppCompatActivity {
    final static int NUMBER_OF_POKEMON = 802;
    public ArrayList<Pokemon> PokemonAdded;
    public int addPresses;
    int layer = 0;
    int Increment = 0;

    @BindView(R.id.add_button)
    Button addButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon_selector);
        PokemonAdded = new ArrayList<Pokemon>();
        addPresses = 0;
        addPokeballs();
        ButterKnife.bind(this);
    }

    @Override
    protected void onResume() {
        super.onResume();
        addPresses = 0;
        PokemonAdded.clear();
        addPokeballs();
        addButton.setEnabled(true);
        layer++;
    }

    public void addPokemon(View view) {
        addPresses++;
        if(addPresses > 6) {
            addButton.setEnabled(false);

        }else{
            addButton.setEnabled(true);
            PokemonCardFragment pokemonCard = (PokemonCardFragment) getSupportFragmentManager().findFragmentById(R.id.card_fragment);
            Pokemon pokemon = null;
            addPokeballs();

            GetPokemonThread pokemonThread = new GetPokemonThread(pokemon, pokemonCard);
            pokemonThread.start();
            int pokemonId = getRandomPokemon();
            pokemonCard.updateCardById(pokemonId);
            if(addPresses == 6){
                Intent intent = new Intent(PokemonSelectorActivity.this, PokemonSpriteViewActivity.class);
                intent.putExtra("Pokemon", PokemonAdded);
                startActivity(intent);
            }
        }

    }

    public void skipPokemon(View view) {
        PokemonCardFragment pokemonCard = (PokemonCardFragment) getSupportFragmentManager().findFragmentById(R.id.card_fragment);
        Integer pokemonId = pokemonCard.getCurrentPokemon().getId();
        pokemonCard.cancelThread(pokemonId);
        int randomPokemonId = getRandomPokemon();
        pokemonCard.updateCardById(randomPokemonId);
    }

    private void addPokeballs(){
        LinearLayout pokeballLayout = findViewById(R.id.pokeball_layout);
        pokeballLayout.removeAllViews();
        for(int pokemon = 0; pokemon < PokemonAdded.size(); pokemon++){
            View inflated = LayoutInflater.from(this).inflate(R.layout.pokeball, pokeballLayout, false);
            ImageView pokeball =  inflated.findViewById(R.id.pokeball_image);
            pokeball.setImageResource(R.drawable.pokeball);
            pokeballLayout.addView(inflated);
        }
        for(int pokemon = 0; pokemon < addPresses-PokemonAdded.size(); pokemon++){
            View inflated = LayoutInflater.from(this).inflate(R.layout.pokeball, pokeballLayout, false);
            ImageView pokeball =  inflated.findViewById(R.id.pokeball_image);
            pokeball.setImageResource(R.drawable.pokeball_grey);
            pokeballLayout.addView(inflated);
        }
        for(int pokemon = 0; pokemon < 6-addPresses; pokemon++){
            getLayoutInflater().inflate(R.layout.pokeball, pokeballLayout);
        }
    }

    public static int getRandomPokemon(){
        return ThreadLocalRandom.current().nextInt(1,NUMBER_OF_POKEMON + 1);
    }

    public int Increment(){
        return Increment++;
    }

    class GetPokemonThread extends Thread{
        Pokemon pokemon;
        PokemonCardFragment pokemonCard;
        GetPokemonThread(Pokemon pokemon, PokemonCardFragment pokemonCard){
            this.pokemon = pokemon;
            this.pokemonCard = pokemonCard;
        }

        public void run(){

            int internalLayer = layer;
            while(pokemon == null){
                pokemon = pokemonCard.getPokemon();
                if(internalLayer != layer){
                    break;
                }
            }
            if(internalLayer != layer){
                return;
            }

            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    PokemonAdded.add(pokemon);

                    addPokeballs();

                    if(PokemonAdded.size() <= 6 && addPresses >= 6){
                        Intent intent = new Intent(PokemonSelectorActivity.this, PokemonSpriteViewActivity.class);
                        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                        intent.putExtra("Pokemon", PokemonAdded);

                        startActivity(intent);
                    }
                }
            });

        }
    }

}
