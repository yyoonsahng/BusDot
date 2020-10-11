# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 07:33:17 2020

@author: tarah
"""
from google.cloud import texttospeech
import os,sys
import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../static/stt-test-283506-48b71d92f7f6.json"

def get_tts_scenario():
    scene_dict={} #전역 & 초기화
    with open('../static/test.txt',encoding='UTF-8') as f: 
        for line in f:
            li=line.split(":")
            key,value=li[0],li[1].strip()
            scene_dict[key]=value
    print(scene_dict)
    return scene_dict
    #scene_df=pd.read_csv("./tts_scenario.csv",index_col='SCENE')
    #scene_dict=scene_df.to_dict()
    #scene_dict=scene_dict['TEXT']
    #return scene_dict
   
def tts_input(texttospeak):
    #print("synthesize {} to sound".format(texttospeak))
    texttospeak+="아아"
    synthesis_input = texttospeech.SynthesisInput(text=texttospeak)
    tts_control(synthesis_input)
    print("complete the task")
    
def tts_scenario(state):
    state_dict=get_tts_scenario()
    tts_text=state_dict[state]
    synthesis_input = texttospeech.SynthesisInput(text=tts_text)
    tts_control(synthesis_input)
    print("complete the task")
    
def tts_control(synthesis_input):
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    #synthesis_input = texttospeech.SynthesisInput(text=texttospeak)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Playing sound...')
 

    os.system('omxplayer ./output.mp3')

    #sys.exit()


    
if __name__ == "__main__":
    #run_quickstart()
    tts_input("안녕하세용 반가워용")
    #tts_scenario("STN_NAME")
