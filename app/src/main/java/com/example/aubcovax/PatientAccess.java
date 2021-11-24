package com.example.aubcovax;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class PatientAccess extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_access);
        Bundle bundle = getIntent().getExtras();
        String username = bundle.getString("username");
        Thread thread = new Thread(new Runnable(){@Override public void run(){
            String outData = "";
            try{
                Socket socket = new Socket("35.231.177.149", 3389);
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                String action = "Search";
                String type = "Patient";
                writer.println(action +","+type+","+username+",");
                InputStream input = socket.getInputStream();
                byte[] buffer = new byte[1024];
                int read;
                while((read = input.read(buffer)) != -1) {
                    String out = new String(buffer, 0, read);
                    outData = outData + out;
                };
                socket.close();
            } catch (UnknownHostException unknownHostException) {
                unknownHostException.printStackTrace();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }

            String finalOutData = outData;
            runOnUiThread(new Runnable(){public void run(){String receivedData = finalOutData;
                TextView PatientData = findViewById(R.id.txtInfoPatientAccesss);
                PatientData.setVisibility(View.VISIBLE);
                PatientData.setText(receivedData);
            }});

        }});thread.start();
    }

}