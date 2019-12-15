package com.example.telemetry;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import android.hardware.SensorEvent;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    public SensorManager sensorManager;
    private Sensor accelerometer;

//    private ArrayList<Double> xCollect, yCollect;

    //values will be changed in main thread(UI thread) as accelerometer reading changes
    //the newest data will be extracted and sent to server(BRIO board) through tcp connection in the client thread
    private String values = "0 0";
    private client tcp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_FASTEST);

//        xCollect = new ArrayList<>();
//        yCollect = new ArrayList<>();
//        for(int i = 0; i < 10; i++){
//            xCollect.add(0.0);
//            yCollect.add(0.0);
//        }
//        values = round(mean(xCollect)) + " " + round(mean(yCollect));

        //button will change between "start" and "stop"
        final Button control = findViewById(R.id.control);
        control.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Code here executes on main thread after user presses button
                if(tcp == null){
                    String ip = getIp();
                    tcp = new client(ip);
                    tcp.start();
                    control.setText("stop");
                }else if(tcp.terminate == true){
                    String ip = getIp();
                    tcp = new client(ip);
                    tcp.start();
                    control.setText("stop");
                }else{
                    tcp.terminate = true;
                    control.setText("start");
                }
            }
        });

    }

    @Override
    public void onBackPressed(){
        //app will not change when back button is pressed
    }

    String getIp(){
        EditText ip = (EditText)findViewById(R.id.ip);
        String ipAdr = ip.getText().toString();
        if(ipAdr.length() == 0){
            ipAdr = "10.8.0.5";
        }
        return ipAdr;
    }


    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // can be safely ignored for this demo
    }

    @Override
    public final void onSensorChanged(SensorEvent event) {

        //raw accelerometer readings
        double xAccel = event.values[0];
        double yAccel = event.values[1];
        double zAccel = event.values[2];

        //get radians from raw accelerometer data
        double xRad = Math.atan(yAccel/Math.sqrt(Math.pow(xAccel,2) + Math.pow(zAccel,2)));
        double yRad = -1 * Math.atan(xAccel/Math.sqrt(Math.pow(yAccel,2) + Math.pow(zAccel,2)));

        //convert radians into degrees
        double xDeg = xRad * (180.0/Math.PI) ;
        double yDeg = yRad * (180.0/Math.PI);

//        xCollect.remove(0);
//        xCollect.add(xDeg);
//        yCollect.remove(0);
//        yCollect.add(yDeg);
//        values = round(mean(xCollect)) + " " + round(mean(yCollect));

        //update values
        values = round(xDeg) + " " + round(yDeg);
    }

    String round(double val)
    {
        return String.format("%.2f", val);
    }

//    double mean(ArrayList<Double> arr){
//        double sum = 0;
//        for(int i = 0; i < arr.size(); i++){
//            sum += arr.get(i);
//        }
//        return sum / arr.size();
//    }



    private class client extends Thread{
        //use terminate to check if the thread is still running or to stop the thread
        boolean terminate = false;
        Socket socket;
        String ip;
        int port = 8080;

        public client(String ip){
            this.ip = ip;
        }

        @Override
        public void run() {
            try {
                Log.i("ownTag", "ip: " + ip + "   port: " + port);
                socket = new Socket(ip, port);
                Log.i("ownTag","built socket");
                PrintWriter send = new PrintWriter(socket.getOutputStream());
                BufferedReader recieve = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                //use control as a thresh hold to wait for the artificial ACK from the server
                boolean control = true;
                Log.i("ownTag", "going into while");
                while (true) {
                    if(terminate){
                        Log.i("ownTag","terminate");
                        break;
                    }
                    if (control) {
                        send.print(values);
                        send.flush();
                        control = false;
                    } else {
                        int read = recieve.read();
                        if (read == -1) {
                            break;
                        }
                        control = true;
                    }
                }
                Log.i("ownTag","close 1");
                socket.close();

            } catch (Exception e) {
                Log.i("ownTag","exception 1");
                Log.i("ownTag", e.toString());
                try {
                    Log.i("ownTag","close 2");
                    socket.close();
                } catch (Exception e1) {
                    Log.i("ownTag", "exception 2");
                    Log.i("ownTag",e1.toString());
                }
            }
            terminate = true;
            //can only change values of contents in main thread(UI thread)
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Button control = findViewById(R.id.control);
                    control.setText("start");
                }
            });
            Log.i("ownTag","out");
        }
    }

}