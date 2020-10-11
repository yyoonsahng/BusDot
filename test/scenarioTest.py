# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules import control as con
from modules import hw_init as hw

#import tts_module as tts
import time
from timeloop import Timeloop
from datetime import timedelta

import requests,json
from requests.exceptions import HTTPError

tl = Timeloop()

USER_ID = "root"

#시나리오 별 버튼 클릭 시 재생 문구
STATE_ANNOUNCEMENTS={}

STATE = "ROUTE_NAME" #ROUTE_NAME, DESTINATION, ...

# 현재 출력되고 있는 점자 숫자
SELECTED_NUM =0

#고른 노선
SELECTED_ROUTE_NAME = ""

#고른 하차 정류장
SELECTED_STN_NAME = ""
SELECTED_STN_ID = ""

#현재 정류장
CURRENT_STN_NAME = ""
CURRNET_STN_ID = ""

#전역 변수
host="http://114.70.21.89:1337"

#사전에 저장할 정보
route_std_list=[]               #승차 전 서버에서 받아 저장 (노선 별 버스 정류장 조회)
std_left_cnt=6                  #남은 정류장 수
stn_num_to_dest=7               #출발-목적지까지 갈 정류장 수

MODE_PREV = 0
MODE_NEXT = 1

def setup():
    global STATE, SELECTED_NUM, SELECTED_ROUTE_NAME, SELECTED_STN_NAME,SELECTED_STN_ID
    STATE = "DEACTIVE"
    SELECTED_NUM = 0
    SELECTED_ROUTE_NAME = ""
    SELECTED_STN_ID = "default station id"
    SELECTED_STN_NAME = "default station name"

#서버에 15초 마다 자신의 gps 정보 전송
@tl.job(interval=timedelta(seconds=15))
def send_my_gps_info_15s(route_std_list):
    global STATE
    global next_stn_id
    global std_left_cnt
   
    url="/api/gps/stn"
    
    #현재 위치
    pos_x,pos_y=hw.gps()   
    params={"pos_y":pos_y,"pos_x":pos_x}
    
    #다음 정류장
    next_stn_id=route_std_list[stn_num_to_dest-std_left_cnt]['stn_id']
    
    #Api 요청
    res=requests.post(host+url,data=json.dumps(params))
    stn_info_list=res.json()                    #자신과 가장 가까운 6개의 정류장 리스트 : stn_info_list
    
    if stn_info_list[0]['stn_id']==next_stn_id: #가장 가까운 정류장이 다음 정류장으로 바뀜
        std_left_cnt-=1
        
        if std_left_cnt<=10 and std_left_cnt >=0: #점자 버튼 안내 시작
            STATE="ARRIVING"
            # 점자 버튼 바꾸기
            con.control(std_left_cnt)
        elif std_left_cnt<0:
            print("system off")
            return
        next_stn_id=route_std_list[stn_num_to_dest-std_left_cnt]['stn_id']
        print("next station:"+next_stn_id)
        print("next station name"+route_std_list[stn_num_to_dest-std_left_cnt]['stn_name'])
    else:
        print("next station name"+route_std_list[stn_num_to_dest-std_left_cnt]['stn_name'])
        pass
    
  
    print ("15s job current time : {}".format(time.ctime()))

def GuardNumberRange(mode):
    global SELECTED_NUM
    if mode == MODE_PREV:
        if SELECTED_NUM == 0:
            SELECTED_NUM = 9
        else:
            SELECTED_NUM -= 1
    else:
        if SELECTED_NUM == 9:
            SELECTED_NUM =0
        else:
            SELECTED_NUM += 1

def select_route_name():
    #처음엔 0 출력
    con.control(SELECTED_NUM)


def switch_prev_callback(channel):
    global STATE
    global SELECTED_STN_ID
    global SELECTED_ROUTE_NAME
    global SELECTED_STN_NAME
    print("STATE:"+STATE)
    try:
        if len(STATE) > 3 and STATE[-3:] == "CHK":
            STATE = STATE[:-4]
            if STATE == "ROUTE_NAME":
                SELECTED_ROUTE_NAME = ""
                print("노선 다시 선택")
            if STATE == "STN_NAME":
                SELECTED_STN_ID = ""
                SELECTED_STN_NAME = ""
                print("하차역 다시 선택")
            return
        elif len(STATE) <3:
            raise Exception("STATE value error")
    except Exception as e:
        print(e)
    
    if STATE == "STN_NAME":
        # TODO 버스정류장 선택
        print("")

    #노선 고르기
    if STATE == "ROUTE_NAME":
        GuardNumberRange(0)
        print("SELECTED_NUM"+str(SELECTED_NUM))
        #con.control(SELECTED_NUM)  
        time.sleep(2)      

def switch_next_callback(channel):
    global STATE
    print("STATE:"+STATE)
    # 노선 고르기
    if STATE == "ROUTE_NAME":
        GuardNumberRange(1)
        print("NUM : "+str(SELECTED_NUM))
        #con.control(SELECTED_NUM)
        time.sleep(2)
    if STATE == "STN_NAME":
        # TODO 버스정류장 선택
        print("")

