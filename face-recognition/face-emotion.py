import numpy as np
import cv2 as cv
from deepface import DeepFace

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

emotion_model = DeepFace.build_model('Emotion')
emotion_labels = {'angry': -1, 'disgust': -1, 'fear': -1, 'happy': 1, 'sad': -1, 'surprise': 0, 'neutral': 0}
# yolov5 = torch.hub.load('ultralytics/yolov5', 'yolov5n')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # face = None
    # detection = yolov5(frame[:, :, ::-1]).xyxy[0]

    # for obj in detection:
    #     if obj[-1] == 0:
    #         print("DETECTED PERSON")
    #         bbox = list(map(int, [obj[0], obj[1], obj[2], obj[3]]))
    #         confidence = obj[4]
    
    #         face = frame[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    #         cv.imshow("face", face)
    #         break

    # if face.any():
    obj = DeepFace.analyze(frame, actions = ['emotion'], models={'emotion': emotion_model}, enforce_detection=False, detector_backend='ssd')
    box = obj['region']
    emotion = obj['dominant_emotion']
    confidence = obj['emotion'][emotion]

    adjusted_scores = [emotion_labels[feeling] * obj['emotion'][feeling] / 100 for feeling in emotion_labels]
    score = sum(adjusted_scores)

    cv.rectangle(frame, (box['x'], box['y']), (box['x'] + box['w'], box['y'] + box['h']), (0, 255, 0), 2)

    font = cv.FONT_HERSHEY_SIMPLEX

    cv.putText(frame, f'{emotion}-{confidence:.2f}-{score:.2f}', (50, 100), font, 1, (0, 0, 255), 2, cv.LINE_4)
    cv.imshow('ORIGINAL_VIDEO', frame)

    
    # else:
        # print("Bring face into view")

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # Display the resulting frame

    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()