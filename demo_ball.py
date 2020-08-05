from pyicubsim import iCubBall
import time

ball = iCubBall()

ball.set()
position = ball.get()
print([round(x) for x in position])

ball.set(y=position[2]+1)
position = ball.get()
print([round(x) for x in position])
