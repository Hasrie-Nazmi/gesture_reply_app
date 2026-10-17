import cv2
import mediapipe as mp
from kivy.graphics.texture import Texture


class GestureCameraProcessor:
    def __init__(self, max_num_hands=1):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.capture = None

    def start_camera(self, camera_index=0):
        """Starts the OpenCV video capture."""
        if not self.capture or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(camera_index)

    def stop_camera(self):
        """Releases the OpenCV video capture."""
        if self.capture:
            self.capture.release()
            self.capture = None

    def process_frame(self, callback_on_gesture=None):
        """
        Reads a frame, runs MediaPipe, draws landmarks, 
        evaluates gestures, and returns a Kivy Texture.
        """
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 1)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)

                detected_gesture = None
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                        )
                        detected_gesture = self._evaluate_gestures(
                            hand_landmarks.landmark)

                        if callback_on_gesture and detected_gesture:
                            callback_on_gesture(detected_gesture)

                frame = cv2.flip(frame, 0)
                buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).tobytes()

                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

                return texture, detected_gesture
        return None, None

    def _evaluate_gestures(self, landmarks):
        """Evaluates hand landmarks against gesture dictionary rules."""
        gestures = {
            "gest_0": {
                "index_down": landmarks[8].y > landmarks[6].y,
                "middle_down": landmarks[12].y > landmarks[10].y,
                "ring_down": landmarks[16].y > landmarks[14].y,
                "pinky_down": landmarks[20].y > landmarks[18].y
            },
            "gest_1": {
                "index_up": landmarks[8].y < landmarks[6].y,
                "middle_down": landmarks[12].y > landmarks[10].y,
                "ring_down": landmarks[16].y > landmarks[14].y,
                "pinky_down": landmarks[20].y > landmarks[18].y
            },
            "gest_2": {
                "index_up": landmarks[8].y < landmarks[6].y,
                "middle_up": landmarks[12].y < landmarks[10].y,
                "ring_down": landmarks[16].y > landmarks[14].y,
                "pinky_down": landmarks[20].y > landmarks[18].y
            },
            "gest_3": {
                "index_up": landmarks[8].y < landmarks[6].y,
                "middle_up": landmarks[12].y < landmarks[10].y,
                "ring_up": landmarks[16].y < landmarks[14].y,
                "pinky_down": landmarks[20].y > landmarks[18].y
            },
            "gest_5": {
                "thumb_out": abs(landmarks[4].x - landmarks[5].x) > 0.05,
                "index_up": landmarks[8].y < landmarks[6].y,
                "middle_up": landmarks[12].y < landmarks[10].y,
                "ring_up": landmarks[16].y < landmarks[14].y,
                "pinky_up": landmarks[20].y < landmarks[18].y
            },
            "gest_4": {
                "index_up": landmarks[8].y < landmarks[6].y,
                "middle_up": landmarks[12].y < landmarks[10].y,
                "ring_up": landmarks[16].y < landmarks[14].y,
                "pinky_up": landmarks[20].y < landmarks[18].y
            }
        }

        for gesture_name, conditions in gestures.items():
            if all(conditions.values()):
                return gesture_name
        return None
