#include "shuffler.h"

#define Serial SERIAL_PORT_USBVIRTUAL

void setup() 
{ 
  pinMode(dcmotor_power, OUTPUT);
  pinMode(dcmotor_sense, INPUT);

  Serial.begin(250000);
  pixel.begin();
  disp_servo.attach(servo_pin);
  disp_servo.write(135);
  delay(500);
  disp_servo.detach();
}

void loop() 
{
  // Initialize some stuff
  setLEDColor(200,0,0);
  unsigned long startTime_us = micros();
  unsigned long t_elapsed_us;
  stepper_obj s0, s1, s2;
  stepper_obj all_steppers[3] = {s0, s1, s2};
  all_steppers[0].init(s0_step, s0_dir, s0_en, true);
  all_steppers[1].init(s1_step, s1_dir, s1_en, true);
  all_steppers[2].init(s2_step, s2_dir, s2_en, false);
  
  char serial_data[100];
  setLEDColor(100,0,0);

  // Start main response loop
  while(true)
  {
    t_elapsed_us = micros() - startTime_us;
    clear_data(serial_data);
    if(respondToSerial(serial_data)){
      setLEDColor(100,50,0);
      switch (serial_data[0]){
        case 'm':{
          // Move stepper motors
          // m,S_INDEX,S_TARPOS,S_VEL,S_ACCEL
          vector<int32_t> args;
          parse_inputs(serial_data, args);
          all_steppers[args[0]].move_motor(args[1], args[2], args[3]);
          break;
        }
        case 's':{
          // Enable stepper index
          int s_index = (int)serial_data[2] - '0';
          all_steppers[s_index].enable();
          break;
        }
        case 'x':{
          // Disable stepper index
          int s_index = (int)serial_data[2] - '0';
          all_steppers[s_index].disable();
          break;
        }
        case 'z':{
          // Set stepper positions or zero
          // z,S_INDEX,S_TARGET
          vector<int32_t> args;
          parse_inputs(serial_data, args);
          all_steppers[args[0]].overwrite_pos(args[1]);
          break;
        }
        case 'h':{
          // Home steppers
          break;
        }
        case 'e':{
          // Enable dispense motor
          digitalWrite(dcmotor_power, LOW);
          break;
        }
        case 'd':{
          // Disable dispense motor
          digitalWrite(dcmotor_power, HIGH);
          break;
        }
        case 'c':{
          // Dispense one card, with verification
          bool resp = dispense_card();
          if(!resp){
            Serial.println("JAM");
          }
          break;
        }
        case 'b':{
          // Baseline dispense motor current
          cur_baseline = calc_cur_threshold(1000);
          break;
        }
        case 'p':{
          // Get all stepper positions
          Serial.print('p');
          for(uint8_t j = 0; j < 3; j++){
            Serial.print(',');
            Serial.print(all_steppers[j].get_pos());
          }
          Serial.println();
          break;
        }
        case 'f':{
          // Configure stepper object
          // f,S_INDEX,STEPSPERMM*1000
          vector<int32_t> args;
          parse_inputs(serial_data, args);
          all_steppers[args[0]].update_config(args[1]);
          break;
        }
      }
      Serial.println("ok");
      setLEDColor(0,100,0);
    }
  }
  while(true);
}

float calc_cur_threshold(uint16_t n_samples){
  float sum = 0;
  for(uint16_t i = 0; i < n_samples; i++){
    sum += analogRead(dcmotor_sense);
    delay(1);
  }
  return (sum / n_samples);
}

bool dispense_card(){
  disp_servo.attach(servo_pin);
  uint16_t cur_window[cur_window_len];
  float window_mean = 0;
  uint16_t window_i = 0;
  for(uint8_t i = 0; i < cur_window_len; i++){cur_window[i] = 0;}

  bool disp_success = false;
  for(uint8_t i = 0; i < 3; i++){
    disp_servo.write(0);
  
    // Wait until card is detected from dispense motor current spike
    for(uint16_t j = 0; j < 1000; j++){
      cur_window[window_i] = analogRead(dcmotor_sense);
      window_i++;
      window_i %= cur_window_len;
      window_mean = calc_mean(cur_window);
      if(window_mean >= (cur_baseline * cur_thresh_mult)){
        disp_success = true;
        delay(100);
        break;
      }
      delay(1);
    }

    disp_servo.write(135);
    delay(600);

    if(disp_success==true){
      break;
    }
  }  
  disp_servo.detach();

  // check for jam
  if(calc_cur_threshold(100)>(cur_baseline*cur_thresh_mult)){
    return false;
  }
  return disp_success;
}

float calc_mean(uint16_t window[]){
  float sum = 0;
  for(uint16_t i = 0; i < cur_window_len; i++){
    sum += window[i];
  }
  return (sum / cur_window_len);
}

void parse_inputs(char serial_data[100], vector<int32_t> &args){
  char delim = ',';
  uint32_t index = 0;
  vector<char> temp_arg_char;

  // Gets past command char to first data
  while(serial_data[index] != delim){index++;}
  index++;
  while(serial_data[index] != '\0'){
    temp_arg_char.push_back(serial_data[index]);
    index++;
    if(serial_data[index] == delim){
      args.push_back(vtoi(temp_arg_char));
      temp_arg_char.clear();
      index++;
    }
  }
  args.push_back(vtoi(temp_arg_char));
}

int32_t vtoi(vector<char> vec)
{
  int32_t ret = 0;
  int mult = pow(10 , (vec.size()-1));

  for(int i = 0; i <= vec.size(); i++) {
    ret += (vec[i] - '0') * mult;
    mult /= 10;
  }
  return ret;
}

// Read serial messages if exist
bool respondToSerial(char (&serial_data) [100])
{
  uint8_t index = 0;
  if (Serial.available() > 0){
    while (Serial.available() > 0) {
      char newchar = Serial.read();
      if(newchar != '\n'){
        serial_data[index] = newchar;
        index++;
      }
      else{
        break;
      }
    }
    return true;
  }
  return false;
}

void clear_data(char (&serial_data) [100]){
  for(uint16_t i = 0; i < 100; i++){
    serial_data[i]='\0';
    }
}

void setLEDColor(int r, int g, int b)
{
  pixel.setPixelColor(0, pixel.Color(r,g,b)); // Set LED to red
  pixel.show();
}
