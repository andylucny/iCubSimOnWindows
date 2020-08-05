from pyicubsim import iCubEmotion
import time

emotion = iCubEmotion()

print('neutral')
emotion.set(emotion.neutral)
time.sleep(2)

print('happy')
emotion.set(emotion.happy)
time.sleep(2)

print('sad')
emotion.set(emotion.sad)
time.sleep(2)

print('surprised')
emotion.set(emotion.surprised)
time.sleep(2)

print('angry')
emotion.set(emotion.angry)
time.sleep(2)

print('evil')
emotion.set(emotion.evil)
time.sleep(2)

print('shy')
emotion.set(emotion.shy)
time.sleep(2)

print('cunning')
emotion.set(emotion.cunning)
time.sleep(2)

emotion.set(emotion.happy)
