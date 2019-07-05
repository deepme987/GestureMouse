# Gesture Controlled Mouse

  An idea started in hack-a-thon which is further continued to make a finished product, GCM is a great utility tool for lazy people/ presentation users.
  
  It makes use of hand gestures to have control over desktop mouse using OpenCV and pynput.
  
## How To Use:

**1. Clone the repository:**
&nbsp;&nbsp; `git clone -https://github.com/deepme987/GestureMouse.git`
 
**2. Ensure you've the required libraries:**

&nbsp;&nbsp; To check, type `pip freeze` in cmd and look for following external packages
```
opencv-python
imutils
win10toast
pynput
wx
```

&nbsp;&nbsp; If you don't find any of the libraries, install them with pip:
  
`pip install <library-name>`

```
pip install opencv-python
pip install imutils
pip install win10toast
pip install pynput
pip install wx
```
    
**3. Once everything is ready, launch the Gesture Control using:**

`python "Gesture Control.py"`

## Future Scope:
  - Converting basic Image Processing into Machine Learning to enable custom gesture-action combo
  
  - Addition of special gestures for built-in windows apps
    
  - Adding recognization of a specific color, so that object can be used instead of hand
    
  - Improvising the accuracy and reducing noise
    
  - Using finger counts to add more possibilites
    
  - Using Voice Control to enable the script(Saving battery)

