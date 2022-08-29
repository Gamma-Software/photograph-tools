import cv2
import os
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
filenames = next(os.walk("data/images/"), (None, None, []))[2]  # [] if no file
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
  for idx, f in enumerate(filenames):
    print()
    print(f)
    image = cv2.imread('data/images/'+f)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw face detections of each face.
    if not results.detections:
      continue
    annotated_image = image.copy()
    i = 0
    for detection in results.detections:
      i += 1
      #print('Nose tip:')
      #print(mp_face_detection.get_key_point(
      #    detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
      mp_drawing.draw_detection(annotated_image, detection)
    print("Number of people:" + str(i))
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)