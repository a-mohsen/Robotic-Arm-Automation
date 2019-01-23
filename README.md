# OWI-535 Automation
![enter image description here](https://www.robotshop.com/media/catalog/product/cache/image/380x380/9df78eab33525d08d6e5fb8d27136e95/o/w/owi-535-robotic-arm-edge_1.jpg)

**OWI-535** (also known as イスペット グリッパーアームロボット in Japan) is a cheap robot with 5-DoF. It can mainly be controlled through a wired remote control, but the company has released a USB controller to be connected to PC, which can be used to control the arm using Python.

![enter image description here](https://lh3.googleusercontent.com/7r0WnigM4FbdM5p84zkLsklfdIDVpDrcC33pNcGAi4hgKmI5xQ8dWXsgR7Rj14dE7E-gwRd3QLTn)

The idea of this project was to attach an electromagnet to the arm's gripper to pickup metallic materials, but as a small electromagnet was used in this project, I've limited the metallic items to some colored stickers having some staples inside them.


![enter image description here](https://lh3.googleusercontent.com/mNwRdpSFxPWjXbuUtHGH8r7mnKEBmZCi5cK4zm94YlVXUhqGN_vBRVnl6nnjrd09xM3-zMRJiDtC)

To simplify the problem and decrease the degree of freedoms, a vertical camera was installed to convert it to a 2D problem.

![enter image description here](https://lh3.googleusercontent.com/RcWsCQw4g63LhdEZ1PZ2cE0zPxm0YvXwRB72ep27tkY5Lbh-iBTrciNmi2ZUdgYTyQjQqRhvbUgT)

The application is implemented on RaspberryPi3, which is attached to a touch screen.
The camera shows the work-space with the items to the user, and he selects the item he wants to pickup. For the current moment, all the items are circular with specific colors, so the program starts to convert the space to HSV to segment the items (and the drop area), then detect the contours and the center of the circle.


![enter image description here](https://lh3.googleusercontent.com/IHucTPZGLfUjRMNzZS3ypaXErCNFJVzP0iuTwZsXn3R1PwEBpT7HIat6Lyri1h8mxvL7muSdDK--)
A laser module is installed on the robot arm to identify the arm position -It has been installed behind the magnet, to allow the camera to track the magnet position, even if the arm is down like the above picture-. So the arm starts first to move its base to stand in front of the center of the circle, then it starts to move the rest of the arm to reach the item. Once it reaches it, it enables the electromagnet to pickup the item, then start moving to the drop area to drop it.

The main drawback of this robot is having an open-loop system. As it uses DC motors, it's so hard to derive equations or to apply any kinematics methods to move the arm, because of the lacking of any feedback. The solution can be found on this link: https://www.instructables.com/id/Intro-and-what-youll-need/, where motor shield and some potentiometers can be used to determine to arm position.

![enter image description here](https://lh3.googleusercontent.com/SWWwfIKlXyIRMBSkeoqK8bCLv-Y0Wl3ONVK5r_5Wwcg7401eA2n9G9dSBohazDBZhWu63QoIBBKF)

Currently I'm still testing the feedback of the motors with the shield. Once I finish it, I can apply the following equations to move the arm to the item's position (Thanks to my friend Abdallah Ezzat who helped me with their derivation):

![enter image description here](https://lh3.googleusercontent.com/GC3p60nHQhfIHNUj5Ith0vHgajUncHiXYhJ0igDdHhS58d3lBBFUKjmVh7iuzHq7oLP4bGCqdsLZ)

Demo for the arm's movement and center determining: 
![enter image description here](https://j.gifs.com/2x47MJ.gif)
