package com.example.aubcovax;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.hbb20.CountryCodePicker;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

//reference to https://github.com/hbb20/CountryCodePickerProject for implementing the country code picker
public class RegisterPatientPage extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register_patient_page);
    }


    //reference to https://github.com/skystone1000/Android-Country-Code-Menu/blob/main/CountryCodeDemo/app/src/main/java/com/example/countrycodedemo/MainActivity.java for the country code picker library

    public final static int SERVICE_PORT = 8000;
    public void SignUp(View view) {
        CountryCodePicker CountryCode =  findViewById(R.id.countrycodepicker);
        CountryCodePicker CountryLocation =  findViewById(R.id.countryname);
        EditText edtusername = findViewById(R.id.editUsernamePatientRegister);
        EditText edtfullname = findViewById(R.id.editFullnamePatient);
        EditText edtpassword1 = findViewById(R.id.textinputedittextpasswordPatientSignUp);
        EditText edtpassword2 = findViewById(R.id.textinputedittextpasswordPatientSignUp2);
        EditText edtemail = findViewById(R.id.editEmailPatientRegister);
        EditText edtphonenumber = findViewById(R.id.editPhoneNumberPatientRegister);
        EditText edtIDnumber = findViewById(R.id.editIDPatientRegister);
        EditText edtCity = findViewById(R.id.editCitySignUp);
        EditText edtBirthDate= (EditText) findViewById(R.id.editBirthDate);
        EditText edtMedicalConditions= (EditText) findViewById(R.id.editMedicalConditions);
        String birthDate = edtBirthDate.getText().toString();
        String username = edtusername.getText().toString();
        String password1 = edtpassword1.getText().toString();
        String password2 = edtpassword2.getText().toString();
        String medicalconditions = edtMedicalConditions.getText().toString();
        String fullname = edtfullname.getText().toString();
        String code = CountryCode.getSelectedCountryCode();
        String country = CountryLocation.getSelectedCountryEnglishName();
        String city = edtCity.getText().toString();
        String location = city + " " + country;
        String phonenumber = "+" + code + " " + edtphonenumber.getText().toString();
        String email = edtemail.getText().toString();
        String IDnumber = edtIDnumber.getText().toString();
        String MedicalConditons = edtMedicalConditions.getText().toString();
        //got help from https://stackoverflow.com/questions/3500197/how-to-display-toast-in-android to display the toast
        if (username.length() == 0 || password1.length() == 0 || password2.length() == 0 || fullname.length() == 0 || phonenumber.length() == 0 || email.length() == 0 || birthDate.length()==0 || IDnumber.length() == 0 || city.length() == 0 || code.length() ==0 || country.length()==0) {
            Toast.makeText(getApplicationContext(), "Missing Required field(s)!", Toast.LENGTH_LONG).show();
            return;
        }
        if (!(password1.equals(password2))) {
            Toast.makeText(getApplicationContext(), "Passwords don't match!", Toast.LENGTH_LONG).show();
            return;
        }

        Thread thread = new Thread(new Runnable(){@Override public void run(){
            String outData = "";
            try{
                Socket socket = new Socket("35.231.177.149", 3389);
                OutputStream output = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(output, true);
                String action = "Sign Up";
                String type = "Patient";
                writer.println(action +","+type+","+username+","+password1+","+fullname+","+birthDate+","+IDnumber+","+phonenumber+","+email+","+location+","+medicalconditions+",");
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
                if("Sign Up Successful".equals(receivedData)){
                    Intent i = new Intent(getApplicationContext(), PatientAccess.class);
                    Bundle bundle = new Bundle();
                    bundle.putString("username",username);
                    i.putExtras(bundle);
                    startActivity(i);
                }
                else if ("This username already exists!".equals(receivedData)) {
                    TextView resultMessage = findViewById(R.id.responseTextPatientSignUp);
                    resultMessage.setText("This username already exists!");
                }
            }});
        }});thread.start();

    }

}
