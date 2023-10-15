import mediapipe as mp
import cv2
import numpy as np
import os
from datetime import datetime
import time

def main(letter: str, nextLetter: str) -> None:
    current =  datetime.now()
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(1)

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands: 
        bigArray = np.load(f"mediapipe approach/landmarkTrainData/{letter}.npy").tolist()
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # image = cv2.flip(image, 1)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # labels for the data collector to actually know what they're collecting
            cv2.putText(image, f"Recording letter {letter.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"NEXT LETTER: {nextLetter.upper() if letter != 'z' else 'done'}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            #actually grabbing the points  
            if results.multi_hand_landmarks:
                handArray = np.empty((0,3), float)
                for hand in results.multi_hand_landmarks:
                    for point in mp_hands.HandLandmark:
                        handArray = np.vstack((handArray,[hand.landmark[point].x,hand.landmark[point].y,hand.landmark[point].z]))
                        
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                            )
                bigArray.append(handArray)

            cv2.imshow('Hand Tracking', image)

            if (datetime.now() - current).total_seconds() > 15 or cv2.waitKey(10) & 0xFF == ord('q'):
                bigArray = np.array(bigArray)
                print(bigArray.shape)
                break

    cap.release()
    cv2.destroyAllWindows()
    absolute_path = "mediapipe approach\landmarkTrainData"
    os.makedirs(absolute_path, exist_ok=True)
    file_path = os.path.join(absolute_path, f'{letter}.npy')
    np.save(file_path, bigArray)

allalphabet=['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']

for counter, letter in enumerate(allalphabet):
    print(f"Recording letter {letter} ({counter+1}/{len(allalphabet)})")
    main(letter, allalphabet[counter+1] if counter+1 < len(allalphabet) else 'done')
    print(f"Your next letter is {allalphabet[counter+1] if counter+1 < len(allalphabet) else 'done'}")
    time.sleep(8)