부킹 프로그램 개발 및 실행환경

1. 윈도우10 환경 + vscode

2. 아나콘다3 설치하여 파이썬 3.7 가상환경을 만듬 ex) 현재 'pyauto'로 되어 있음

3. 만들어진 가상환경에 requirements.txt 이용하여 관련 패키지 설치

4. config.py 파일에서 PROJECT_DIR 을 현재 소스파일이 있는 폴더로 지정
   현재는 PROJECT_DIR = 'C:/Users/iraboo/Documents/my_project/NewSeoul/' 로 되어 있음
   
5. newseoul.bat 에서 실행명령을 파일위치에 맞게 올바르게 수정
   현재는
   C:\users\iraboo\Anaconda3\envs\pyauto\python.exe C:\users\iraboo\documents\my_project\NewSeoul\newseoul.py
   python.exe 위치와 소스 위치를 수정해야함

6. newseoul.py에 예약하고 싶은 날짜와 시간대, 그리고 우선 예약하고 싶은 코스를 입력

7. 작업스케쥴러에 예약일 오전 9:50에 예약 프로그램(newseoul.bat)이 실행되도록 설정 (실제 예약은 10시에 진행)

