package com.example.aubcovax;

import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class PatientAccess extends AppCompatActivity {
    Bundle bundle = getIntent().getExtras();
    String username = bundle.getString("username");
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_access);
        Thread thread = new Thread(new Runnable(){@Override public void run(){
            String outData = "";
            try{
                Socket socket = new Socket("35.231.177.149", 3389);
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                String action = "Search";
                String type = "Patient";
                writer.println(action +"$"+type+"$"+username+"$");
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
    public void sendCertificate(View view) {
        Thread thread = new Thread(new Runnable(){@Override public void run(){
            String outData = "";
            try{
                Socket socket = new Socket("35.231.177.149", 3389);
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                String action = "Send Certificate";
                String type = "Patient";
                writer.println(action +"$"+type+"$"+username+"$");
                InputStream input = socket.getInputStream();
                ContextWrapper contextWrapper = new ContextWrapper(getApplicationContext());
                File directory = contextWrapper.getDir(getFilesDir().getName(), Context.MODE_PRIVATE);
                File file = new File(directory,"Vaccination Certificate.pdf");
                byte[] buffer = new byte[1024];
                int read;
                FileOutputStream fos = new FileOutputStream("Vaccination Certificate.pdf",true);
                while((read = input.read(buffer)) != -1) {
                    String data = new String(buffer, 0, read);
                    fos.write(data.getBytes());
                };
                fos.close();
                socket.close();
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setDataAndType(Uri.fromFile(file),"application/pdf");
                intent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
                startActivity(intent);
            } catch (UnknownHostException unknownHostException) {
                unknownHostException.printStackTrace();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }

            String finalOutData = outData;
            runOnUiThread(new Runnable(){public void run(){String receivedData = finalOutData;
                if("Certificate Unavailable".equals(receivedData)){
                    TextView resultMessage = findViewById(R.id.responseTextPersonnel);
                    resultMessage.setText("This username doesn't exist");
                }
                else {

                }
            }});
        }});thread.start();}

}