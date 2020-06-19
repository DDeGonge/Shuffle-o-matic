from helpers.CameraDriver import Camera
from helpers.CardDetector import debug_save_img

EXP_MIN = 70
EXP_MAX = 100
EXP_STEP = 2

def main():
    c = Camera()
    sweep = list(range(EXP_MIN, EXP_MAX, EXP_STEP))
    imgs = c.exposure_sweep(sweep)

    for e, i in zip(sweep, imgs):
        debug_save_img(i, str(e) + '.jpg')


if __name__=='__main__':
    main()
