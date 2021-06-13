package com.example.fotosinteza;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;

public class AddImage extends AppCompatActivity {

    private static final int PERMISSION_ALL = 123;
    private static final int PERMISSION_CODE = 1000;
    ImageView plantImage;
    Button captureBtn;
    Uri image_uri;
    String curUserID;
    LocationManager locationManager;
    Location lok;
    TextView errorText;
    double lat;
    double lon;
    String BOUNDARY = "s2retfgsGSRFsERFGHfgdfgw734yhFHW567TYHSrf4yarg"; //This the boundary which is used by the server to split the post parameters.
    String MULTIPART_FORMDATA = "multipart/form-data;boundary=" + BOUNDARY;

    String[] PERMISSIONS = {
            android.Manifest.permission.ACCESS_FINE_LOCATION,
            android.Manifest.permission.INTERNET,
            android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
            android.Manifest.permission.ACCESS_NETWORK_STATE,
            android.Manifest.permission.CAMERA
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_image);

        errorText = findViewById(R.id.errorText2);
        plantImage = findViewById(R.id.plant_image);
        captureBtn = findViewById(R.id.captureButton);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            String[] permission = {Manifest.permission.ACCESS_FINE_LOCATION};
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                requestPermissions(permission, PERMISSION_CODE);
            }
        }

        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 2000, 10, locationListener);

        Intent i = getIntent();
        curUserID = i.getExtras().getString("userID");

        captureBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED ||
                            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED) {
                        String[] permission = {Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE};
                        requestPermissions(permission, PERMISSION_CODE);
                    } else {
                        openCamera();
                    }
                } else {
                    openCamera();
                }
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        if (!hasPermissions(this,PERMISSIONS)) {
            ActivityCompat.requestPermissions(this, PERMISSIONS, PERMISSION_ALL);
        }
    }

    private void openCamera() {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.TITLE, "New plant");
        values.put(MediaStore.Images.Media.DESCRIPTION, "Slikajte novo rastline");
        image_uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, image_uri);
        startActivityForResult(cameraIntent, 1001);
    }

    public void onAddClick(View v) {
        TextView opisView = findViewById(R.id.descriptionText);
        String opis = opisView.getText().toString();

        if(opis.trim().isEmpty()){
            errorText.setText("Vnesite opis");
        } else {
            POSTRequest(opis);
        }
    }

    private final LocationListener locationListener = new LocationListener() {
        public void onLocationChanged(Location location) {
            lon = location.getLongitude();
            lat = location.getLatitude();
        }
    };

    public void POSTRequest(String opis){
        Thread thread = new Thread(new Runnable() {

            @Override
            public void run() {
                try {
                    BitmapDrawable drawable = (BitmapDrawable) plantImage.getDrawable();
                    Bitmap bm = drawable.getBitmap();

                    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                    // In case you want to compress your image, here it's at 40%
                    bm.compress(Bitmap.CompressFormat.JPEG, 40, byteArrayOutputStream);
                    byte[] byteArray = byteArrayOutputStream.toByteArray();

                    String image = Base64.encodeToString(byteArray, Base64.DEFAULT);



                    HashMap<String, String> params = new HashMap<String, String>() {{
                        put("description", opis);
                        put("lon", String.valueOf(lon));
                        put("lat", String.valueOf(lat));
                        put("userId", curUserID);
                        put("slika", image);
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
                        URL url = new URL("http://10.0.2.2:3000/APIimage/dodaj");
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

                        Log.i("yo", result.toString());

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

    public static boolean hasPermissions(Context context, String... permissions) {
        if (context != null && permissions != null) {
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                    return false;
                }
            }
        }
        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode){
            case PERMISSION_CODE: {
                if(grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    openCamera();
                else {
                    Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK) {
            plantImage.setImageURI(image_uri);
        }
    }
}