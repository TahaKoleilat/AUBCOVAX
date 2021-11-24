package com.example.aubcovax;

import android.content.Intent;
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

public class PersonnelLogin extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_personnel_login);
    }

    public void sendPersonnel(View view) {
        EditText edtusername = findViewById(R.id.editUsernamePersonnel);
        EditText edtpassword = findViewById(R.id.textinputedittextpasswordPersonnel);
        String username = edtusername.getText().toString();
        String password = edtpassword.getText().toString();
        //got help from https://stackoverflow.com/questions/3500197/how-to-display-toast-in-android to display the toast
        if (username.length() == 0 && password.length() != 0) {
            Toast.makeText(getApplicationContext(), "Please enter a username", Toast.LENGTH_LONG).show();
            return;
        } else if (password.length() == 0 && username.length() != 0) {
            Toast.makeText(getApplicationContext(), "Please enter a password", Toast.LENGTH_LONG).show();
            return;
        } else if (password.length() == 0 && username.length() == 0) {
            Toast.makeText(getApplicationContext(), "Please enter a username and a password", Toast.LENGTH_LONG).show();
            return;
        }
            Thread thread = new Thread(new Runnable(){@Override public void run(){
                String outData = "";
                try{
                    Socket socket = new Socket("35.231.177.149", 3389);
                    OutputStream output = socket.getOutputStream();
                    PrintWriter writer = new PrintWriter(output, true);
                    String action = "Sign In";
                    String type = "Medical Personnel";
                    writer.println(action +","+type+","+username+","+password+",");
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
                    if("LogIn Successful".equals(receivedData)){
                        Intent i = new Intent(getApplicationContext(), PersonnelAccess.class);
                        startActivity(i);
                    }
                    else if ("This username doesn't exist".equals(receivedData)) {
                        TextView resultMessage = findViewById(R.id.responseTextPersonnel);
                        resultMessage.setText("This username doesn't exist");
                    }
                    else if ("Incorrect Password".equals(receivedData)) {
                        TextView resultMessage = findViewById(R.id.responseTextPersonnel);
                        resultMessage.setText("Incorrect Password");
                    }
                    // Closing the socket connection with the server
                }});
            }});thread.start();}
}