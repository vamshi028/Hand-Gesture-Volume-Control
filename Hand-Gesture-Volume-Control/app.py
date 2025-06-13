from flask import Flask, render_template, Response
import cv2
import HandTrackingModule as htm
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from flask import jsonify
app = Flask(__name__)
detector = htm.HandDetector()

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

# Initialize volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

def generate_frames():
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        
        if len(lmList) != 0:
            # Index finger and thumb tip coordinates
            x1, y1 = lmList[4][1], lmList[4][2]  # Index finger tip
            x2, y2 = lmList[8][1], lmList[8][2]  # Thumb tip
            
            # Calculate length between the fingers
            length = np.hypot(x2 - x1, y2 - y1)
            
            # Set volume based on finger distance
            vol = np.interp(length, [20, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

            # Calculate volume percentage
            volPer = np.interp(vol, [minVol, maxVol], [0, 100])
            volPer = int(volPer)

            # Visual indicators
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # Button effect
            if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            # Draw the volume percentage on the image
            cv2.putText(img, f'Volume: {volPer}%', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Encode image as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/volume')
def volume_update():
    vol = volume.GetMasterVolumeLevelScalar()  # Get current volume level as a scalar
    volPer = np.interp(vol, [minVol, maxVol], [0, 100])
    return jsonify({'volume': int(volPer)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
