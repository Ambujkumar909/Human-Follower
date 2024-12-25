import cv2
import mediapipe as mp
from collections import deque


mppose = mp.solutions.pose
pose = mppose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpdraw = mp.solutions.drawing_utils


prev_shoulder_x = None
prev_shoulder_y = None
prev_hip_x = None
prev_hip_y = None


direction_queue = deque(maxlen=8)
stable_direction = "Stable"

# Dead zone threshold
DEAD_ZONE = 0.005

# Start capturing video
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    current_direction = "Stable"

    if results.pose_landmarks:

        mpdraw.draw_landmarks(img, results.pose_landmarks, mppose.POSE_CONNECTIONS)


        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mppose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mppose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mppose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mppose.PoseLandmark.RIGHT_HIP]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_center_x = (left_hip.x + right_hip.x) / 2
        hip_center_y = (left_hip.y + right_hip.y) / 2

        if prev_shoulder_x is not None and prev_shoulder_y is not None:
            dx_shoulder = shoulder_center_x - prev_shoulder_x
            dy_shoulder = shoulder_center_y - prev_shoulder_y


            print(f"dx_shoulder: {dx_shoulder}, dy_shoulder: {dy_shoulder}")

            if abs(dx_shoulder) > DEAD_ZONE or abs(dy_shoulder) > DEAD_ZONE:
                if abs(dx_shoulder) > abs(dy_shoulder):
                    current_direction = "Moving Right (Shoulder)" if dx_shoulder > 0 else "Moving Left (Shoulder)"
                else:
                    current_direction = "Moving Forward (Shoulder)" if dy_shoulder > 0 else "Moving Backward (Shoulder)"
            else:
                current_direction = "Stable (Shoulder)"

        elif prev_hip_x is not None and prev_hip_y is not None:
            dx_hip = hip_center_x - prev_hip_x
            dy_hip = hip_center_y - prev_hip_y


            print(f"dx_hip: {dx_hip}, dy_hip: {dy_hip}")

            if abs(dx_hip) > DEAD_ZONE or abs(dy_hip) > DEAD_ZONE:
                if abs(dx_hip) > abs(dy_hip):
                    current_direction = "Moving Right (Hip)" if dx_hip > 0 else "Moving Left (Hip)"
                else:
                    current_direction = "Moving Forward (Hip)" if dy_hip > 0 else "Moving Backward (Hip)"
            else:
                current_direction = "Stable (Hip)"


        prev_shoulder_x, prev_shoulder_y = shoulder_center_x, shoulder_center_y
        prev_hip_x, prev_hip_y = hip_center_x, hip_center_y


        direction_queue.append(current_direction)


        if len(direction_queue) == direction_queue.maxlen:
            most_common_direction = max(set(direction_queue), key=direction_queue.count)
            if direction_queue.count(most_common_direction) > len(direction_queue) // 2:
                stable_direction = most_common_direction


    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Direction: {stable_direction}", (10, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)


    cv2.imshow("Human Follower", img)


    if cv2.waitKey(1) & 0xFF == ord('a'):
        break


cap.release()
cv2.destroyAllWindows()
