import cv2
import mysql.connector
import numpy as np
import os

# Load pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="Samir@14999",
    password="Samir@14999",
    database="ai"
)
cursor = conn.cursor()

# Create table if not exists for faces
cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(255),
                  face LONGBLOB)''')

# Create table if not exists for attendance
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(255),
                  face LONGBLOB)''')

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

# Flag to track if face is saved
face_saved = False

while not face_saved:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Extract region of interest (ROI) for further analysis
        roi_color = frame[y:y+h, x:x+w]

        # Encode the face as a JPEG image
        _, buffer = cv2.imencode('.jpg', roi_color)
        face_blob = buffer.tobytes()

        # Check if the detected face already exists in the database
        cursor.execute("SELECT * FROM faces WHERE face = %s", (face_blob,))
        existing_face = cursor.fetchone()

        if existing_face:
            print("Face already exists in the database. Saving to attendance table instead.")
            # Insert face data into the attendance table with the associated name
            cursor.execute("INSERT INTO attendance (name, face) VALUES (%s, %s)", (existing_face[1], face_blob))
        else:
            # Prompt user to enter the name of the person associated with the detected face
            person_name = input("Enter the name of the person: ")

            # Insert face data into the faces table with the provided name
            cursor.execute("INSERT INTO faces (name, face) VALUES (%s, %s)", (person_name, face_blob))
            print("Face saved to database with name:", person_name)

            # Insert face data into the attendance table with the associated name
            cursor.execute("INSERT INTO attendance (name, face) VALUES (%s, %s)", (person_name, face_blob))
            print("Face saved to attendance table with name:", person_name)

        # Commit changes to the database
        conn.commit()

        # Set the flag to True to break out of the loop
        face_saved = True

        # Display the resulting frame
        cv2.imshow('Save Face', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

# Close the database connection
conn.close()
