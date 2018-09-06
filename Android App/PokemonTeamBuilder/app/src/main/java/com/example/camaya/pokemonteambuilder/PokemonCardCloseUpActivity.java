package com.example.camaya.pokemonteambuilder;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import java.util.ArrayList;

public class PokemonCardCloseUpActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon_card_close_up);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        int pokemonId = bundle.getInt("pokemonId");

        PokemonCardFragment pokemonCard = (PokemonCardFragment) getSupportFragmentManager().findFragmentById(R.id.card_fragment_close_up);
        pokemonCard.updateCardById(pokemonId);
    }
}
