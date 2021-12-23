 # 7segment.py
 import RPi.GPIO as GPIO
 import time

 # GPIO 7개 Pin 번호 설정
 #              A  B  C  D  E  F  G
SEGMENT_PINS = [2, 3, 4, 5, 6, 7, 8]

GPIO.setmode(GPIO.BCM)

for segment in SEGMENT_PINS:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)

data =[1, 1, 1, 1, 1, 1, 0]

try:
    for _ in range(3):  #0~2
        # 0 출력
        for i in range(7):  # 0~6
            GPIO.output(SEGMENT_PINS[i], data[i])

    time.sleep(1)

    # 0 출력 끄기
    for i in range(7): # 0~6
        GPIO.output(SEGMENT_PINS[i], GPIO.LOW)  



# data = [[1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 0, 0, 1, 1]]  # 9
