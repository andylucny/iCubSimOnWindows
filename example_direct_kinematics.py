# Edited by Francesco Nori
# Genova Jan 2008
# This function computes the iCub right arm forward kinematic as
# described by the CAD files. The kinematics include the 
# iCub waist. Parameters are given according to the DH notation. 
# Global forward kinematic is given by T_Ro0 * T_0n.
import numpy as np
from numpy import cos
from numpy import sin
from numpy import pi

def DH(a, d, alph, thet):
    return np.array([ \
        [ cos(thet), -sin(thet)*cos(alph),  sin(thet)*sin(alph), cos(thet)*a], \
        [ sin(thet),  cos(thet)*cos(alph), -cos(thet)*sin(alph), sin(thet)*a], \
        [         0,            sin(alph),            cos(alph),           d], \
        [         0,                    0,                    0,           1] \
    ])
                    
#
# Usage:
#       wtheta = (wtheta0, wtheta1, wtheta2)
#       wtheta0: torso_pitch
#       wtheta1: torso_roll
#       wtheta2: torso_yaw
#
#       rtheta = (rtheta0, rtheta1, rtheta2, rtheta3, rtheta4, rtheta5, rtheta6)
#       rtheta0: shoulder_pitch
#       rtheta1: shoulder_roll
#       rtheta2: shoulder_yaw
#       rtheta3: elbow
#       rtheta4: wrist_prosup
#       rtheta5: wrist_pitch
#       rtheta6: wirst_yaw
#
#       return (x,y,z)
def direct_kinematics_right_arm(wtheta,rtheta):

    ljnt = 20  #joint pic length
    rjnt = 5   #joint pic radius

    wtheta0 = wtheta[2]
    wtheta1 = wtheta[1]
    wtheta2 = wtheta[0]

    G_01 = DH(      32,       0,     pi/2,     wtheta0)
    G_12 = DH(       0,    -5.5,     pi/2,     wtheta1-pi/2)
    G_23 = DH(-23.3647,  -143.3,     pi/2,     wtheta2 - 15*pi/180 - pi/2 )

    theta0 = rtheta[0]
    theta1 = rtheta[1]
    theta2 = rtheta[2]
    theta3 = rtheta[3]
    theta4 = rtheta[4]
    theta5 = rtheta[5]
    theta6 = rtheta[6]

    G_34=DH(    0, -107.74,     pi/2,    theta0-pi/2)
    G_45=DH(    0,       0,    -pi/2,    theta1-pi/2)
    G_56=DH(  -15, -152.28,    -pi/2,    theta2-pi/2-15*pi/180) 
    G_67=DH(   15,       0,     pi/2,    theta3) 
    G_78=DH(    0,  -137.3,     pi/2,    theta4-pi/2) 
    G_89=DH(    0,       0,     pi/2,    theta5+pi/2) 
    G_910=DH( 62.5,     16,        0,    theta6+pi) 

    T_Ro0 = np.array([[0,-1,0,0],[0,0,-1,0],[1,0,0,0],[0,0,0,1]])
    T_0n  = G_01.dot(G_12).dot(G_23).dot(G_34).dot(G_45).dot(G_56).dot(G_67).dot(G_78).dot(G_89).dot(G_910)
    XE = np.transpose(np.array([[0,0,0,1]]))
    pos = T_Ro0.dot(T_0n).dot(XE)

    return (pos[0][0],pos[1][0],pos[2][0])

import time
from pyicubsim import iCubLimb

right_arm = iCubLimb('/direct_kinematics','/icubSim/right_arm')
while True:
    joints = right_arm.get()
    #print(joints)
    joints = tuple([x*pi/180.0 for x in joints]) #degrees to radians
    pos = direct_kinematics_right_arm((0,0,0),(joints[0],joints[1],joints[2],joints[3],joints[4],joints[5],joints[6]))
    print('x (to back) = %1.2f, y (to left) = %1.2f, z (up) = %1.2f' % pos)
    time.sleep(0.5)
