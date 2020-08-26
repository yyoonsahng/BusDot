# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 04:16:22 2020

@author: tarah
"""
import control as con
import hw_init as hw
import time
from timeloop import Timeloop
from datetime import timedelta

import requests,json
from requests.exceptions import HTTPError

tl = Timeloop()

#시나리오별 state
STATE = "ROUTE_NAME" #ROUTE_NAME, DESTINATION, ...

# 현재 출력되고 있는 점자 숫자
SELECTED_NUM =0

#고른 노선
SELECTED_ROUNTE_NAME = ""
#전역 변수
host="http://114.70.21.89:1337"

#사전에 저장할 정보
route_std_list=[]               #승차 전 서버에서 받아 저장 (노선 별 버스 정류장 조회)
std_left_cnt=6                  #남은 정류장 수
stn_num_to_dest=7               #출발-목적지까지 갈 정류장 수

#서버에 15초 마다 자신의 gps 정보 전송
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
    
    #Api 요청
    res=requests.post(host+url,data=json.dumps(params))
    stn_info_list=res.json()                    #자신과 가장 가까운 6개의 정류장 리스트 : stn_info_list
    
    if stn_info_list[0]['stn_id']==next_stn_id: #가장 가까운 정류장이 다음 정류장으로 바뀜
        std_left_cnt-=1
        next_stn_id=route_std_list[stn_num_to_dest-std_left_cnt]['stn_id']
        print("next station:"+next_stn_id)
        print("next station name"+route_std_list[stn_num_to_dest-std_left_cnt]['stn_name'])
    else:
        print("next station name"+route_std_list[stn_num_to_dest-std_left_cnt]['stn_name'])
        pass
    
    print ("15s job current time : {}".format(time.ctime()))

'''
mode
0: prev
1: next
'''
def GuardNumberRange(mode):
    global SELECTED_NUM
    if mode == 0:
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


def switch_prev_callback():
    print("switch_prev_callback")
    #노선 고르기
    if STATE == "ROUTE_NAME":
        GuardNumberRange(0)
        con.control(SELECTED_NUM)
        print("state: ROUTE_NAME")



def switch_next_callback():
    print("switch_next_callback")
    # 노선 고르기
    if STATE == "ROUTE_NAME":
        GuardNumberRange(1)
        con.control(SELECTED_NUM)
        print("state: ROUTE_NAME")

def switch_save_callback():
    global SELECTED_ROUNTE_NAME
    print("switch_save_callback")
    if STATE == "ROUTE_NAME":
        SELECTED_ROUNTE_NAME += str(SELECTED_NUM)

def switch_done_callback():
    print("switch_done_callback")



def main():
    # GPIO 초기화 (GPS,Solenoid, Switch) - 이벤트 핸들러 등록
   # hw.hw_init()
    hw.init(switch_prev_callback, switch_next_callback,switch_save_callback, switch_done_callback)
    print("please")
    tl.start(block=False)
    print("wow2")

    
if __name__ == "__main__":
    main()