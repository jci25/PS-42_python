from socketIO_client import SocketIO, BaseNamespace
import threading, time, urllib, base64, json, datetime
img = ""
batt = 0
head = 0
roll = 0
pitch = 0
yaw = 0
waterTemp = 0
depth = 0
humid = 0
hullTemp = 0
timestamp = time.time()
t=datetime.datetime.fromtimestamp(timestamp)
data_file=t.strftime('%Y-%m-%d-%s.json')
json_str= '{"run_start": "'+str(timestamp)+'",  "data":[]}'
json_var = json.loads(json_str)

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')
	
def update_json():
    global batt, head, roll, pitch, yaw, timestamp, img, waterTemp, depth, humid, hullTemp
    json_var['data'].append({"timestamp":timestamp, "image":img, "battery":batt, "heading":head, "roll":roll, "pitch":pitch, "yaw":yaw, "watertemp":watertemp, "depth":depth, "humidity": humid, "hulltemp":hulltemp})

def on_arduino(*args):
    global waterTemp, depth, humid, hullTemp, timestamp
    timestamp = time.time()
    arduio = str(args[0])
    arduio = arduio.split(", ")
    for item in arduio:
    	item = item.split(": ")
    	if "WaterTemp " == item[0]:
		waterTemp = item[1]
	elif "Depth " == item[0]:
		depth = item[1]
	elif "Humidity " == item[0]:
		humid = item[1]
	elif "HullTemp " == item[0]:
		hullTemp = item[1]
    update_json()

def on_mav(*args):
    global batt, head, roll, pitch, yaw, timestamp, img
    timestamp = time.time()
    img = base64.b64encode(urllib.urlopen("http://127.0.0.1:8080/?action=snapshot").read())
    arduio = str(args[0])
    arduio = arduio.split(", ")
    for item in arduio:
    	item = item.split(": ")
    	if "Battery " == item[0]:
		batt = item[1]
	elif "Heading " == item[0]:
		head = item[1]
	elif "Roll " == item[0]:
		roll = item[1]
	elif "Pitch " == item[0]:
		pitch = item[1]
	elif "Yaw " == item[0]:
		yaw = item[1]
    update_json()
		
def record():
    # do something here ...
    # call f() again in 60 seconds
    print waterTemp
    with open(data_file, 'w') as f:
	json.dump(json_var, f, ensure_ascii=False)
    threading.Timer(10, record).start()
    
record()

socketIO = SocketIO('localhost', 8888, Namespace)
socketIO.on('arduino', on_arduino)
socketIO.on('mav', on_mav)
socketIO.wait()