def switch_save_callback(channel):
    global SELECTED_ROUTE_NAME, SELECTED_NUM
    if STATE == "ROUTE_NAME":
        SELECTED_ROUTE_NAME += str(SELECTED_NUM)
        time.sleep(2)
        print("입력된 숫자 : "+str(SELECTED_NUM))
        print("현재까지 저장된 노선 : "+str(SELECTED_ROUTE_NAME))
        SELECTED_NUM = 0
def switch_tts_callback(channel):
    tts.tts_scenario(STATE)
def switch_done_callback(channel):

    global STATE
    global USER_ID
    global SELECTED_STN_ID
    global SELECTED_STN_NAME
    global SELECTED_ROUTE_NAME
    global CURRENT_STN_NAME, CURRNET_STN_ID
        
    print("STATE:"+STATE)
    # 승차 정류장 설정
    if STATE == "DEACTIVE":
        
        # GPS보내기
        pos_x,pos_y=hw.gps()
        dict_data = dict()
        dict_data['pos_x'] = pos_x
        dict_data['pos_y'] = pos_y
        url = host+'/api/gps/stn'
        res = requests.post(url,data=json.dumps(dict_data))

        CURRENT_STN_NAME = res.json()[0]['stn_name']
        CURRENT_STN_ID = res.json()[0]['stn_id']

        print("승차 할 정류소가 \'"+CURRENT_STN_NAME+"\'가 맞습니까?\n")
        #tts.tts_input("승차할 정류소가 "+SELECTED_STN_NAME+"가 맞습니까?")
        #TO DO : 승차 정류소가 맞다면 save, 아니면 pre 눌러서 분기--> 그 이후에 상태 바꾸기
        STATE = "DEACTIVE_CHK"

    # 승차 정류장 설정 확인
    elif STATE == "DEACTIVE_CHK":
        print("승차 정류장 설정 완료")
        #tts.tts_input("승차 정류장 설정이 완료되었습니다.")
        print("노선 번호를 입력하세요")
        STATE = "ROUTE_NAME"

    # 노선 입력
    elif STATE == "ROUTE_NAME":
        if SELECTED_ROUTE_NAME != "":
            print("승차 노선이 "+SELECTED_ROUTE_NAME+"가 맞습니까?\n")
            #tts.tts_input("승차 노선이 "+SELECTED_ROUTE_NAME+"가 맞습니까?")
            STATE = "ROUTE_NAME_CHK"
        else:
            print("입력된 노선이 없습니다")
   
    # 노선 입력 확인
    elif STATE == "ROUTE_NAME_CHK":
        print("노선 설정 완료")
        #tts.tts_input("노선 설정이 완료되었습니다.")
        STATE = "STN_NAME"
        print("하차역을 설정하세요")

    # 하차벨 예약
    elif STATE == "STN_NAME":
    
        if SELECTED_STN_ID == "" or SELECTED_ROUTE_NAME == "":
            STATE = "STN_NAME"
            print("유효하지 않은 역 또는 노선")
            
            return
        # else:               
        #     #하차벨 예약 중 누름
        #     tts.tts_input("성수역")

        dict_data = dict()
        dict_data['stn_id'] = SELECTED_STN_ID
        dict_data['route_nm'] = SELECTED_ROUTE_NAME
        url = host+'/api/route-station-chk'
        data = requests.post(url,data=json.dumps(dict_data))
        if data.status_code != 200:
            print("해당 역이 노선에 없습니다.")
            print("하차역을 설정하세요")
            return
            
        print("status code : "+str(data.status_code)+"\n")

        print("노선 " + SELECTED_ROUTE_NAME + " 과 정류장 이름 "+SELECTED_STN_ID+" 가 맞습니까? ")
        STATE = "STN_NAME_CHK"

    # 하차벨 예약 확인
    # elif STATE == "STN_NAME_CHK":
    #     dict_data = dict()
    #     dict_data['user_id'] = USER_ID
    #     dict_data['stn_id'] = SELECTED_ROUTE_NAME
    #     dict_data['route_nm'] = SELECTED_STN_ID
    #     url = host+'/buzzer/register'
    #     data = requests.post(url,data=json.dumps(dict_data))
    #     status_data = data.status_code

    #     if str(status_data) == "200":
    #         # TODO : 몇분후에 도착하는지 알림
    #         print("n분 후에 도착 예정입니다. ")
    #         tts.tts_input("n분 후 도착 예정입니다.")
    #         STATE = "RUNNING"
    #     else :
    #         print("유효하지 않은 요청")
    #         tts.tts_input("잘못된 요청입니다.")
    #         STATE = "STN_NAME"
    #         SELECTED_STN_ID = ""
        
    # elif STATE == "RUNNING":
    #     STATE = "DEACTIVE"
    #     # TODO : 종료(?)

    # elif STATE == "ARRIVING":
    #     tts.tts_input("다음 정류장은"+ route_std_list[stn_num_to_dest-std_left_cnt]['stn_name']+"입니다.")
    # else:
    #     tts.tts_scenario(STATE)
    
if __name__ == "__main__":
    # GPIO 초기화 (GPS,Solenoid, Switch) - 이벤트 핸들러 등록
    hw.init(switch_prev_callback, switch_next_callback,switch_save_callback, switch_done_callback,switch_tts_callback)
    setup()
    # STATE_ANNOUNCEMENTS=tts.get_tts_scenario() 
    # tl.start(block=False)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        hw.destroy()


