# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 01:33:57 2020

@author: tarah
"""
#37.5663° N, 126.9779° E

import RPI.GPIO as GPIO
#import tts
#import stt

SWITCH_TTS=23
SWITCH_STT=21
GPS=24

def HW_INIT():
    
    GPIO.setmode(GPIO.BCM)
    
    #initialize pins
    GPIO.setup(SWITCH_TTS,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_STT,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    #add eventHandler
    GPIO.add_event_detect(SWITCH_TTS,GPIO.RISING,callback=switch_tts_callback)
    GPIO.add_event_detect(SWITCH_STT,GPIO.RISING,callback=switch_stt_callback)

def switch_stt_callback(channel):
    #stt(next_stn_name) : 마이크 작동 > 텍스트로 변환
    print("stt")
def switch_tts_callback(channel):
    #tts() : 녹음 파일을 재생
    print("tts")
def gps():
    pos_x="126.9786567859"
    pos_y="37.5668260055"
    
    return pos_x,pos_y