import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules import control as con
from modules import hw_init as hw

from settings import host,port

#import tts_module as tts
import time
from timeloop import Timeloop
from datetime import timedelta

import requests,json
from requests.exceptions import HTTPError

MODE_PREV = 0
MODE_NEXT = 1

def select_route_name(self):
    #처음엔 0 출력
    con.control(self.selected_num)

class Button():
    userId = ""
    state = "DEACTIVE"
    selected_route_name = ""
    selected_stn_id = ""
    selected_stn_name = ""
    current_stn_id = ""
    current_stn_name = ""
    selected_num = 0

    def __init__(self, userId):
        self.userId = userId
        self.state = "DEACTIVE"
        
    def GuardNumberRange(self,mode):
        if mode == MODE_PREV:
            if self.selected_num == 0:
                self.selected_num = 9
            else:
                self.selected_num -= 1
        else:
            if self.selected_num == 9:
                self.selected_num =0
            else:
                self.selected_num += 1

    def switch_prev_callback(self,channel):
        print("state:"+self.state)
        try:
            if len(self.state) > 3 and self.state[-3:] == "CHK":
                self.state = self.state[:-4]
                if self.state == "ROUTE_NAME":
                    self.selected_route_name = ""
                    print("노선 다시 선택")
                if self.state == "STN_NAME":
                    self.selected_stn_id = ""
                    self.selected_stn_name = ""
                    print("하차역 다시 선택")
                return
            elif len(self.state) <3:
                raise Exception("state value error")
        except Exception as e:
            print(e)
        
        if self.state == "STN_NAME":
            # TODO 버스정류장 선택
            print("")
            #노선 고르기
        if self.state == "ROUTE_NAME":
            self.GuardNumberRange(0)
            print("SELECTED_NUM"+str(self.selected_num))
            #con.control(SELECTED_NUM)  
            time.sleep(2)  

    def switch_next_callback(self,channel):
        print("state:"+self.state)
        # 노선 고르기
        if self.state == "ROUTE_NAME":
            self.GuardNumberRange(1)
            print("NUM : "+str(self.selected_num))
            #con.control(selected_num)
            time.sleep(2)
        if self.state == "STN_NAME":
            # TODO 버스정류장 선택
            print("")
    def switch_save_callback(self,channel):
        if self.state == "ROUTE_NAME":
            self.selected_route_name += str(self.selected_num)
            time.sleep(2)
            print("입력된 숫자 : "+str(self.selected_num))
            print("현재까지 저장된 노선 : "+str(self.selected_route_name))
            self.selected_num = 0

    def switch_done_callback(self,channel):
        print("state:"+self.state)
        # 승차 정류장 설정
        if self.state == "DEACTIVE":
            # GPS보내기
            pos_x,pos_y=hw.gps()
            dict_data = dict()
            dict_data['pos_x'] = pos_x
            dict_data['pos_y'] = pos_y
            url = host+'/api/gps/stn'
            res = requests.post(url,data=json.dumps(dict_data))

            self.current_stn_name = res.json()[0]['stn_name']
            self.current_stn_id = res.json()[0]['stn_id']

            print("승차 할 정류소가 \'"+self.current_stn_name+"\'가 맞습니까?\n")
            #tts.tts_input("승차할 정류소가 "+selected_stn_name+"가 맞습니까?")
            #TO DO : 승차 정류소가 맞다면 save, 아니면 pre 눌러서 분기--> 그 이후에 상태 바꾸기
            self.state = "DEACTIVE_CHK"

        # 승차 정류장 설정 확인
        elif self.state == "DEACTIVE_CHK":
            print("승차 정류장 설정 완료")
            #tts.tts_input("승차 정류장 설정이 완료되었습니다.")
            print("노선 번호를 입력하세요")
            self.state = "ROUTE_NAME"

        # 노선 입력
        elif self.state == "ROUTE_NAME":
            if self.selected_route_name != "":
                print("승차 노선이 "+self.selected_route_name+"가 맞습니까?\n")
                #tts.tts_input("승차 노선이 "+selected_route_name+"가 맞습니까?")
                self.state = "ROUTE_NAME_CHK"
            else:
                print("입력된 노선이 없습니다")
    
        # 노선 입력 확인
        elif self.state == "ROUTE_NAME_CHK":
            print("노선 설정 완료")
            #tts.tts_input("노선 설정이 완료되었습니다.")
            self.state = "STN_NAME"
            print("하차역을 설정하세요")

        # 하차벨 예약
        elif self.state == "STN_NAME":
        
            if self.selected_stn_id == "" or self.selected_route_name == "":
                self.state = "STN_NAME"
                print("유효하지 않은 역 또는 노선")
                
                return
            # else:               
            #     #하차벨 예약 중 누름
            #     tts.tts_input("성수역")

            dict_data = dict()
            dict_data['stn_id'] = self.selected_stn_id
            dict_data['route_nm'] = self.selected_route_name
            url = host+'/api/route-station-chk'
            data = requests.post(url,data=json.dumps(dict_data))
            if data.status_code != 200:
                print("해당 역이 노선에 없습니다.")
                print("하차역을 설정하세요")
                return
                
            print("status code : "+str(data.status_code)+"\n")

            print("노선 " + self.selected_route_name + " 과 정류장 이름 "+self.selected_stn_id+" 가 맞습니까? ")
            self.state = "STN_NAME_CHK"

        # 하차벨 예약 확인
        # elif state == "STN_NAME_CHK":
        #     dict_data = dict()
        #     dict_data['user_id'] = USER_ID
        #     dict_data['stn_id'] = selected_route_name
        #     dict_data['route_nm'] = selected_stn_id
        #     url = host+'/buzzer/register'
        #     data = requests.post(url,data=json.dumps(dict_data))
        #     status_data = data.status_code

        #     if str(status_data) == "200":
        #         # TODO : 몇분후에 도착하는지 알림
        #         print("n분 후에 도착 예정입니다. ")
        #         tts.tts_input("n분 후 도착 예정입니다.")
        #         state = "RUNNING"
        #     else :
        #         print("유효하지 않은 요청")
        #         tts.tts_input("잘못된 요청입니다.")
        #         state = "STN_NAME"
        #         selected_stn_id = ""
            
        # elif state == "RUNNING":
        #     state = "DEACTIVE"
        #     # TODO : 종료(?)

        # elif state == "ARRIVING":
        #     tts.tts_input("다음 정류장은"+ route_std_list[stn_num_to_dest-std_left_cnt]['stn_name']+"입니다.")
        # else:
        #     tts.tts_scenario(state)
        