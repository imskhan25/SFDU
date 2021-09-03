# To generate OTP
import random

#To get date and time
import datetime
import time

# Import Module
from tkinter import *


#twilio sms gateway

from twilio.rest import Client

account_sid = 'AC0cebfdb6fced5357cecf78ee1e8xe830'
auth_token = '1aaefcbbb8e32543012ceaffm841c8c1'
client = Client(account_sid, auth_token)

#To connect with microcontroller 
import serial
import time
arduino=serial.Serial('COM7',9600)

#To recognize face
import cv2
import numpy as np
import face_recognition
# This is a running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific. If you have trouble installing it, try any of the other that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
image1 = face_recognition.load_image_file("image_3.jpeg")
image1_face_encoding = face_recognition.face_encodings(image1)[0]

# Load a second sample picture and learn how to recognize it.
#image2 = face_recognition.load_image_file("image_4.jpeg")
#image2_face_encoding = face_recognition.face_encodings(image2)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    image1_face_encoding
]
known_face_names = [
    "Sumit"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

e=0

# Import Module
from tkinter import *
 

while True:
    
    
    #choice for user 
    def choice():
        ch=input("enter N for next or q for exit: ")
        if ch=="N":
            print("Recoginsing Face...")
        elif ch=="q":
            pass
        else:
            print("Wrong Input!")
            choice()

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []     
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:                                
                
                print("Face Recoginsed!")
                name = known_face_names[best_match_index]
                
                
                face_names.append(name)
                
                process_this_frame = not process_this_frame
                
                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # Display the resulting image
                cv2.imshow('Video', frame)
                
                #Getting date and time
                x=str(datetime.datetime.now())
                y=x.replace(':','-')[:-7]
                
                # writing the extracted images
                s_name='DATA/'+y+' '+name+'.jpg'
                cv2.imwrite(s_name, frame)

                #generating random OTP
                otp=random.randint(100000,999999)
                #print(otp)
                
                # OTP will be send after face is recognised
                message = client.messages \
                .create(
                    body='*** your OTP to UNLOCK the DOOR is *** :- '+str(otp),
                     from_='+19163786591',
                     to='+917599208825'
                 )

                
                # create root window
                root = Tk()

                # root window title and dimension
                root.title("Smart Facial Door Unlock")

                # Set geometry (widthxheight)
                root.geometry('600x500')

                root.config(background = "black", pady=10)


                get_OTP=StringVar()
                attempt=0 
                def button():
                    global attempt
                    attempt+=1
                    global u_otp
                    global upw
                    u_otp=get_OTP.get()
                    #three attempts are allowed for OTP verification
                    #otp_v=input("please enter OTP: ")
                    # verify the OTP
                    if u_otp==str(otp):
                        print("Authentication Success!")
                        print("Welcome",name)
                        print("door is UNLOCKED!\n")

                        heading= Label(root, font=( 'aria' ,40, 'bold' ),text="DOOR UNLOCKED..!!",
                                          fg="orange",bd=10,bg='black')
                        heading.grid(row=3,column=1)



                        arduino.write(b'1')
                        print("You have 5 seconds to enter the room")

                        for i in range(1,6):
                            print(i,"...")
                            time.sleep(1)
                        print("Door is LOCKED again!")
                        arduino.write(b'0')
                        root.destroy()
                        choice()


                    else:
                        if attempt<3:
                            print("attempt",attempt,"Authentication Error!")
                            heading= Label(root, font=( 'aria' ,40, 'bold' ),text="Attempt Failed",
                                          fg="orange",bd=10,bg='black')
                            heading.grid(row=7,column=1)

                        else:

                            print("All attempts are failed...")
                            print("Unknown Access!")
                            print("Access Denied!")
                            print(" BUZZER<<BEEP>><<BEEP>>\n")


                            heading= Label(root, font=( 'aria' ,40, 'bold' ),text="UNKNOWN ACCESS",
                                          fg="orange",bd=10,bg='black')
                            heading.grid(row=7,column=1)

                            arduino.write(b'2')

                            for i in range(1,10):

                                time.sleep(1)

                            #arduino.write(b'0')
                            root.destroy()
                            choice()
                            



                def next():
                    root.destroy()
                    choice()


                # all widgets will be here
                heading= Label(root, font=( 'aria' ,30, 'bold' ),text="Smart Facial Door Unlock",
                                  fg="lightgreen",bd=10,bg='black')
                heading.grid(row=1,column=1)


                heading= Label(root, font=( 'aria' ,40, 'bold' ),text="FACE RECOGNISED..!!",
                                  fg="orange",bd=10,bg='black')
                heading.grid(row=2,column=1)


                b=Button(root,padx=16,pady=8, bd=10 ,fg="white",
                                font=('ariel' ,16,'bold'),width=4,
                                text="Submit", bg="red", command=button)
                b.grid(row=6,column=1)


                b=Button(root,padx=16,pady=8, bd=10 ,fg="white",
                                font=('ariel' ,16,'bold'),width=4,
                                text="Next", bg="red", command=next)
                b.grid(row=0,column=1)



                OTP_e= Entry(root,font=('ariel' ,16,'bold'), 
                                  bd=6,insertwidth=4,
                                  bg="yellow" ,justify='left',width=30, textvariable=get_OTP)
                OTP_e.grid(row=5,column=1)


                OTP_l= Label(root, font=( 'aria' ,30, 'bold' ),text="Enter OTP",
                                  fg="lightgreen",bd=10,bg='black')
                OTP_l.grid(row=4,column=1)


                # Execute Tkinter
                root.mainloop()
            else:
                face_names.append(name)
                
                process_this_frame = not process_this_frame
                
                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    
                    
                #Getting date and time
                x=str(datetime.datetime.now())
                y=x.replace(':','-')[:-7]
                
                # writing the extracted images
                s_name='DATA/'+y+' '+name+'.jpg'
                cv2.imwrite(s_name, frame)
                
                
                
                # Display the resulting image
                cv2.imshow('Video', frame)
                
                print("Unknown Access!")                
                print("Access Denied!")
                print(" BUZZER<<BEEP>><<BEEP>>\n")
                
                               
                arduino.write(b'2')

                for i in range(1,10):

                    time.sleep(1)
                    
                arduino.write(b'0')



                choice()
            face_names.append(name)
       

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Thank You! Successfully Exit...")
        break
        

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()