import requests
import json

HOST = '114.70.21.89'
PORT = '1337'

url_prefix = 'http://'+HOST+":"+PORT

# 시나리오 : 승차 정류장 주변에서 / 처음 확인 버튼 입력 시 / 
# Input : cur_x, cur_y (GPS module)
# Response : stn_id, stn_name (가장 가까운 정류장)
print("# 1")
cur_x = 127.168
cur_y = 37.556
dict_data = dict()
dict_data['pos_x'] = cur_x
dict_data['pos_y'] = cur_y
url = url_prefix+'/api/gps/stn'
res = requests.post(url,data=json.dumps(dict_data))
print(">> 승차 위치로 \'"+res.json()[0]['stn_name']+"\'가 맞습니까?\n")

# 시나리오: 배열 앞 뒤
# 해당 정류장을 지나는 노선이 경유하는 모든 정류장을 보고 사용자가 선택
# Input : route_nm
# Response : list of stn
print("# 2")
route_nm = 106
url = url_prefix+'/api/route-station/'+str(route_nm)
data = requests.get(url)
#data = requests.post(HOST+":"+PORT+'/users')
json_data = dict()
json_data = data.json()
print(">> 노선이 지나는 역 : ",end="")
flag = 0
for i in json_data:
    print(i['stn_name'],end="")
    if flag == 2:
        break
    print(", ",end="")
    flag = flag+1

print("...\n")

# 시나리오 : #1, #2 이후 하차벨 예약
# Input : user_id, stn_id, route_nm
print("# 3")

user_id = "root"
route_nm = "146"
stn_id = "110000346"
dict_data = dict()
dict_data['user_id'] = user_id
dict_data['stn_id'] = stn_id
dict_data['route_nm'] = route_nm
url = url_prefix+'/buzzer/register'
data = requests.post(url,data=json.dumps(dict_data))
status_data = data.status_code
print("status code : "+str(status_data)+"\n")
# TODO print(">> 남은 시간 : "+data.json()['left_time'])

# 시나리오 : 승차 후
# Input : cur_x, cur_y (GPS module)
print("# 4")
cur_x = 127.168
cur_y = 37.556
dict_data = dict()
dict_data['pos_x'] = cur_x
dict_data['pos_y'] = cur_y
url = url_prefix+'/api/gps/stn'
res = requests.post(url,data=json.dumps(dict_data))
print(res.json()[0])