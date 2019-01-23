#!/usr/bin/env python

#ROBOT ARM CONTROL PROGRAM

# MoveArm(1,[0,1,0]) @Rotate base anti-clockwise
# MoveArm(1,[0,2,0]) @Rotate base clockwise
# MoveArm(1,[64,0,0]) @Shoulder up
# MoveArm(1,[128,0,0]) @Shoulder down
# MoveArm(1,[16,0,0]) @Elbow up
# MoveArm(1,[32,0,0]) @Elbow down
# MoveArm(1,[4,0,0]) @Wrist up
# MoveArm(1,[8,0,0]) @ Wrist down
# MoveArm(1,[2,0,0]) @Grip open
# MoveArm(1,[1,0,0]) @Grip close
# MoveArm(1,[0,0,1]) @Light on
# MoveArm(1,[0,0,0]) @Light off

#Use sudo pip install pyusb for usb.core

import usb.core, usb.util, time, sys
import argparse



class MaplinRobot:
	def __init__(self):
		self.usb_vendor_id=0x1267
		self.usb_prod_id=0x001
		self.rctl = usb.core.find(idVendor=self.usb_vendor_id, idProduct=self.usb_prod_id) #Object to talk to the robot
		self.duration=1.0 # Duration (In seconds) for each action. Defaults to 1 second
		
		self.moves={
		'base-anti-clockwise' : [0,1,0],
		'base-clockwise' : [0,2,0],
		'shoulder-up': [64,0,0],
		'shoulder-down': [128,0,0],
		'elbow-up': [16,0,0],
		'elbow-down': [32,0,0],
		'wrist-up': [4,0,0],
		'wrist-down': [8,0,0],
		'grip-open': [2,0,0],
		'grip-close': [1,0,0],
		'light-on': [0,0,1],
		'light-off': [0,0,0],
		'stop': [0,0,0],
		}

	def SetVendorId(self,vid):
		self.usb_vendor_id = vid


	def SetProdID(self,pid):
		self.usb_prod_id = pid


	def StopArm(self):
		if self.CheckComms():
			self.rctl.ctrl_transfer(0x40,6,0x100,0,self.moves['stop'],1000) #Send stop command	
			return True
		else:
			return False


	def CheckComms(self):
		'''Checks that the arm is connected and we can talk to it'''
		try:
			if self.rctl != None:
				return True
			else:
				print ("Couldn't talk to the arm.\n")
				return False
		except usb.core.USBError:
			print ("USB communication error.\n")
			return False

	def MoveArm(self,t,cmd):
		try:
			#Check that we can send commands to the arm
			if self.CheckComms():
				#We can send stuff
				print ("Sending command %s\n" %cmd)
				self.rctl.ctrl_transfer(0x40,6,0x100,0,self.moves[cmd],1000) #Send command
				time.sleep(t) #Wait 
				self.StopArm()
				print ("Done.\n")
				return True
			else:
				return False
			
		except KeyboardInterrupt:
			print ("ctrl-c pressed. Stopping the arm")
			self.StopArm()
			return False

		except usb.core.USBError:
			print ("USB communication error.\n")
			return False

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--part", required=True,
	help="base - shoulder - elbow")
ap.add_argument("-a", "--action", required=True,
	help="up - down - anti-cloclwise - clockwise")
ap.add_argument("-time", "--time", required=True,
	help="Moving Time")
args = vars(ap.parse_args())

#Example usage
s = MaplinRobot()

if args["part"] == "base" or args["part"] == "b":
	if args["action"] == "anti" or args["action"] == "a":
		s.MoveArm(float(args["time"]), cmd='base-anti-clockwise')
	elif args["action"] == "clock" or args["action"] == "c":
		s.MoveArm(float(args["time"]), cmd='base-clockwise')
elif args["part"] == "shoulder" or args["part"] == "s":
	if args["action"] == "up" or args["action"] == "u":
		s.MoveArm(float(args["time"]), cmd='shoulder-up')
	elif args["action"] == "down" or args["action"] == "d":
		s.MoveArm(float(args["time"]), cmd='shoulder-down')
elif args["part"] == "elbow" or args["part"] == "e":
	if args["action"] == "up" or args["action"] == "u":
		s.MoveArm(float(args["time"]), cmd='elbow-up')
	elif args["action"] == "down" or args["action"] == "d":
		s.MoveArm(float(args["time"]), cmd='elbow-down')

#s.MoveArm(t=0.5, cmd='shoulder-down')
#s.MoveArm(t=1.0, cmd='elbow-up')
#while True:
#	s.MoveArm(t=1.0, cmd='light-on')
#s.MoveArm(t=1.0, cmd='elbow-down')	
#s.MoveArm(t=1.0, cmd='elbow-down')
#s.MoveArm(t=0.5, cmd='grip-close')	
#s.MoveArm(t=1.0, cmd='wrist-up')	

