package com.example.aubcovax;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class PersonnelAccess extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_personnel_access);
    }
    public void PersonnelSearch(View view) {
        EditText edtSearchField = findViewById(R.id.searchDataBasePersonnel);
        String searchobject = edtSearchField.getText().toString();
        Thread thread = new Thread(new Runnable(){@Override public void run(){
            String outData = "";
            try{
                Socket socket = new Socket("35.231.177.149", 3389);
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                String action = "Search";
                String type = "Personnel";
                writer.println(action +"$"+type+"$"+searchobject+"$");
                InputStream input = socket.getInputStream();
                byte[] buffer = new byte[1024];
                int read;
                while((read = input.read(buffer)) != -1) {
                    String out = new String(buffer, 0, read);
                    outData = outData + out;
                }
                socket.close();
            } catch (UnknownHostException unknownHostException) {
                unknownHostException.printStackTrace();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }

            String finalOutData = outData;
            runOnUiThread(new Runnable(){public void run(){String receivedData = finalOutData;
                if("This patient doesn't exist!".equals(receivedData)){
                    Toast.makeText(getApplicationContext(), "This Person doesn't exist", Toast.LENGTH_LONG).show();
                    return;
                }
                else {
                    TextView datatext = findViewById(R.id.txtsearchPatientPersonnel);
                    datatext.setVisibility(View.VISIBLE);
                    datatext.setText(receivedData);
                }
                // Closing the socket connection with the server
            }});

        }});thread.start();
}
    public void Book(View view) {
        EditText edtSearchField = findViewById(R.id.searchDataBasePersonnel);
        String searchobject = edtSearchField.getText().toString();
        Thread thread = new Thread(new Runnable(){@Override public void run(){
            String outData = "";
            try{
                Socket socket = new Socket("35.231.177.149", 3389);
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                String action = "Book";
                String type = "Personnel";
                writer.println(action +"$"+type+"$"+searchobject+"$");
                InputStream input = socket.getInputStream();
                byte[] buffer = new byte[1024];
                int read;
                while((read = input.read(buffer)) != -1) {
                    String out = new String(buffer, 0, read);
                    outData = outData + out;
                }
                socket.close();
            } catch (UnknownHostException unknownHostException) {
                unknownHostException.printStackTrace();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }
            String finalOutData = outData;
            runOnUiThread(new Runnable(){public void run(){String receivedData = finalOutData;
                if("This patient already took Dose 2!".equals(receivedData)){
                    Toast.makeText(getApplicationContext(), "This patient already took Dose 2!", Toast.LENGTH_LONG).show();
                    return;
                }
                else if("This patient didn't take Dose 1 yet!".equals(receivedData)){
                    Toast.makeText(getApplicationContext(), "This patient didn't take Dose 1 yet!", Toast.LENGTH_LONG).show();
                    return;
                }
                else {
                    TextView datatext = findViewById(R.id.txtsearchPatientPersonnel);
                    datatext.setText(receivedData);
                    Toast.makeText(getApplicationContext(), "Booked Dose 2 Successfully!", Toast.LENGTH_LONG).show();
                }
                return;
            }});

        }});thread.start();
    }
}