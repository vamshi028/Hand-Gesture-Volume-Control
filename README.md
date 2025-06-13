# Hand-Gesture-Volume-Control
This project implements a hand-gesture-based volume control system using Python and web technologies. It consists of four main components: HandTrackingModule.py, VolumeControl.py, app.py, and index.html.
HandTrackingModule.py is a Python module that uses the mediapipe library to detect hands in a video feed and track their positions. It provides methods to find hands and determine the positions of the landmarks, with optional drawing for visualization.
VolumeControl.py is a script that uses the HandTrackingModule to control the system volume based on hand gestures. It captures video from the webcam, detects hand gestures, and maps the distance between the thumb and index finger tips to the system volume using the pycaw library. It also provides visual feedback by drawing on the video feed.
app.py is a Flask web application that integrates the hand-tracking volume control into a web interface. It serves a video feed from the webcam and provides real-time volume updates to the web interface. The Flask application runs a web server that allows users to control the volume via a web browser.
index.html is the front-end of the web application. It displays the video feed from the webcam and shows a volume bar that updates in real-time based on the hand gestures. The volume bar is dynamically updated using JavaScript, providing an interactive user experience.
Overall, this project allows users to control the volume of their computer using hand gestures, providing a seamless and interactive experience. The system is designed to be user-friendly and can be easily deployed and used on any system with a webcam.

# Requirements:-

To run the code you provided, you'll need to install several Python libraries. Here’s a list of the required libraries along with their installation commands:

1. OpenCV: For image and video processing.
   
   pip install opencv-python
 

2. MediaPipe: For hand tracking.
  
   pip install mediapipe

3. NumPy: For numerical operations.
  
   pip install numpy
   

4. Flask: For web framework to serve the application.
  
   pip install Flask
  

5. PyCaw: For controlling audio volume in Windows.
  
   pip install pycaw
 

6. comtypes: Required for the PyCaw library.

   pip install comtypes
   if pip install comtypes gives errors while executing the files then try to install given below commands 
   pip install --upgrade comtypes  # not work
   pip uninstall comtypes && pip install --upgrade comtypes  # not work
   pip uninstall comtypes && pip install --no-cache-dir comtypes  # works
  

7. ctypes: This is a built-in library in Python, so no installation is needed for this.
You can install all of these libraries using pip by running the following command in your terminal:

   pip install opencv-python mediapipe numpy Flask pycaw comtypes




