import subprocess
mav_txt = subprocess.check_output("tail -n 20 ~/tmp.out", shell=True)
mav_txt = mav_txt.split("\n")
battery = -99
heading = -99
roll = -99
pitch = -99
yaw = -99
for line in mav_txt:
	if "SYS_STATUS" in line:
		tmp1 = line.split(",")
		for item in tmp1:
			if "battery_remaining" in item:
				tmp2 = item.split(" : ")
				battery = tmp2[1]
	if "VFR_HUD" in line:
		tmp1 = line.split(",")
		for item in tmp1:
			if "heading" in item:
				tmp2 = item.split(" : ")
				heading = tmp2[1]
	if "ATTITUDE" in line:
		tmp1 = line.split(",")
		for item in tmp1:
			if "roll " in item:
				tmp2 = item.split(" : ")
				roll = tmp2[1]
			elif "pitch " in item:
				tmp2 = item.split(" : ")
				pitch = tmp2[1]
			elif "yaw " in item:
				tmp2 = item.split(" : ")
				yaw = tmp2[1]

print "Battery : " + "{0:.2f}".format(float(battery)) + ", Heading : " + heading+ ", Roll : " + "{0:.5f}".format(float(roll))+ ", Pitch : " + "{0:.5f}".format(float(pitch))+ ", Yaw : " + "{0:.5f}".format(float(yaw))
