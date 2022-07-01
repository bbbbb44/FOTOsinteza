package com.example.fotosinteza;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void prijavaOnClick (View v) throws IOException {
        TextView usernameView = findViewById(R.id.UsernameText);
        TextView passwordView = findViewById(R.id.PasswordText);

        String username = usernameView.getText().toString();
        String password = passwordView.getText().toString();

        if(username.trim().isEmpty() || password.trim().isEmpty()){
            TextView errorView = findViewById(R.id.errorText);
            errorView.setText("Izpolnite vsa polja!");
        } else {
            Thread thread = new Thread(new Runnable() {

                @Override
                public void run() {
                    try {
                        HashMap<String, String> params = new HashMap<String, String>() {{
                            put("username", username);
                            put("password", password);
                        }};

                        StringBuilder sbParams = new StringBuilder();
                        int i = 0;
                        for (String key : params.keySet()) {
                            try {
                                if (i != 0) {
                                    sbParams.append("&");
                                }
                                sbParams.append(key).append("=")
                                        .append(URLEncoder.encode(params.get(key), "UTF-8"));

                            } catch (UnsupportedEncodingException e) {
                                e.printStackTrace();
                            }
                            i++;
                        }

                        try {
                            URL url = new URL("http://10.0.2.2:3000/APIuser/login");
                            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                            conn.setDoOutput(true);
                            conn.setRequestMethod("POST");
                            conn.setRequestProperty("Accept-Charset", "UTF-8");

                            conn.setReadTimeout(10000);
                            conn.setConnectTimeout(15000);

                            conn.connect();
                            String paramsString = sbParams.toString();

                            DataOutputStream wr = new DataOutputStream(conn.getOutputStream());
                            wr.writeBytes(paramsString);
                            wr.flush();
                            wr.close();
                            InputStream in = new BufferedInputStream(conn.getInputStream());
                            BufferedReader reader = new BufferedReader(new InputStreamReader(in));
                            StringBuilder result = new StringBuilder();
                            String line;
                            while ((line = reader.readLine()) != null) {
                                result.append(line);
                            }

                            String data = result.toString();
                            String[] splitData = data.split("\"", 0);

                            if(splitData[1].equals("status")){
                                TextView errorText = findViewById(R.id.errorText);
                                errorText.setText("Napacno uporabnisko ime ali geslo");
                            } else {
                                String userID = splitData[3];
                                Intent intent = new Intent(getApplicationContext(), AddImage.class);
                                intent.putExtra("userID", userID);
                                startActivity(intent);
                            }

                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });

            thread.start();
        }
    }
}