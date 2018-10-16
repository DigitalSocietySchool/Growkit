package com.example.joelruhe.myapplication;

import android.content.Intent;
import android.graphics.drawable.AnimationDrawable;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;

public class Splashscreen extends AppCompatActivity {
    AnimationDrawable plantAnimation;
    private static int SPLASH_TIME_OUT = 3000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.splashscreen);

        ImageView imageView= (ImageView)findViewById(R.id.splashscreenAnimationView);
        imageView.setBackgroundResource(R.drawable.splashscreen_animation);
        plantAnimation = (AnimationDrawable) imageView.getBackground();

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent homeIntent = new Intent(Splashscreen.this, MainActivity.class);
                startActivity(homeIntent);
                finish();
            }
        }, SPLASH_TIME_OUT);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        plantAnimation.start();
    }
}
