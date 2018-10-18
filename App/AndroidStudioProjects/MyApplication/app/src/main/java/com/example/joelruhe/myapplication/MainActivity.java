package com.example.joelruhe.myapplication;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity {

    int i = 0;
    ImageView image;

    int [] images = new int[] {R.drawable.plant1, R.drawable.plant2, R.drawable.plants,
            R.drawable.cactus, R.drawable.potplant, R.drawable.longgrass};
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setLogo(R.mipmap.ic_launcher);
        getSupportActionBar().setDisplayUseLogoEnabled(true);
        setContentView(R.layout.activity_main);

        image = (ImageView)findViewById(R.id.plantSelect);

    }

    void next_plant(View v){
        i++;
        if(i > 5){
            i=0;
        }
        image.setImageResource(images[i]);

    }

    void previous_plant(View v){
        i--;
        if(i < 0){
            i=5;
        }
        image.setImageResource(images[i]);
    }
}

