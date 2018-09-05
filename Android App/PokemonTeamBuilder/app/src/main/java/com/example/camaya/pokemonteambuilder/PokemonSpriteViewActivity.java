package com.example.camaya.pokemonteambuilder;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

public class PokemonSpriteViewActivity extends AppCompatActivity {

    final String POKEMON_SPRITE_URL = "https://www.serebii.net/sunmoon/pokemon/778.png";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon_sprite_view);

        LinearLayout pokemonSpriteLayout = findViewById(R.id.pokemon_sprite_layout);
        pokemonSpriteLayout.removeAllViews();

        View inflated = LayoutInflater.from(this).inflate(R.layout.layout_sprite_pokemon, pokemonSpriteLayout, false);
        ImageView pokemonSprite =  inflated.findViewById(R.id.pokemon_sprite);
        TextView pokemonSpriteName = inflated.findViewById(R.id.pokemon_sprite_name);

        Picasso.get()
                .load("https://www.serebii.net/sunmoon/pokemon/778.png")
                .placeholder(R.drawable.pikachu_sill)
                .resize(200,200)
                .centerCrop()
                .into(pokemonSprite);

        pokemonSpriteLayout.addView(inflated);

        pokemonSpriteName.setText("Mimikyu");

        getLayoutInflater().inflate(R.layout.layout_sprite_pokemon, pokemonSpriteLayout);

    }
}
