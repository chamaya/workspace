package com.example.camaya.pokemonteambuilder;

import android.content.Intent;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

public class PokemonSelectorActivity extends AppCompatActivity {
    final int NUMBER_OF_POKEMON = 802;
    final String POKEBALL_IMAGE = "pokeball_image_%d";
    public ArrayList<Integer> PokemonAdded;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon_selector);
        PokemonAdded = new ArrayList<Integer>();
        addPokeballs();
    }


    public void addPokemon(View view) {

        PokemonCardFragment pokemonCard = (PokemonCardFragment) getSupportFragmentManager().findFragmentById(R.id.card_fragment);
        int pokemonId = getRandomPokemon();
        pokemonCard.updateCardById(pokemonId);

        PokemonAdded.add(pokemonId);
        addPokeballs();

        if(PokemonAdded.size() >= 6){
            Intent intent = new Intent(PokemonSelectorActivity.this, PokemonSpriteViewActivity.class);

            startActivity(intent);
        }
    }

    public void skipPokemon(View view) {
        PokemonCardFragment pokemonCard = (PokemonCardFragment) getSupportFragmentManager().findFragmentById(R.id.card_fragment);
        int pokemonId = getRandomPokemon();
        pokemonCard.updateCardById(pokemonId);
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
        for(int pokemon = 0; pokemon < 6-PokemonAdded.size(); pokemon++){
            getLayoutInflater().inflate(R.layout.pokeball, pokeballLayout);
        }
    }

    private int getRandomPokemon(){
        return ThreadLocalRandom.current().nextInt(1,NUMBER_OF_POKEMON + 1);
    }

}
