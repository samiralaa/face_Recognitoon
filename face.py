import cv2
import mysql.connector
import numpy as np
import os

# Load pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Connect to MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="Samir@14999",
        password="Samir@14999",
        database="ai"
    )
    cursor = conn.cursor()
    print("Connected to MySQL database")
except mysql.connector.Error as e:
    print("Error connecting to MySQL database:", e)
    exit()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS faces
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

    if not ret:
        print("Error: Couldn't capture frame")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Extract region of interest (ROI) for further analysis
        roi_color = frame[y:y+h, x:x+w]

        # Resize the face image to width=300 while preserving aspect ratio
        width = 300
        aspect_ratio = w / h
        height = int(width / aspect_ratio)
        resized_roi_color = cv2.resize(roi_color, (width, height))

        # Encode the resized face image as a JPEG image
        _, buffer = cv2.imencode('.jpg', resized_roi_color)
        face_blob = buffer.tobytes()

        # Prompt user to enter the name of the person associated with the detected face
        person_name = input("Enter the name of the person: ")

        # Insert face data into the database with the provided name
        try:
            cursor.execute("INSERT INTO faces (name, face) VALUES (%s, %s)", (person_name, face_blob))
            print("Face saved to database with name:", person_name)
            conn.commit()
            face_saved = True

            # Save the resized detected face image to the specified directory with the name of the person
            save_path = os.path.join("C:\\Users\\hpp\\Desktop\\Ai Project", person_name + "_face.jpg")
            cv2.imwrite(save_path, resized_roi_color)
            print("Resized detected face image saved to:", save_path)

        except mysql.connector.Error as e:
            print("Error saving face to database:", e)

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
