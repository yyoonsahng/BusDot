# :oncoming_bus:HamkkeTajo Device:oncoming_bus:


### 시각장애인을 위한 버스 이용 보조 서비스 ‘함께타조’:bird:
함께타조는 시각장애인들이 버스정류장에 도착해서 버스를 탑승하고 하차하는데 불편함을 느끼지 않도록 도움을 주는 프로젝트입니다.


### 프로젝트 구성
1. [서버](https://github.com/yangjae33/tajo_backend)
2. [휴대폰 애플리케이션](https://github.com/seungyeonchoi/tajo_frontend)
3. 디바이스

## :cherries:Device:cherries:
- 함께타조 프로젝트에서 라즈베리파이는 시각장애인이 버스를 편리하게 이용하기 위해 지참하는 디바이스 역할을 제공

디바이스의 기능
1. 서버와 GPS 정보 통신
2. 타고자하는 버스 번호를 입력받아 서버에게 전달
3. 서버로부터 정류장 데이터를 받아, 하차하고자하는 정류장 선택
4. 도착정류장까지 남은 정류장 수를 점자로 표현


### :warning: 사전 설정 :warning:
- 라즈베리 파이 오디오 출력 확인
	```
	 # 라즈비안 업데이트 
	 - sudo apt-get update
	 - sudo apt-get upgrade
	 - sudo apt-get install alsa-units
	
	 # 개인 실행 환경에 따라 사운드 출력 변경 (예 3.5mm audio jack)
	 - sudo amixer cset numid=3 1
	```
- 구글 cloud api 인증
	```
	export GOOGLE_APPLICATION_CREDENTIALS="[서비스 계정 키 파일 경로]"
	```
- 네트워크 환경 설정



### 서버와 GPS 통신:earth_asia:

- 다음 정류장의 id를 받아와서 next_stn_id에 저장
``` python
@tl.job(interval=timedelta(seconds=15))
def send_my_gps_info_15s(route_std_list):
    global next_stn_id
    global std_left_cnt
    url="/api/gps/stn"
    #현재 위치
    pos_x,pos_y=hw.gps()   
    params={"pos_y":pos_y,"pos_x":pos_x}

    #다음 정류장
    next_stn_id=route_std_list[stn_num_to_dest-std_left_cnt]['stn_id']
```


- 서버에 디바이스의 현재 위치를 보내서 디바이스와 가장 가까운 6개 정류소를 받아서 json 형식으로 stn_info_list에 저장
```python
    #Api 요청
    res=requests.post(host+url,data=json.dumps(params))
    stn_info_list=res.json()                   
```


- stn_info_list[0] (현재 GPS 위치에 따른 가장 가까운 정류장 id)과 next_stn_id (다음 정류장 id)가 같다면 next_stn_id를 그 다음 정류장으로 갱신
``` python
    if stn_info_list[0]['stn_id']==next_stn_id: #가장 가까운 정류장이 다음 정류장으로 바뀜
        std_left_cnt-=1
        next_stn_id=route_std_list[stn_num_to_dest-std_left_cnt]['stn_id']
        print("next station:"+next_stn_id)
        print("next station name"+route_std_list[stn_num_to_dest-std_left_cnt]['stn_name'])
    else:
        print("next station name"+route_std_list[stn_num_to_dest-std_left_cnt]['stn_name'])
        pass

    print ("15s job current time : {}".format(time.ctime()))

``` 


### 타고자하는 버스 번호를 입력받아 서버에게 전달:oncoming_bus:

- 이전 버튼을 누르면 수를 1 감소 (만약 0이라면 9로 감소)
``` python
def switch_prev_callback():
    print("switch_prev_callback")
    #노선 고르기
    if STATE == "ROUTE_NAME":
        GuardNumberRange(0)
        con.control(SELECTED_NUM)
        print("state: ROUTE_NAME")
``` 


- 다음 버튼을 누르면 수를 1 증가 (만약 9라면 0으로 증가)
``` python
def switch_next_callback():
    print("switch_next_callback")
    # 노선 고르기
    if STATE == "ROUTE_NAME":
        GuardNumberRange(1)
        con.control(SELECTED_NUM)
        print("state: ROUTE_NAME")
``` 


- 저장 버튼을 누르면 현재 자리수의 숫자를 SELECTED_ROUNTE_NAME에 추가
``` python
def switch_save_callback():
    global SELECTED_ROUNTE_NAME
    print("switch_save_callback")
    if STATE == "ROUTE_NAME":
        SELECTED_ROUNTE_NAME += str(SELECTED_NUM)
``` 


### 서버로부터 정류장 데이터를 받아, 하차하고자하는 정류장 선택:busstop:

- 인자로 받은 타고자 하는 버스 번호(bus_num)를 이용해 서버에 해당 버스의 노선 정보를 요청후 json 형식으로 전달받음

- json형식으로 받은 노선 정보를 버스 정류장 이름만 떼어내 리스트로 저장

- 인자로 받은 현재 위치한 버스정류장(curr_stn)을 이용해 해당 노선(리스트)에서 curr_stn이 위치한 index를 찾아서 ind 변수에 저장
``` python
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
``` 


### 도착정류장까지 남은 정류장 수를 점자로 표현:station:

- br에 사용할 GPIO 핀의 번호들을 저장

- br1 ~ br0까지 각 숫자에 따라 올라올 점자를 지정
``` python
br = [17, 18, 27, 22]
br1 = [17]
br2 = [17, 27]
br3 = [17, 18]
br4 = [17, 18, 22]
br5 = [17, 22]
br6 = [17, 18, 27]
br7 = [17, 18, 27, 22]
br8 = [17, 27, 22]
br9 = [18, 27]
br0 = [18, 27, 22]
numbers = [br1, br2, br3, br4, br5, br6, br7, br8, br9, br0]
``` 


- 점자로 올라오길 원하는 숫자를 인자로 받음

- 숫자에 해당하는 br에 저장된 GPIO 핀들에 전류를 흘려보냄

- X초 뒤 GPIO 핀들에 전류를 보내지 않음으로서 원상복귀
``` python
def control(num):#원하는 숫자의 점자 올라옴
	for pin in numbers[num - 1]:
		GPIO.output(pin, GPIO.HIGH)
	time.sleep(3)#원하는 시간만큼 점자 올라옴
	#clean
	for pin in numbers[num - 1]:
		GPIO.output(pin, GPIO.LOW)
	print("completed")
``` 


