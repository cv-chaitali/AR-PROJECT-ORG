import cv2
import numpy as np
import math
import os
# calibration = np.load("/Users/chaitalibhattacharyya/Desktop/ARE/cam_mat.npz")
calibration = np.load("/Users/chaitalibhattacharyya/Desktop/ARE/calib_data_AVER/MultiMatrix.npz")

mtx= calibration["camMatrix"]
dist = calibration["distCoef"]

marker1_id = 101
marker2_id = 100
marker3_id = 102

cap = cv2.VideoCapture(1)


while True:
    ret, frame = cap.read()
    
    if frame is None:
        # Restart the loop to check for the next latest added video file
        break
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000))
    #마커 2개 보일때   
    if ids is not None and len(ids) == 2:
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
            rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker1_index], 100.0, mtx, dist)
            rvec2, tvec2, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker2_index], 100.0, mtx, dist)
            distance = cv2.norm(tvec1-tvec2)
            print("2개 마커 사이의 거리:", distance)
            
            
            point1 = cv2.drawFrameAxes(frame, mtx, dist, rvec1, tvec1 ,  9,4)
            point2 = cv2.drawFrameAxes(frame, mtx, dist, rvec2, tvec2 ,  9,4)
            frame_markers = cv2.aruco.drawDetectedMarkers(frame,corners,ids,(0,255,0))
            for i in range(len(ids)):
            
                id_num = str(ids[i][0])
                
                
                center = tuple(map(int, corners[i][0].mean(axis=0)))
                
                
                cv2.putText(frame_markers, id_num, center, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "Distance between marker 1 and marker 2: {:.2f}".format(round(distance,2)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

            # cv2.imshow("Frame", frame_markers)
            key = cv2.waitKey(1) & 0xFF

            
    elif ids is not None and len(ids) >= 3:
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
            rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker1_index], 100.0, mtx, dist)
            rvec2, tvec2, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker2_index], 100.0, mtx, dist)
            rvec3, tvec3, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker3_index], 100.0, mtx, dist)
    
            # 거리 계산
            
            distance1 = np.linalg.norm(tvec1-tvec2)
            distance2 = np.linalg.norm(tvec1-tvec3)
            distance3 = np.linalg.norm(tvec2-tvec3)
            
            
            print("마커 1 과 마커 2 사이의 거리:", distance1)
            print("마커 1 과 마커 3 사이의 거리:", distance2)
            print("마커 2 과 마커 3 사이의 거리:", distance3)
            
            point1 = cv2.drawFrameAxes(frame, mtx, dist, rvec1, tvec1 ,  4,4)
            point2 = cv2.drawFrameAxes(frame, mtx, dist, rvec2, tvec2 ,  4,4)
            point3 = cv2.drawFrameAxes(frame, mtx, dist, rvec3, tvec3 , 4,4)
            
            frame_markers = cv2.aruco.drawDetectedMarkers(frame,corners,ids,(0,255,0))
            for i in range(len(ids)):
                id_num = str(ids[i][0])
                
                
                center = tuple(map(int, corners[i][0].mean(axis=0)))
                
                # Draw the ID number on the frame at the center of the marker
                # cv2.putText(frame_markers, id_num, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            
            



            cv2.putText(frame, "Distance between marker 1 and marker 2: {:.2f}".format(round(distance1,2)), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, "Distance between marker 1 and marker 3: {:.2f}".format(round(distance2,2)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        
cap.release()
cv2.destroyAllWindows()

            