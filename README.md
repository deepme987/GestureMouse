# Gesture Controlled Mouse

  An idea started in hack-a-thon which is further continued to make a finished product, GCM is a great utility tool for lazy people/ presentation users.
  
  It makes use of hand gestures to have control over desktop mouse using OpenCV and pynput.
  
## How To Use:

**1. Clone the repository:**
&nbsp;&nbsp; `git clone -https://github.com/deepme987/GestureMouse.git`
 
**2. Ensure you've the required libraries:**

&nbsp;&nbsp; To check, type `pip freeze` in cmd and look for following external packages
```
imutils==0.5.2
numpy==1.16.4
opencv-python==4.1.0.25
Pillow==6.1.0
pynput==1.4.2
pypiwin32==223
pywin32==224
six==1.12.0
win10toast==0.9
wxPython==4.0.6
```

&nbsp;&nbsp; If you don't find any of the libraries, install them with pip:
  
`pip install <library-name>`

```
pip install opencv-python
pip install imutils
pip install win10toast
pip install pynput
pip install wxPython 
```
    
**3. Once everything is ready, launch the Gesture Control using:**

`python Gesture-Control.py`

**4. Wait for camera to pop and hold your hand still at center of ROI**

**5. When a message of `Calibrated` appears, mouse your hand slowly to test the mouse**
- Move left, right, up, down for mouse movement
- Close-Open grip in 1 second for MOUSE1 or MouseClick
- Hold grip for MouseDrag, Release grip for MouseRelease to drag and drop

**6. Remove your mouse from ROI to get control back to mouse**

**7. Press 'q' on keyboard to stop**

## For better results:
- Keep your camera still
- Stay out of ROI duing initialisation
- Keep dark elegant or plain white background

## Future Scope:
  - Converting basic Image Processing into Machine Learning to enable custom gesture-action combo
  
  - Addition of special gestures for built-in windows apps
    
  - Adding recognization of a specific color, so that object can be used instead of hand
    
  - Improvising the accuracy and reducing noise
    
  - Using finger counts to add more possibilites
    
  - Using Voice Control to enable the script(Saving battery)

### Any bug reports or feedbacks are appreciated
