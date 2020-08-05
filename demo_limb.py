from pyicubsim import iCubLimb
import time

app = '/demo'
right_arm = iCubLimb(app,'/icubSim/right_arm')
print([round(x) for x in right_arm.get()])
right_arm.set(joint1=85,joint3=40,joint2=40)
print([round(x) for x in right_arm.get()])
time.sleep(0.05)
print([round(x) for x in right_arm.get()])
time.sleep(0.05)
print([round(x) for x in right_arm.get()])
time.sleep(0.05)
print([round(x) for x in right_arm.get()])
time.sleep(2)
print([round(x) for x in right_arm.get()])
right_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))


