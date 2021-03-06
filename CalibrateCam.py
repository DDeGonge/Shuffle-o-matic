from helpers.CameraDriver import Camera, debug_save_img
import helpers.Config as cfg
import cv2

# MANUAL CAL PARAMETERS
EXP_MIN = 70
EXP_MAX = 100
EXP_STEP = 2

def manual_cal():
    c = Camera()
    sweep = list(range(EXP_MIN, EXP_MAX, EXP_STEP))
    imgs = c.exposure_sweep(sweep)

    for e, i in zip(sweep, imgs):
        debug_save_img(i, str(e) + '.jpg')

def auto_cal():
    print("Ensure blank white playing card is being used")
    c = Camera()
    img_raw = c._capture_image(enable_and_disable=True)
    img_greyscale = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
    img_gs_blur = cv2.GaussianBlur(img_greyscale,(5,5),0)
    img_gs_blur_crop = img_gs_blur[cfg.H_MIN:cfg.H_MAX, cfg.W_MIN:cfg.W_MAX]

    debug_save_img(img_gs_blur_crop, 'Shuffle-o-matic/helpers/Card_Imgs/cal.jpg')

    print("Calibration image updated!")

if __name__=='__main__':
    # manual_cal()
    auto_cal()
