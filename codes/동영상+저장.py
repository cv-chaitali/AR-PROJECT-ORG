import cv2
import numpy as np
import math
import glob
import os
import time
import random
import json


data_list = []

if os.path.exists("dataset3.txt"):
    # If it exists, load the data from the file
    with open("dataset3.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split("\t")
            distance1 = float(data[0])
            distance2 = float(data[1])
            angle = float(data[2])
            data_list.append([distance1,distance2,angle])
    # Remove the file to avoid appending the same data multiple times
    os.remove("dataset3.txt")


calibration = np.load("CALIBRATION DATA.npz")

mtx= calibration["camMatrix"]
dist = calibration["distCoef"]
mtx= calibration["camMatrix"]
dist = calibration["distCoef"]
marker1_id = 100
marker2_id = 101
marker3_id = 102
latest_modification_time = 0


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

while True:
    
    video_files = glob.glob("*.mp4")
    
    
    video_files = sorted(video_files, key=os.path.getmtime)
    
    if os.path.getmtime(video_files[-1]) > latest_modification_time:
        latest_modification_time = os.path.getmtime(video_files[-1])
        
        file = video_files[-1]
        
        cap = cv2.VideoCapture(file)
        
        while True:
            ret, frame = cap.read()
            
            if frame is None:
                # Restart the loop to check for the next latest added video file
                print("video has ended")
                break
            corners, ids, rejectedImgPoints = detector.detectMarkers(frame)     
            if ids is None:
                print("마커 없습니다")
##NOoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                 

                #마커 2개 보일때   
            elif ids is not None and len(ids) == 2:
                marker1_index = None
                marker2_index = None
                for i in range(len(ids)):
                    if ids[i] == marker1_id:
                        marker1_index = i
                    elif ids[i] == marker2_id:
                        marker2_index = i
                    elif ids[i] == marker3_id:
                        marker2_index = i
        
                if marker1_index is not None and marker2_index is not None:
                    #마커 정보 r 과 t
                    rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker1_index], 300.0, mtx, dist)
                    rvec2, tvec2, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker2_index], 300.0, mtx, dist)
                    distance = cv2.norm(tvec1-tvec2)                     
                    point1 = cv2.drawFrameAxes(frame, mtx, dist, rvec1, tvec1 ,  4,4)
                    point2 = cv2.drawFrameAxes(frame, mtx, dist, rvec2, tvec2 ,  4,4)

 ##NOoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                 
            #마커 3개 보일때      
            elif ids is not None and len(ids) == 3:
                marker1_index = None
                marker2_index = None
                marker3_index = None
                for i in range(len(ids)):
                    if ids[i] == marker1_id:
                        marker1_index = i
                    elif ids[i] == marker2_id:
                        marker2_index = i
                    elif ids[i] == marker3_id:
                        marker3_index = i
                if marker1_index is not None and marker2_index is not None and marker3_index is not None:
                    #마커 정보 r 과 t
                    rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker1_index], 300.0, mtx, dist)
                    rvec2, tvec2, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker2_index], 300.0, mtx, dist)
                    rvec3, tvec3, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker3_index], 300.0, mtx, dist)
            
                    # 거리 계산
                    
                    distance1 = cv2.norm(tvec1-tvec2)
                    distance2 = cv2.norm(tvec1-tvec3)
                    distance3 = np.sqrt(distance1**2+distance2**2)
                    angle =math.degrees(math.acos((distance1**2+distance2**2-distance3**2)/(2.0*distance1*distance2)))
                    
                    print("마커 1 과 마커 2 거리:", (round(distance1,2),0,0))
                    print("마커 1 과 마커 3 거리:", (0,round(distance2,2),0))
                    
                    data_list.append([distance1,distance2,angle])

                    filename1 = "dataset3_" + str(int(time.time())) +  "_" + str(random.randint(1, 10000)) + ".txt"  # add a timestamp to the filename
                    with open("dataset3.txt", "a") as f:
                        for data in data_list:
                            f.write("{:.2f}\t{:.2f}\t{:.2f}\n".format(data[0], data[1], data[2]))
                        data_list.clear()
                   
                    
                    with open ("dataset3.txt") as f :
                        lines = f.readlines()
                    max_cols = 0
                    for line in lines:
                        row = line.strip().split()
                        max_cols = max(max_cols, len(row))
                        col1_sum = 0
                        col2_sum = 0
                        col3_sum = 0
                        num_rows = len(lines)
    
                        for line in lines:
                            cols = line.split()
                            col1_sum += float(cols[0])
                            col2_sum += float(cols[1])
                            col3_sum += float(cols[2])
    
                        col1_avg = col1_sum / num_rows
                        col2_avg = col2_sum / num_rows
                        col3_avg = col3_sum / num_rows
    
                        print("Average of column 1:", col1_avg)
                        print("Average of column 2:", col2_avg)
                        print("Average of column 3:", col3_avg)
    
    
                        # Define the JSON data
                        data_마커_3개 = {
                            "result": [
                                {"distance1": col1_avg,
                                "distance2": col2_avg,
                                "angle": col3_avg}
                            ]
                        }
                        dataset_time1 = os.path.getmtime(video_files[-1])
                        time_str1 = time.strftime("%Y%m%d-%H%M", time.localtime(dataset_time1))
                        filename1 = f"data_마커_3개_{time_str1}.json"
                        with open(filename1, "w") as f:
                            json.dump(data_마커_3개, f)
                   
                    
        # Release the video file
        cap.release()
        
