import cv2
import mediapipe as mp
import util
import pyautogui
import random
from pynput.mouse import Button,Controller
mouse = Controller()

screen_width,screen_height = pyautogui.size()
mphands = mp.solutions.hands
hands = mphands.Hands(
    static_image_mode =False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands = 1
)
def find_finger_tip(result):
    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x*screen_width)
        y = int(index_finger_tip.y*screen_height)
        pyautogui.moveTo(x,y)

def left_click(landmark_list,thumb_index_distance):
    return (util.get_angle(landmark_list[5],landmark_list[6],landmark_list[8])<50 and 
            util.get_angle(landmark_list[9],landmark_list[10],landmark_list[12])>90 and 
            thumb_index_distance > 50)
def right_click(landmark_list,thumb_index_distance):
    return (util.get_angle(landmark_list[9],landmark_list[10],landmark_list[12])<50 and 
            util.get_angle(landmark_list[5],landmark_list[6],landmark_list[8])>90 and 
            thumb_index_distance > 50)
def double_click(landmark_list,thumb_index_distance):
    return (util.get_angle(landmark_list[9],landmark_list[10],landmark_list[12])<50 and 
            util.get_angle(landmark_list[5],landmark_list[6],landmark_list[8])<90 and 
            thumb_index_distance > 50)
def screenshot(landmark_list,thumb_index_distance):
    return (util.get_angle(landmark_list[5],landmark_list[6],landmark_list[8])<50 and 
            util.get_angle(landmark_list[9],landmark_list[10],landmark_list[12])<90 and 
            thumb_index_distance < 50)


def detect_gestures(frame,landmark_list,result):
    if(len(landmark_list))>=21:
        index_finger_tip =  find_finger_tip(result)
        thumb_index_distance = util.get_distance([landmark_list[4],landmark_list[5]])

        if thumb_index_distance < 50 and util.get_angle(landmark_list[5],landmark_list[6],landmark_list[8])>90:
            move_mouse(index_finger_tip)
        elif left_click(landmark_list,thumb_index_distance):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame,"Left-Click",(50,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),1)
        elif right_click(landmark_list,thumb_index_distance):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame,"Right-Click",(50,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),1)

        elif double_click(landmark_list,thumb_index_distance):
             pyautogui.doubleClick()
             cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif screenshot(landmark_list,thumb_index_distance):
             im1 = pyautogui.screenshot()
             label = random.randint(1,1000)
             im1.save(f"my_screensot{label}.png")
             cv2.putText(frame, "screenshot-taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)




def main():
    cap = cv2.VideoCapture(0)
    mpdraw = mp.solutions.drawing_utils

    try:
        while cap.isOpened():
            ret,frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame,1)
            frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            result = hands.process(frameRGB)

            landmark_list = [] 
            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                mpdraw.draw_landmarks(frame,hand_landmarks,mphands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x,lm.y))

            detect_gestures(frame,landmark_list,result)
            cv2.imshow("WebCam-FeeD",frame)
            if cv2.waitKey(1) & 0xff==ord('q'):
                break 

    finally:
        cap.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    main()