void stepper_obj::init(int s_pin, int d_pin, int e_pin, bool reverse)
{
  step_pin = s_pin;
  dir_pin = d_pin;
  en_pin = e_pin;
  pinMode(step_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(en_pin, OUTPUT);
  digitalWrite(en_pin, HIGH);
  digitalWrite(step_pin, LOW);
  digitalWrite(dir_pin, LOW);
  pos = 0;
  if(reverse){
    invert_dir = -1;
  }
  else{
    invert_dir = 1;
  }
}

void stepper_obj::enable()
{
  digitalWrite(en_pin, LOW);
}

void stepper_obj::disable()
{
  digitalWrite(en_pin, HIGH);
}

void stepper_obj::set_dir(bool dir)
{
  if(dir){
    digitalWrite(dir_pin, HIGH);
  }
  else{
    digitalWrite(dir_pin, LOW);
  }
}

void stepper_obj::overwrite_pos(int32_t newpos)
{
  pos = newpos;
}

void stepper_obj::update_config(int32_t s_per_mm_new)
{
  steps_per_mm = s_per_mm_new;
  steps_per_mm /= 1000;
}

void stepper_obj::move_motor(int32_t s_target, int32_t v_max, int32_t accel)
{
  // Set stepper turn direction
  if(invert_dir*(s_target - pos) < 0){
    set_dir(false);
  }
  else{
    set_dir(true);
  }

  // Calculate some motion paramters
  int count_sign = (s_target - pos) / abs(s_target - pos);
  int n_steps = abs(s_target - pos);
  float move_dist = n_steps;
  move_dist /= steps_per_mm;
  float step_size_mm = 1 / steps_per_mm;
  float accel_dist = (pow(v_max, 2) / (2 * accel));

  // Determine if move will be all accelerations or if it will have plateau
  int32_t t_min = 0;
  int32_t accel_steps = 0;
  if((2 * accel_dist) < move_dist)
  {
    t_min = (1000000 * step_size_mm) / v_max;
    accel_steps = steps_per_mm * accel_dist;
  }
  else
  {
    accel_steps = floor(n_steps / 2);
  }

  int32_t last_step = micros();
  int32_t t_start = last_step;
  int32_t next_target_delta_us = 0;
  float v_now = 0;

  // Accelerate and remember ramp up timings
  vector<uint16_t> timings;
  for(int i = 0; i < accel_steps; i++)
  {
    next_target_delta_us = solve_for_t_us(v_now, accel, step_size_mm);
    timings.push_back(next_target_delta_us);
    onestep(step_pin);
    pos += (1 * count_sign);
    dwell_until_time(last_step + next_target_delta_us);
    v_now = ((last_step - t_start) * accel) / 1000000;
    last_step += next_target_delta_us;
  }

  // Plateau
  int plat_steps = n_steps - (2 * accel_steps);
  for(int i = 0; i < plat_steps; i++)
  {
    onestep(step_pin);
    pos += (1 * count_sign);
    dwell_until_time(last_step + t_min);
    last_step += t_min;
  }

  // Decelerate
  for(int i = accel_steps - 1; i >= 0; i--)
  {
    onestep(step_pin);
    pos += (1 * count_sign);
    dwell_until_time(last_step + timings[i]);
    last_step += timings[i];
  }
}

void dwell_until_time(int32_t tar_time)
{
  while(micros() < tar_time);
}

int32_t stepper_obj::get_pos()
{
  return pos;
}

int32_t solve_for_t_us(float v, float a, float d){
  float t = -v;
  if(v >= 0){
    t += sqrt(pow(v, 2) + 2 * a * d);
    t /= a;
  }
  else{
    t -= sqrt(pow(v, 2) - 2 * a * d);
    t /= a;
  }
  t *= 1000000;
  t = (int32_t)(t - 1); // Subtract 1 to account for the time of the step pulse
  if(t > 50000){
    return 50000;
  }
  return t;
}

void onestep(int pin){
  digitalWrite(pin, HIGH);
  delayMicroseconds(1);
  digitalWrite(pin, LOW);
}
