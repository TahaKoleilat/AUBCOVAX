package com.example.aubcovax;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

public class MainPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_page);
    }
    public void btnPatient(View view){
        Intent i = new Intent(getApplicationContext(), PatientLogin.class);
        startActivity(i);
    }
    public void btnAdmin(View view){
        Intent i = new Intent(getApplicationContext(), AdminLogin.class);
        startActivity(i);
    }
    public void btnPersonnel(View view){
        Intent i = new Intent(getApplicationContext(), PersonnelLogin.class);
        startActivity(i);
    }
}