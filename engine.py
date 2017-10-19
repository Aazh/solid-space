from detection_functions import detector
from movement_functions import liigu
import cv2
try:
    detectors = []
    for i in range(3):
        looker = detector('colorConfig{0}.txt'.format(i), i)
        detectors.append(looker)

    cap = cv2.VideoCapture(0)

    cv2.namedWindow("k")

    while True:
        ret, mask, x, y = detectors[0].detect(cap)
        k = cv2.waitKey(5) & 0xFF

        if x < 300:
            liigu(0, 0, 1)

        if x > 400:
            liigu(0, 0, -1)

        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
except:
    cv2.destroyAllWindows()
    cap.release()