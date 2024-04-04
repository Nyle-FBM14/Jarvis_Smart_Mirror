import eel
from ui import switch_to_main_ui

import cv2
import face_recognition
from tkinter import *
from PIL import Image, ImageTk
import pickle
import os
global counter
counter = 0

global username
username = "Test Name"

@eel.expose
def getUsername():
    return username

def facial_code():
    def switch_to_main(name):
        #set this when user is logged in
        global username
        username = name
        try:
            os.remove("screenshot.jpg")
        except OSError as e:
            # If it fails, inform the user.
            print("Error: %s - %s." % (e.filename, e.strerror))
        cap.release()
        root.destroy() # Properly destroy the current Tkinter window

    # Load the pre-trained Haarcascades face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the camera (0 represents the default camera)
    cap = cv2.VideoCapture(0)

    # Initialize Tkinter window
    root = Tk()
    root.title("Facial Recognition Demo")
    root.config(bg="black")  # specify background color


    # Create a label for displaying the video feed
    video_label = Label(root)
    video_label.pack(pady=20)

    welcome_label = Label(root, text="Welcome - Please Look At the Mirror", font=('Helvetica 14 bold'), fg='white', bg='black')
    welcome_label.pack(pady=20)

    def load_encodings():
        encodings = {}
        encoding_directory = "UserData/encoding/"
        for name_folder in os.listdir(encoding_directory):
            # Convert the folder name to lowercase
            name = name_folder.lower()
            encodings[name] = []

            # Load all the encoding files for the current name
            name_folder_path = os.path.join(encoding_directory, name_folder)
            for encoding_file in os.listdir(name_folder_path):
                encoding_file_path = os.path.join(name_folder_path, encoding_file)
                with open(encoding_file_path, "rb") as file:
                    encoding = pickle.load(file)
                    encodings[name].append(encoding)
                    print(name)

        return encodings

    # Load all encodings
    all_encodings = load_encodings()

    # Function to update video feed
    def update_video():
        global counter
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Save a screenshot when a face is detected
            cv2.imwrite('screenshot.jpg', frame)
            counter = counter+1
            #print(counter)

        # Display the resulting frame in the Tkinter window
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
        # Call update_video after 1 ms (you can adjust the delay)
        root.after(1, update_video)
        if counter >= 30:
            counter = 0
            recognize_face()

    # Start updating the video feed
    update_video()

    # Function to handle face recognition
    def recognize_face():
        try:
            # Load the screenshot image for recognition
            t6 = face_recognition.load_image_file("screenshot.jpg")
            CurrentFace = face_recognition.face_encodings(t6)[0]

            max_average_result = 0
            recognized_name = None

            for name, encodings in all_encodings.items():
                # Compare the current face with all encodings for the current name
                results = face_recognition.compare_faces(encodings, CurrentFace, 0.6)
                average_result = sum(results) / len(results)

                if average_result > max_average_result:
                    max_average_result = average_result
                    recognized_name = name

            if recognized_name:
                welcome_label.config(text=f"Welcome {recognized_name}!", font=('Helvetica 14 bold'), fg='white', bg='black')
                
                encoding_directory = f"UserData/encoding/{recognized_name}"
                # Check if file with the same name exists
                existing_files = os.listdir(encoding_directory)
                existing_names = [file.split('_')[0] for file in existing_files]
                count = len(existing_names)
                name = f"{recognized_name}_{count}"  # Append number to the name
                encoding_file_path = os.path.join(encoding_directory, f"{name}_encoding.pkl")
                try:
                    with open(encoding_file_path, "wb") as file:
                        pickle.dump(CurrentFace, file)  # Save the encoding dump
                except Exception as e:
                    print(f"Error saving encoding file: {e}")
                
                switch_to_main(recognized_name)
            else:
                welcome_label.config(text="Hello, New User!", font=('Helvetica 14 bold'), fg='white', bg='black')
                
                # Save the encoding dump to the relevant folder
                name = input("Enter the name of the person: ")  # Ask for the name of the person
                name = name.lower()
                encoding_directory = f"UserData/encoding/{name}/"
                os.makedirs(encoding_directory, exist_ok=True)  # Create directory if it doesn't exist
                encoding_file_path = os.path.join(encoding_directory, f"{name}_encoding.pkl")
                with open(encoding_file_path, "wb") as file:
                    pickle.dump(CurrentFace, file)  # Save the encoding dump
                    
                switch_to_main(name)

        except IndexError:
            welcome_label.config(text="No Face Detected", font=('Helvetica 14 bold'), fg='white', bg='black')

    # Button to trigger face recognition
    recognize_button = Button(root, text="Recognize Face", command=recognize_face, font=('Helvetica 14 bold'), fg='white', bg='black')
    recognize_button.pack(pady=10)

    # Button to trigger the transition to the second page
    switch_button = Button(root, text="Switch to Main UI", command=lambda: switch_to_main("Testing"), font=('Helvetica 14 bold'), fg='white', bg='black')
    switch_button.pack(pady=10)

    # Start the Tkinter mainloop
    root.mainloop()

    # Release the camera
    cap.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()