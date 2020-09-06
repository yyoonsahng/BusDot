# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 01:33:57 2020

@author: tarah
"""
#37.5663° N, 126.9779° E

import RPi.GPIO as GPIO
#import tts
#import stt

SWITCH_PREV=21 #이전
SWITCH_NEXT=22 #다음
SWITCH_SAVE=23 #저장
SWITCH_DONE=24 #확인

SWITCH_TTS=25
SWITCH_STT=26
GPS=24


def init(switch_prev_callback, switch_next_callback,  switch_save_callback, switch_done_callback):
    GPIO.setmode(GPIO.BCM)

    # initialize pins
    GPIO.setup(SWITCH_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_SAVE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_DONE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(SWITCH_TTS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_STT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # add eventHandler
    GPIO.add_event_detect(SWITCH_PREV, GPIO.RISING, callback=switch_prev_callback)
    GPIO.add_event_detect(SWITCH_NEXT, GPIO.RISING, callback=switch_next_callback)
    GPIO.add_event_detect(SWITCH_SAVE, GPIO.RISING, callback=switch_save_callback)
    GPIO.add_event_detect(SWITCH_DONE, GPIO.RISING, callback=switch_done_callback)

    GPIO.add_event_detect(SWITCH_TTS, GPIO.RISING, callback=switch_tts_callback)
    GPIO.add_event_detect(SWITCH_STT, GPIO.RISING, callback=switch_stt_callback)

def myinit():
    
    GPIO.setmode(GPIO.BCM)
    
    #initialize pins
    GPIO.setup(SWITCH_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_TTS,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_STT,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    #add eventHandler

    GPIO.add_event_detect(SWITCH_TTS,GPIO.RISING,callback=switch_tts_callback)
    GPIO.add_event_detect(SWITCH_STT,GPIO.RISING,callback=switch_stt_callback)

def destroy():
    GPIO.cleanup()

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
