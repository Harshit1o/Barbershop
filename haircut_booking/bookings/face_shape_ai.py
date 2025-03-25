import numpy as np
import cv2
import dlib
from sklearn.cluster import KMeans
import math
from math import degrees
import os
from django.conf import settings

# Dynamically resolve the file paths
face_cascade_path = os.path.join(settings.BASE_DIR, 'bookings', 'haarcascade_frontalface_default (1).xml')
predictor_path = os.path.join(settings.BASE_DIR, 'bookings', 'shape_predictor_68_face_landmarks.dat')
faceCascade = cv2.CascadeClassifier(face_cascade_path)
predictor = dlib.shape_predictor(predictor_path)

# Map of face shapes to recommended hairstyles
hairstyle_recommendations = {
    "Square": ["Short Pompadour", "Side Part", "Undercut"],
    "Round": ["Angular Fringe", "High Volume Top", "Flat Top"],
    "Triangle": ["Buzz Cut", "Textured Crop", "Side-Swept"],
    "Diamond": ["Comb Over", "Faux Hawk", "Quiff"],
    "Rectangular": ["Crew Cut", "Pompadour", "Short Textured"],
    "Oblong": ["Side Part", "Fringe", "Layered Top"],
    "Unknown": ["Consult a stylist for a custom recommendation."]
}

def detect_face_and_recommend(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        dlib_rect = dlib.rectangle(x, y, x + w, y + h)
        landmarks = predictor(frame, dlib_rect)
        landmarks_array = np.matrix([[p.x, p.y] for p in landmarks.parts()])

        # Compute facial dimensions
        line1 = w  # Forehead width (already captured)
        line2 = np.linalg.norm([landmarks_array[15, 0] - landmarks_array[1, 0], landmarks_array[15, 1] - landmarks_array[1, 1]])
        line3 = np.linalg.norm([landmarks_array[13, 0] - landmarks_array[3, 0], landmarks_array[13, 1] - landmarks_array[3, 1]])
        line4 = np.linalg.norm([landmarks_array[8, 1] - y])

        angle = abs(degrees(math.atan2(landmarks_array[5, 1] - landmarks_array[3, 1], landmarks_array[5, 0] - landmarks_array[3, 0])))

        # Determine face shape
        shape = "Unknown"
        if abs(line1 - line2) < 10:
            shape = "Square" if angle < 160 else "Round"
        elif line3 > line1:
            shape = "Triangle" if angle < 160 else "Diamond"
        elif line4 > line2:
            shape = "Rectangular" if angle < 160 else "Oblong"

        # Get hairstyle recommendations
        recommendations = hairstyle_recommendations.get(shape, ["No recommendation available."])

        return shape, recommendations

    return "No face detected", []

# Test example
if __name__ == "__main__":
    # Replace this with a frame from your system or camera
    test_frame = cv2.imread("face_image.jpg")  # Example face image
    shape, recommendations = detect_face_and_recommend(test_frame)
    print(f"Detected Shape: {shape}")
    print("Hairstyle Recommendations:", recommendations)
