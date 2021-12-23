import spidev # SPI
from flask import Flask, render_template # Web Flask
import cv2 # opencv
import numpy as np # DNN
import time

#----------------------------------SPI----------------------------------
# SPI 인스턴스 생성 
spi = spidev.SpiDev()

# SPI 통신 시작
spi.open(0, 0) # bus: 0, dev: 0(CE0, CE1 둘 중 하나가 0임)

# SPI 최대 통신 속도 설정
spi.max_speed_hz = 100000

# 채널에서 읽어온 아날로그값을 디지털로 변환하여 리턴하는 함수
def analog_read(channel):
    #[byte_1, byte_2, byte_3]
    #byte_1 : 1
    #byte_2 : channel(0) + 8 = 0000 1000(2진수) << 4 - > 1000 0000
    #byte_3 : 0
    ret = spi.xfer2([1, (channel + 8) << 4, 0])
    adc_out = ((ret[1] & 3) << 8) + ret[2]
    return adc_out
#----------------------------------SPI----------------------------------

#----------------------------------CV2----------------------------------
# model, config, classFile 설정
model = './dnn/bvlc_googlenet.caffemodel'
config = './dnn/deploy.prototxt'
classFile = './dnn/classification_classes_ILSVRC2012.txt'

classNames = None
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Load a pre-trained neural network
net = cv2.dnn.readNet(model, config)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed')
    exit()
#----------------------------------CV2----------------------------------

#----------------------------------FLASK--------------------------------
app = Flask(__name__)
species = "None"

@app.route("/")
def main():
    return render_template("adminv2.html")

@app.route("/manage") # 5초마다 반복
def manage(): 
    try:
        reading = analog_read(0)

        if reading < 1023: # 조도센서 값이 일정 값 이하일 때 True
            ref, frame = cap.read() # 사진 촬영
            
            # blob 이미지 생성
            blob = cv2.dnn.blobFromImage(frame, scalefactor=1, size=(224, 224), mean=(104, 117, 123))

            # blob 이미지를 네트워크 입력으로 설정
            net.setInput(blob)

            # 네트워크 실행 (순방향)
            detections = net.forward()

            # 가장 높은 값을 가진 클래스 얻기
            out = detections.flatten()
            classId = np.argmax(out)
            confidence = out[classId]

            # species 변수에 종 이름 기입
            species = classNames[classId]
            
            # 화면에 5초간 사진 띄우기
            cv2.imshow('frame', frame)
            cv2.waitKey(5000)

            return species

        else: # 일정 값 초과 시 오전으로 간주하고 False
            return "Not afternoon"
    except Exception as e:
        print(e)



if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    finally:
        spi.close()
        cap.release()
        cv2.destroyAllWindows()
#----------------------------------FLASK--------------------------------
