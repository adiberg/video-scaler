import cv2

cap = cv2.VideoCapture(0)

def rescale_frame(frame, ratio):
    width = int(frame.shape[1] * ratio)
    height = int(frame.shape[0] * ratio)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
    cv2.imwrite(name, resized)

cap.release()
cv2.destroyAllWindows()