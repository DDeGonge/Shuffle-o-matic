from helpers.CameraDriver import Camera
import helpers.Config as cfg

def main():
    c = Camera()
    c.start_camera()
    card = c.read_card()
    print(card.rank, card.suit)
    c.stop_camera()

if __name__=='__main__':
    main()
