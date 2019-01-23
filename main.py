import cv2
import numpy as np
import imutils
from imutils import perspective
from scipy.spatial import distance as dist
import copy
import math
from videocaptureasync import VideoCaptureAsync
from maplinrobot import MaplinRobot

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def callback(event, x, y, flags, param):

            if event == cv2.EVENT_LBUTTONUP:
                for i in range(0,len(contours)):
                	r=cv2.pointPolygonTest(contours[i],(x,y),False)
                	if r>0 and cv2.contourArea(contours[i]) > 50:
                		global selected_contour
                		selected_contour = contours[i]

def contourCenter(contour):
	M = cv2.moments(contour)
	if M["m00"] != 0:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		return (cX, cY)
	else:
		return None
		
if __name__ == '__main__':

	global contours, selected_contour
	s = MaplinRobot()

	selected_contour = []
	laser_center = None
	selected_contour_center = None


	colors_lower_range = np.array([[170, 100, 200], [52, 100, 100], [103, 100, 100], [18, 100, 100]], dtype=np.uint8)
	colors_upper_range = np.array([[190, 255, 255], [72, 255, 255], [125, 255, 255], [40, 255, 255]], dtype=np.uint8)
	colors = ("Red","Green","Blue","Yellow")

	cap = VideoCaptureAsync(0)
	cap.start()
	cv2.namedWindow('image')
	cv2.setMouseCallback('image', callback)
	

	while True:
		# Capture frame-by-frame
		ret, img = cap.read() 
		img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		black = np.zeros((img.shape[0],img.shape[1],1), np.uint8)
		_, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)	
		_, laser = cv2.threshold(img2gray, 250, 255, cv2.THRESH_BINARY)	
		_, drop = cv2.threshold(img2gray, 20, 255, cv2.THRESH_BINARY_INV)	
		drop_mask = np.zeros((img.shape[0],img.shape[1],1), np.uint8)
		drop_mask[0:int(drop_mask.shape[0]/3),drop_mask.shape[1]-int(drop_mask.shape[1]/3):drop_mask.shape[1]]=255
		drop_area = cv2.bitwise_and(drop,drop_mask,mask = mask)
		
		
				
				
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		output = copy.deepcopy(img)
		contours = []
		
		cnts = cv2.findContours(drop_area, cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key = cv2.contourArea)
		x,y,w,h = cv2.boundingRect(c)
		# draw the book contour (in green)
		cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
		cv2.putText(output, "Drop Area", (x+10,y+h+20),
							cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,0), 2)

		if len(selected_contour) == 0:
			for color in range(0,len(colors)):
				
				lower_range = colors_lower_range[color]
				upper_range = colors_upper_range[color]
				color_name = colors[color]
				hsv_range = cv2.inRange(hsv, lower_range, upper_range)
				result = cv2.bitwise_or(black,hsv_range,mask = mask)
				cnts = cv2.findContours(result.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)
				#print(str(color_name)+" has "+str(len(cnts))+ "circles")
				

				for c in cnts:
					#cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
					if cv2.contourArea(c) < 50:
						continue
					contours.append(c)
					(x,y),radius = cv2.minEnclosingCircle(c)
					center = (int(x),int(y))
					radius = int(radius)
					output = cv2.circle(output,center,radius,(0,0,255),2)
					rect = cv2.boundingRect(c)
					x,y,w,h = rect
					cv2.putText(output, color_name, (int(x-radius/2),int(y)),
							cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,0), 2)
			
		else:
				cnts = cv2.findContours(laser.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)
								

				if len(cnts) != 0:
					laser_center = contourCenter(cnts[0])
					cv2.circle(output, laser_center, 3, (0, 0, 0), -1)
					(selex,y),radius = cv2.minEnclosingCircle(selected_contour)
					center = (int(x),int(y))
					radius = int(radius)
					output = cv2.circle(output,center,radius,(0,0,255),3)
					selected_contour_center = contourCenter(selected_contour)
					D = dist.euclidean(laser_center, selected_contour_center)
					print("distance = " + str(D))
					r=cv2.pointPolygonTest(selected_contour,laser_center,False)
					if r<=0:
						#s.MoveArm(t=1.0, cmd='shoulder-up')
						angle_rad = math.atan2(selected_contour_center[1]-laser_center[1], selected_contour_center[0]-laser_center[0])
						angle_degree = math.degrees(angle_rad)
						#Acordding to the current setup, the arm move about 20 degrees for each 0.1 second
						arm_movement_time = 0.1 * abs(angle_degree) / 20
						if angle_degree <= 5 and angle_degree >= -5:
							print("found")
						else:
							if angle_degree > 5:
								s.MoveArm(arm_movement_time , cmd='base-anti-clockwise')
								time.sleep(0.5)
							elif angle_degree < 5:
								s.MoveArm(arm_movement_time , cmd='base-clockwise')
								time.sleep(0.5)

						print("center = " + str(laser_center))
						print("degree = " + str(angle_degree))
				else:
					s.MoveArm(0.05, cmd='base-clockwise')
				
		
		#cv2.imshow('mask', aho)
		cv2.imshow('image', output)

		if cv2.waitKey(1) & 0xFF == ord('c'):
			selected_contour = []
	 
		elif cv2.waitKey(1) & 0xFF == ord('q'):
			break
		 
	cv2.destroyAllWindows()
