"""
MediaPipe Face Detection - Recommended Approach
Simple, fast, and accurate face detection
"""

import cv2 as cv
import mediapipe as mp

# 1. Initialize MediaPipe Face Detection

# accesses mediapipe's face detection module and stores into a variable
mp_face_detection = mp.solutions.face_detection 
# accesses mediapipe's rectangle drawing utilities
mp_drawing = mp.solutions.drawing_utils

# function for face detection in live video feed
def detect_faces_in_video(video_path=None, use_webcam=False):
    """Detect faces in video file or webcam"""
    # Initialize video capture
    if use_webcam:
        cap = cv.VideoCapture(0)  # 0 = default webcam
    else:
        cap = cv.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video")
        return
    
    # Initialize face detection
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5
    ) as face_detection:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            # Detect faces
            results = face_detection.process(rgb_frame)
            
            # Draw detections
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(frame, detection)
            
            # Display frame
            cv.imshow('Face Detection', frame)
            
            # Press 'q' to quit
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv.destroyAllWindows()

def get_face_bbox(image, detection):
    """Extract bounding box coordinates from detection"""
    h, w, _ = image.shape
    bbox = detection.location_data.relative_bounding_box
    
    x = int(bbox.xmin * w)
    y = int(bbox.ymin * h)
    width = int(bbox.width * w)
    height = int(bbox.height * h)
    
    return (x, y, width, height)

def detect_faces_custom_drawing(image_path):
    """Detect faces with custom drawing (more control)"""
    image = cv.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return None
    
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5
    ) as face_detection:
        
        results = face_detection.process(rgb_image)
        
        if results.detections:
            for detection in results.detections:
                # Get bounding box
                x, y, w, h = get_face_bbox(image, detection)
                
                # Draw custom rectangle
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Get confidence score
                confidence = detection.score[0]
                cv.putText(image, f'{confidence:.2f}', (x, y - 10),
                          cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image

# Example usage
if __name__ == "__main__":
    
    # Example 2: Detect faces in webcam (real-time)
    detect_faces_in_video(use_webcam=True)
    
    # Example 3: Detect faces in video file
    # detect_faces_in_video("path/to/your/video.mp4")
    
    print("MediaPipe Face Detection Example")
    print("Uncomment the examples above to test!")

