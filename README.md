# :oncoming_bus:BusDot Device:oncoming_bus:


### 시각장애인을 위한 버스 이용 보조 서비스 ‘버스닷’ by 함께타조:bird:
- 버스닷 시각장애인들이 버스정류장에 도착해서 버스를 탑승하고 하차하는데 불편함을 느끼지 않도록 도움을 주는 프로젝트입니다.


### 프로젝트 구성
1. [서버](https://github.com/yangjae33/tajo_backend)
2. [휴대폰 애플리케이션](https://github.com/seungyeonchoi/tajo_frontend)
3. [디바이스](https://github.com/yyoonsahng/2020ESWContest_free_1081/wiki)




### Architecture
<img src="https://user-images.githubusercontent.com/48347010/92088064-59620800-ee07-11ea-8ca7-ba0b4852c31a.png" width="500" height="600"/>





### 프로젝트 주요 특징 및 기능:zap:



- 주요 특징

1. 점자 시계를 통한 노선 설정 및 하차벨 예약
2. text to speech 을 활용한 음성 안내
3. GPS 기반 승차 지점 확인 및 하차 지점 도착 안내



- 주요 기능 별 사용 시나리오

1. 현재 위치한 정류소 확인 및 탑승할 노선 번호 입력

    - 입력한 버스 노선이 현재 위치한 정류소를 경유하는지 확인
    
    
2. 하차 정류소 예약

    - 입력한 버스 노선이 지나는 정류소 이름을 탑승 정류소부터 순차적으로 안내
    - 음성 안내에 따라 하차 정류소 예약

3.  하차 예정 정류소 10개 이전 정류소부터 남은 정류소 갯수를 점자로 안내

     - 음성 안내 버튼 누를 경우 정류소 이름 음성 안내

