#include <Adafruit_NeoPixel.h>
#include <Servo.h>
#include <vector>
#include <algorithm>

#define servo_pin 4
#define dcmotor_power A5
#define dcmotor_sense A4

#define s0_en A1
#define s0_step 11
#define s0_dir 12
#define s1_en A2
#define s1_step 9
#define s1_dir 10
#define s2_en A3
#define s2_step 5
#define s2_dir 6

Adafruit_NeoPixel pixel = Adafruit_NeoPixel(1, 8, NEO_GRB + NEO_KHZ800);
Servo disp_servo;

using namespace std;

int cur_window_len = 20;
float cur_thresh_mult = 1.7;
int cur_baseline = 0;

struct stepper_obj
{
  public:
  void init(int s_pin, int d_pin, int e_pin, bool reverse);
  void enable();
  void disable();
  void set_dir(bool dir);
  void move_motor(int32_t s_target, int32_t v_max, int32_t accel);
  void overwrite_pos(int32_t newpos);
  void update_config(int32_t s_per_mm_new);
  int32_t get_pos();

  private:
  int step_pin;
  int dir_pin;
  int en_pin;
  int32_t pos;
  int8_t invert_dir;
  float steps_per_mm;
};

struct global_config
{
  public:
  uint16_t step_len_us;               // a
  uint8_t servo_min_pwm;              // b
  uint8_t servo_max_pwm;              // c
  uint16_t dispense_timeout_ms;       // d
  uint16_t current_detect_freq_hz;    // e
  uint16_t current_detect_window_ms;  // f
  float current_threshold_factor;     // g
  uint16_t servo_return_time_ms;      // h
  uint8_t dispense_max_attempts;      // i
};
