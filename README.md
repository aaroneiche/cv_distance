
# CV Distance calculation and finding.

This script was made while exploring OpenCV as part of a learning project for work. It will identify 
blobs on the calibration grid, and using a known focal length of the camera, and determine their approximate distance based on the relationship to the nearest neighbor dot.

<img src="demo.gif" width="640" height="378">

## Running 
There are 3 ways to run this script:

Video:
`python findCircles.py videoname.mp4 video`
Image:
`python findCircles.py imagename.jpg image`
Webcam
`python findCircles.py blerf live`
(Note the above 'filler' arg - this will be fixed in the future.)

## Controls
When running the script, there are several key commands you can issue to control the view:
`1` : Color image (Raw Webcam feed)
`2` : Greyscale image (cut out color to make thresholding easier) 
`3` : Thresholded Image
`4` : (Default) The Data image (where we overlay data on the color image.)

On The Data image you can toggle the following: 
`b` : Blob Identities (IDs and location of detected 'blobs')
`l` : Lines drawn to nearest neighbors
`d` : Distance text calculated for blobs, based on nearest neighbor identity.

## Environment
In order to run this script, you need the following installed in your python environment:
- Python 3 (This was made with Python 3.8.13)
And these libraries (I installed with pip)
- OpenCV4 with contribs `opencv-contrib-python`
- imutils `opencv-python`
- attrs `attrs`

I strongly recommend using `pyenv` to manage your python versions, and `virtualenv` to create a dependable environment for running OpenCV projects in.

## Calibration
The calibration pattern used in the image and video can be found here: 
https://nerian.com/nerian-content/downloads/calibration-patterns/pattern-letter.pdf
Mine was cut in half to accommodate a piece of cardboard I had. More information about finding the focal length of your own camera, and calibrating is avaiable here: https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/

More calibration patterns and information here: https://nerian.com/support/calibration-patterns/

### Acknowledgements 
A lot of the code here is representative of context learned from the [OpenCV documentation](https://docs.opencv.org/), [pyimagesearch.com](https://pyimagesearch.com), [learnopencv.com](https://learnopencv.com), and dozens of Stack Overflow and random forum questions. As a result, the code may reflect similarity to code found elsewhere. 