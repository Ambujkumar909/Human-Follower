Human Follower

This project uses MediaPipe's Pose module to track human movement and determine the direction in which the tracked human is moving. The application continuously analyzes video frames from a camera feed to estimate pose landmarks and classify directional movement based on changes in shoulder and hip positions.

Features

Real-time Pose Estimation: Uses MediaPipe's Pose module to track human landmarks in live video.

Direction Tracking: Determines whether the human is moving forward, backward, left, or right.

Stabilization: Implements a queue to smooth out rapid directional changes and provides a stable directional output.

Dead Zone Threshold: Ignores minor movements to avoid noise in tracking.

Live Video Display: Shows the camera feed with overlaid pose landmarks and direction status.

Requirements

Python 3.7 or higher

OpenCV

MediaPipe

Installation

Clone the repository or download the script file:

git clone <repository-link>
cd <repository-folder>

Install the required Python packages:

pip install opencv-python mediapipe

How It Works

Pose Landmarks Detection:

MediaPipe's Pose module identifies key human landmarks (e.g., shoulders and hips) in the video feed.

Direction Calculation:

The script calculates the average position of the left and right shoulders and hips to determine movement.

Changes in these positions between frames are used to classify direction:

Forward: Shoulder/hip moves up.

Backward: Shoulder/hip moves down.

Left: Shoulder/hip moves left.

Right: Shoulder/hip moves right.

Stabilization:

A deque (queue) of recent directional changes is maintained.

The most common direction in the queue is selected as the stable output.

Output Display:

Pose landmarks and the stable direction are displayed in real time on the video feed.

Code Highlights

Pose Initialization:

mppose = mp.solutions.pose
pose = mppose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

Direction Calculation:

dx_shoulder = shoulder_center_x - prev_shoulder_x
dy_shoulder = shoulder_center_y - prev_shoulder_y

if abs(dx_shoulder) > DEAD_ZONE or abs(dy_shoulder) > DEAD_ZONE:
    if abs(dx_shoulder) > abs(dy_shoulder):
        current_direction = "Moving Right (Shoulder)" if dx_shoulder > 0 else "Moving Left (Shoulder)"
    else:
        current_direction = "Moving Forward (Shoulder)" if dy_shoulder > 0 else "Moving Backward (Shoulder)"

Stabilization:

direction_queue.append(current_direction)
if len(direction_queue) == direction_queue.maxlen:
    most_common_direction = max(set(direction_queue), key=direction_queue.count)
    if direction_queue.count(most_common_direction) > len(direction_queue) // 2:
        stable_direction = most_common_direction

Usage

Run the script:

python human_follower.py

The script will open a video feed window showing:

Pose landmarks overlaid on the detected person.

The stable direction displayed at the top left of the window.

Press the A key to exit the program.

Future Improvements

Obstacle Detection: Integration with object detection models (e.g., YOLO) to identify obstacles.

Path Mimicking: Implement logic for mimicking human path while avoiding obstacles.

Enhanced Stabilization: Use advanced filtering techniques for smoother direction tracking.

Performance Optimization: Optimize for deployment on devices like Raspberry Pi.

Contributing

Feel free to submit issues or pull requests for any improvements or feature additions.

License

This project is licensed under the MIT License. See LICENSE for details.

