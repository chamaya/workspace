package com.example.camaya.pokemonteambuilder;

import android.content.Intent;
import android.graphics.drawable.GradientDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

public class PokemonSpriteViewActivity extends AppCompatActivity {

    final String POKEMON_SPRITE_URL = "https://www.serebii.net/sunmoon/pokemon/%03d.png";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon_sprite_view);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        ArrayList<Pokemon> PokemonAdded = (ArrayList) bundle.getParcelableArrayList("Pokemon");

        addPokemon(PokemonAdded);

    }

    private void addPokemon(ArrayList<Pokemon> pokemonAdded) {
        LinearLayout pokemonSpriteLayout = findViewById(R.id.pokemon_sprite_layout);
        pokemonSpriteLayout.removeAllViews();

        for (int pokemonId = 0; pokemonId < pokemonAdded.size(); pokemonId++) {
            Pokemon pokemon = pokemonAdded.get(pokemonId);

            View inflated = LayoutInflater.from(this).inflate(R.layout.layout_sprite_pokemon, pokemonSpriteLayout, false);
            ImageView pokemonSprite = inflated.findViewById(R.id.pokemon_sprite);
            TextView pokemonSpriteName = inflated.findViewById(R.id.pokemon_sprite_name);
            TextView pokemonSpriteType = inflated.findViewById(R.id.pokemon_sprite_type);
            TextView pokemonSpriteId = inflated.findViewById(R.id.pokemon_sprite_num);

            Picasso.get()
                    .load(String.format(POKEMON_SPRITE_URL, pokemon.getId()))
                    .placeholder(R.drawable.pikachu_sill)
                    .resize(200, 200)
                    .centerCrop()
                    .into(pokemonSprite);

            pokemonSpriteName.setText(pokemon.getName());
            pokemonSpriteType.setText(pokemon.getType());
            pokemonSpriteId.setText(pokemon.getId() + "");

            int color = PokemonCardFragment.POKEMON_TYPE_COLORS.get(pokemon.getMainType());
            //move.setBackgroundColor(getResources().getColor(color));
            GradientDrawable bg = (GradientDrawable) inflated.getBackground();
            bg.setColor(getResources().getColor(color));

            pokemonSpriteLayout.addView(inflated);

        }

    }
}
