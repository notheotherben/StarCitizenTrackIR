# You can use this script with FreePIE, it'll try and clamp the resulting values to rational ranges.

import sys

def toIntSafe(value):
    if value > sys.maxint: return sys.maxint
    if value < -sys.maxint: return -sys.maxint
    return value

def update():
	yaw = filters.mapRange(trackIR.yaw, -90, 90, -vJoy[0].axisMax, vJoy[0].axisMax)
	pitch = filters.mapRange(trackIR.pitch, -90, 90, -vJoy[0].axisMax, vJoy[0].axisMax)
	roll = filters.mapRange(trackIR.roll, -50, 50, -vJoy[0].axisMax, vJoy[0].axisMax)

	vJoy[0].x = toIntSafe(yaw)
	vJoy[0].y = toIntSafe(pitch)
	vJoy[0].z = toIntSafe(roll)

if starting:
    trackIR.update += update
