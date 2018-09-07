package com.example.camaya.pokemonteambuilder;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

public class PokemonSpriteViewActivity extends AppCompatActivity {

    final String POKEMON_SPRITE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%d.png";//"https://www.serebii.net/sunmoon/pokemon/%03d.png";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon_sprite_view);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        final ArrayList<Pokemon> PokemonAdded = (ArrayList) bundle.getParcelableArrayList("Pokemon");

        addPokemon(PokemonAdded);

    }

    private void addPokemon(ArrayList<Pokemon> pokemonAdded) {
        LinearLayout pokemonSpriteLayout = findViewById(R.id.pokemon_sprite_layout);
        pokemonSpriteLayout.removeAllViews();

        for (int pokemonId = 0; pokemonId < pokemonAdded.size(); pokemonId++) {
            final Pokemon pokemon = pokemonAdded.get(pokemonId);

            View inflated = LayoutInflater.from(this).inflate(R.layout.layout_sprite_pokemon, pokemonSpriteLayout, false);
            ImageButton pokemonSprite = inflated.findViewById(R.id.pokemon_sprite);
            TextView pokemonSpriteName = inflated.findViewById(R.id.pokemon_sprite_name);
            TextView pokemonSpriteType = inflated.findViewById(R.id.pokemon_sprite_type);
            TextView pokemonSpriteId = inflated.findViewById(R.id.pokemon_sprite_num);

            Picasso.get()
                    .load(String.format(POKEMON_SPRITE_URL, pokemon.getId()))
                    .resize(200, 200)
                    .centerCrop()
                    .into(pokemonSprite);
            pokemonSprite.setOnClickListener(new View.OnClickListener(){
                @Override
                public void onClick(View v) {
                    startCardCloseUp(pokemon);
                }
            });

            float[] hsv = new float[3];
            int colorButton = getResources().getColor(PokemonCardFragment.POKEMON_TYPE_COLORS.get(pokemon.getMainType()));
            Color.colorToHSV(colorButton, hsv);
            hsv[2] *= 0.9f; // value component
            colorButton = Color.HSVToColor(hsv);
            pokemonSprite.setBackgroundColor(colorButton);


            pokemonSpriteName.setText(pokemon.getName());
            pokemonSpriteType.setText(pokemon.getType());
            pokemonSpriteId.setText(pokemon.getId() + "");

            int color = PokemonCardFragment.POKEMON_TYPE_COLORS.get(pokemon.getMainType());
            GradientDrawable bg = (GradientDrawable) inflated.getBackground();
            bg.setColor(getResources().getColor(color));

            pokemonSpriteLayout.addView(inflated);

        }

    }

    private void startCardCloseUp(Pokemon pokemon) {
        Intent intent = new Intent(this, PokemonCardCloseUpActivity.class);
        intent.putExtra("pokemon", pokemon);

        startActivity(intent);
    }
}
