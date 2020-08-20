import requests
#import RPi.GPIO as GPIO
bus_stop = []
ind = 0
state = 0
def selectStation(bus_num, curr_stn):
    global bus_stop
    global ind
    url = 'http://localhost:1337/api/route-station/' + str(bus_num)
    response = requests.get(url)
    res = response.json()
    for i in res:
        bus_stop.append(i['stn_name'])
    #print(bus_stop)
    ind = bus_stop.index(curr_stn)
    #print(ind)
'''
def setup():
    global state
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(18, GPIO.RISING, callback=move_right)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.RISING, callback=move_left)
'''


def move_right():
    global ind
    global state
    ind += 1
    curr_stop = bus_stop[ind]

def move_left():
    global ind
    global state
    ind -= 1
    curr_stop = bus_stop[ind]

if __name__ == '__main__':
    selectStation(143, '신동중학교')
    #setup()
    print(bus_stop)
    print(ind)