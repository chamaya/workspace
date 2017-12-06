package com.example.anthonydelarosa.senior_design;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Button btnLogin = (Button) findViewById(R.id.login_button);
        btnLogin.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                EditText password = (EditText) findViewById(R.id.password);
                EditText ip = (EditText) findViewById(R.id.username);
                //Create the bundle
                Bundle bundle = new Bundle();

                //Add your data to bundle
                bundle.putString("stuff", ip.getText().toString());
                bundle.putString("stuff2", password.getText().toString());
                if(password.getText().toString().contains("TEATEAM123"))
                {
                    Intent next = new Intent(getApplicationContext(), HomePage.class);
                    next.putExtras(bundle);
                    startActivityForResult(next, 1000);
                }
                else
                {
                    Toast.makeText(getBaseContext(), "Invalid Password", Toast.LENGTH_LONG).show();
                }
            }
        });

    }
}
