import sys
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
#sys.path.insert(0, 'C:\Python\Lib\site-packages')
import zbar

from PIL import Image
import cv2


def main():

    try:
        capture = cv2.VideoCapture()
        capture.open('tcp://192.168.1.1:5555')
        print "QRReader: Capture success!"
    except:
        print "QRReader: Failed!"

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)


        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        # Prints data from image.
        for decoded in zbar_image:
            print(decoded.data)


if __name__ == "__main__":
    main()
