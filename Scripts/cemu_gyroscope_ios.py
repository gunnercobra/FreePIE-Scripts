# IOS Gyroscope script for CEMU
# Requires FreePIE - http://andersmalmgren.github.io/FreePIE/
# Also requires - https://itunes.apple.com/us/app/sensor-data/id397619802 - Paid application, there might be free alternatives.
# Install it and run on your IOS device
# Recomended to run on FullScreen
# F2 to activate the plugin is the default key, check below

import ctypes
from ctypes import windll, Structure, c_ulong, byref, wintypes
import time

if starting:
	enabled = False
	
# Gets Window Size
hwnd = windll.user32.GetForegroundWindow()
currentwindow = ctypes.windll.dwmapi.DwmGetWindowAttribute

if currentwindow:
    rect = ctypes.wintypes.RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    currentwindow(
        ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect), ctypes.sizeof(rect))
    window_size = (rect.left, rect.top, rect.right, rect.bottom)

window_width = rect.left + rect.right
window_height = rect.top + rect.bottom
set_cursor = ctypes.windll.user32.SetCursorPos
	
# Toggle the script, default = F2
toggle = keyboard.getPressed(Key.F2)
if toggle:
	mouse.setButton(1,0)
	set_cursor((window_width / 2),(window_height / 2))	
	time.sleep(0.2)
	enabled = not enabled

# Right mouse click if enabled
if enabled:
	mouse.setButton(1,1)

# IOS gyro/accel inputs, roll and pitch are inverted to use it as landscape, yaw yet not implemented
roll = math.degrees(iPhone.roll)
pitch = math.degrees(iPhone.pitch)
#yaw = math.degrees(iPhone.yaw)

# sensitivity multiplier, < 1 lowers sensitivity, >1 hightens sensitivity
sens = 0.02
roll = roll * sens
pitch = pitch * sens
#yaw = yaw * sens

x_per = roll/1.5								# Converts axis to -1 to 1 scale
x_per = - x_per 								# Invert axis, comment to disable
window_width_total = window_width/2
x_value = window_width_total*x_per
x_coord = window_width_total - x_value
x_coord = filters.simple(x_coord, 0.5)
x_coord = int(round(x_coord))

y_per = pitch/1.5								# Converts axis to -1 to 1 scale
y_per = -y_per 									# Invert axis, comment to disable
window_height_total = window_height/2
y_value = window_height_total*y_per	
y_coord = window_height_total - y_value
y_coord = filters.simple(y_coord,  0.5)
y_coord = int(round(y_coord))

# Limits Roll to -1.5 to 1.5 scale
if 10 >= roll > 1.5:
	roll = 1.5
	
if -1.5 > roll or roll > 11:
	roll = -1.5
	
# Send mouse coordinates to window
if enabled :	
	set_cursor(x_coord ,y_coord)
	
# Diagnostics
diagnostics.watch(iPhone.roll)
diagnostics.watch(iPhone.pitch)
diagnostics.watch(iPhone.yaw)
diagnostics.watch(enabled)
#diagnostics.watch(x_per)
#diagnostics.watch(x_value)
#diagnostics.watch(x_coord)
#diagnostics.watch(y_per)
#diagnostics.watch(y_value)
#diagnostics.watch(y_value)
