#include <Adafruit_NeoPixel.h>
#include <Servo.h>
#include <vector>
#include <algorithm>

#define servo_pin 0
#define dcmotor_power 9
#define dcmotor_sense A4

#define s0_en 13
#define s0_step 5
#define s0_dir 6
#define s1_en 1
#define s1_step 10
#define s1_dir 11
#define s2_en 99
#define s2_step 99
#define s2_dir 99

Adafruit_NeoPixel pixel = Adafruit_NeoPixel(1, 8, NEO_GRB + NEO_KHZ800);
Servo disp_servo;

using namespace std;

int cur_window_len = 15;
float cur_thresh_mult = 1.5;
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
