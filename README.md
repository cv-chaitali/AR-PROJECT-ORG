AR project related to Distance angle measurement if there are multiple markers present in the situation. 
The algorithm used in this project are 1. L2 Norm or Euclidean Distance formula and Cosine rule for triangle. 
The workflow was :
1. Calibrate the camera [ We have used Pinhole camera model for 120 degree and 115 degree FOV cameras ]
2. If it has more than 150/180 degree FOV Fisheye model is recommended
3. For real time cv2.VideoCapture (0) : If we use USB camera connected with the laptop.. we can use cv2.VideoCapture (1).. However the camera gets shuffled so it's better to run and check
4. To run any of the code in code folder.
5. Under 1.5m distance the process goes well
