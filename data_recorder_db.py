from socketIO_client import SocketIO, BaseNamespace
from tinydb import TinyDB, where
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
table_name=t.strftime('%Y-%m-%d-%s')
db = TinyDB("/home/pi/record_data/tinydb.json")
table = db.table(table_name)

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')
	
def update_json():
    global table, batt, head, roll, pitch, yaw, timestamp, img, waterTemp, depth, humid, hullTemp
    table.insert({"timestamp":timestamp, "image":img, "battery":batt, "heading":head, "roll":roll, "pitch":pitch, "yaw":yaw, "watertemp":waterTemp, "depth":depth, "humidity": humid, "hulltemp":hullTemp})

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
		yaw = item[1].split("\n")
		yaw = yaw[0]
    update_json()
    
def get_tables(*args):
    global db, socketIO
    print "get tables"
    all_tables = db.tables()
    json_tables = json.dumps(list(all_tables))
    socketIO.emit('table_names', json_tables)
    print "table names sent"
    
def get_table_data(*args):
    global db, socketIO
    table_of_interest = str(args[0])
    db_table = db.table(table_of_interest)
    json_table = json.dumps(db_table.all())
    socketIO.emit('table_of_interest', json_table)
		
def record():
    # do something here ...
    # call f() again in 60 seconds
#    with open(data_file, 'w') as f:
#	json.dump(json_var, f, ensure_ascii=False)
#    threading.Timer(10, record).start()
	print "NOOO"
    

socketIO = SocketIO('localhost', 8888, Namespace)
socketIO.on('arduino', on_arduino)
socketIO.on('mav', on_mav)
socketIO.on('getTables', get_tables)
socketIO.on('getTableData', get_table_data)

socketIO.wait()
