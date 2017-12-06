package com.example.anthonydelarosa.senior_design;
import android.app.Activity;
import android.content.Intent;
import android.icu.util.Calendar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.TimePicker;
import java.util.Arrays;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONObject;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.app.Activity;
import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.appindexing.Thing;
import com.google.android.gms.common.api.GoogleApiClient;

public class Settings extends AppCompatActivity implements OnClickListener{
    Tea tea;
    private GoogleApiClient client;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        TextView tvIsConnected = (TextView) findViewById(R.id.tvIsConnected);;
        Button btnPost = (Button) findViewById(R.id.Start);
        Spinner mySpinner = (Spinner) findViewById(R.id.spinner);
        Spinner teaSpinner = (Spinner) findViewById(R.id.spinner2);

        // check if you are connected or not
        if (isConnected()) {
            tvIsConnected.setBackgroundColor(0xFF00CC00);
            tvIsConnected.setText("You are connected");
        } else {
            tvIsConnected.setText("You are NOT conncted");
        }

        // add click listener to Button "POST"
        btnPost.setOnClickListener(this);
        Button timedate = (Button) findViewById(R.id.toTime);
        mySpinner = (Spinner) findViewById(R.id.spinner);
        teaSpinner = (Spinner) findViewById(R.id.spinner2);
        timedate.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                Intent next = new Intent(getApplicationContext(),timedate.class);
                startActivityForResult(next,2000);
            }
        });

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }

    public void onClick(View view) {
        Bundle bundle = getIntent().getExtras();
        String startAdress = "http://";
        String ip = bundle.getString("stuff");
        String send = startAdress + ip;
        Spinner mySpinner = (Spinner) findViewById(R.id.spinner);
        Spinner teaSpinner = (Spinner) findViewById(R.id.spinner2);
        Intent next = setSpinners();
        //Later change this value depending on strength??
        next.putExtra("date", TimeUnit.MINUTES.toMillis(5));
        setResult(Activity.RESULT_OK,next);
        switch (view.getId()) {
            case R.id.Start:
                if (!validate())
                    Toast.makeText(getBaseContext(), "Enter some data!", Toast.LENGTH_LONG).show();
                // call AsynTask to perform network operation on separate thread
                new HttpAsyncTask(teaSpinner.getSelectedItem().toString(),mySpinner.getSelectedItem().toString()).execute(send);
                break;
        }

        finish();
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        if(requestCode == 2000){
            if (resultCode == RESULT_OK){
                Bundle extras = data.getExtras();
                long myEtLong;
                Intent next = setSpinners();
                if (extras != null) {
                    myEtLong = extras.getLong("date");
                    next.putExtra("date",myEtLong);
                    setResult(Activity.RESULT_OK, next);
                    finish();
                }
            }
            if (requestCode == Activity.RESULT_CANCELED) {

            }

        }
    }

    private Intent setSpinners(){
        Spinner mySpinner = (Spinner) findViewById(R.id.spinner);
        Spinner teaSpinner = (Spinner) findViewById(R.id.spinner2);
        Intent next = new Intent(this, HomePage.class);
        String strength = mySpinner.getSelectedItem().toString();
        next.putExtra("strength" , strength);
        String tea = teaSpinner.getSelectedItem().toString();
        next.putExtra("tea" , tea);
        return next;
    }

    public String POST(String url, Tea tea) {
        InputStream inputStream = null;
        String result = "";
        try {

            // 1. create HttpClient
            HttpClient httpclient = new DefaultHttpClient();

            // 2. make POST request to the given URL
            HttpPost httpPost = new HttpPost(url);

            String json = "";

            // 3. build jsonObject
            Bundle bundle2 = getIntent().getExtras();
            String password = bundle2.getString("stuff2");
            JSONObject jsonObject = new JSONObject();
            jsonObject.accumulate("tea", tea.getTea());
            jsonObject.accumulate("strength", tea.getStrength());
            jsonObject.accumulate("key", password);

            // 4. convert JSONObject to JSON to String
            json = jsonObject.toString();

            // ** Alternative way to convert Person object to JSON string usin Jackson Lib
            // ObjectMapper mapper = new ObjectMapper();
            // json = mapper.writeValueAsString(person);

            // 5. set json to StringEntity
            StringEntity se = new StringEntity(json);

            // 6. set httpPost Entity
            httpPost.setEntity(se);

            // 7. Set some headers to inform server about the type of the content
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");

            // 8. Execute POST request to the given URL
            HttpResponse httpResponse = httpclient.execute(httpPost);

            // 9. receive response as inputStream
            inputStream = httpResponse.getEntity().getContent();

            // 10. convert inputstream to string
            if (inputStream != null)
                result = convertInputStreamToString(inputStream);
            else
                result = "Did not work!";

        } catch (Exception e) {
            Log.d("InputStream", e.getLocalizedMessage());
        }

        // 11. return result
        Log.i(result,"out");
        return result;
    }

    public boolean isConnected() {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }

    private class HttpAsyncTask extends AsyncTask<String, Void, String>
    {
        String myTea;
        String myStrength;
        public HttpAsyncTask(String tea, String strength)
        {
            myTea = tea;
            myStrength = strength;
        }
        protected String doInBackground(String... urls) {

            tea = new Tea();
            tea.setTea(myTea);
            tea.setStrength(myStrength);

            return POST(urls[0], tea);
        }

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            Toast.makeText(getBaseContext(), "Data Sent!", Toast.LENGTH_LONG).show();
        }
    }

    private boolean validate() {
        Spinner mySpinner = (Spinner) findViewById(R.id.spinner);
        Spinner teaSpinner = (Spinner) findViewById(R.id.spinner2);
        if (teaSpinner.getSelectedItem().toString().trim().equals(""))
            return false;
        else if (mySpinner.getSelectedItem().toString().trim().equals(""))
            return false;
        else
            return true;
    }

    private static String convertInputStreamToString(InputStream inputStream) throws IOException
    {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        String line = "";
        String result = "";
        while ((line = bufferedReader.readLine()) != null)
            result += line;

        inputStream.close();
        return result;
    }
}