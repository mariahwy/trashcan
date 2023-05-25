import sys
import cv2
# 텐서플로lite 라이브러리 import
from tflite_support.task import core, vision
# grove 센서 import
from grove.grove_servo import GroveServo # servo
from grove.grove_button import GroveButton # button
import time

# servo 관련 setting
servoL = GroveServo(12)
servoR = GroveServo(5)
servo = GroveServo(16)

# button 관련 setting
PIN = 18
button = GroveButton(PIN)

def on_press(t):
    servo.setAngle(90)
    
def on_release(t):
    servo.setAngle(90)

# 움직임 classify() 모델, 분류목록, 분류할 이미지를 입력하면 가장 가능성있는 분류명, 가능성 리턴
def move_classify(model, labels, image): # -> (label, probability)
    
    # classifier에 사용할 모델 설정
    classifier_options = vision.ImageClassifierOptions(base_options=core.BaseOptions(file_name=move_model)) # move_model
    classifier = vision.ImageClassifier.create_from_options(classifier_options)
    
    # 텐서플로우 이미지로 변환
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tensor_image = vision.TensorImage.create_from_array(rgb_image)
    
    # 분류 실행
    result = classifier.classify(tensor_image)
    
    # 결과 정리
    category = result.classifications[0].categories[0]
    category_name = labels[category.index]
    probability = round(category.score, 2)
    
    return (category_name, probability)


# 쓰레기 classify() 모델, 분류목록, 분류할 이미지를 입력하면 가장 가능성있는 분류명, 가능성 리턴
def trash_classify(model, labels, image): # -> (label, probability)
    
    # classifier에 사용할 모델 설정
    classifier_options = vision.ImageClassifierOptions(base_options=core.BaseOptions(file_name=trash_model))
    classifier = vision.ImageClassifier.create_from_options(classifier_options)
    
    # 텐서플로우 이미지로 변환
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tensor_image = vision.TensorImage.create_from_array(rgb_image)
    
    # 분류 실행
    result = classifier.classify(tensor_image)
    
    # 결과 정리
    category = result.classifications[0].categories[0]
    category_name = labels[category.index]
    probability = round(category.score, 2)
    
    return (category_name, probability)


def main():
    button.on_press = on_press
    button.on_release = on_release

    # 모델파일 지정
    move_model = 'move_model.tflite'
    trash_model = 'trash_model.tflite'
    
    # move 레이블 파일을 읽어 리스트로
    move_label = open('move_labels.txt', 'r')
    move_labels = move_label.readlines()
    move_label.close()
    
    # trash 레이블 파일을 읽어 리스트로
    trash_label = open('trash_labels.txt', 'r')
    trash_labels = trash_label.readlines()
    trash_label.close()
    
    # 비디오 캡쳐 시작
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224) # 가로 224px
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224) # 세로 224px

    while cap.isOpened():
        success, image = cap.read() 
        # 캡쳐 오류시 프로그램 종료
        if not success: 
            sys.exit('ERROR: Please verify your webcam settings.')
        # 이미지 좌우 반전
        image = cv2.flip(image, 1)
        
        # image로 move 분류 실행
        move_prediction = move_classify(move_model, move_labels, image)
        report_text1 = move_prediction[0]+str(move_prediction[1]*100)+'%'

        # 만약 go라면 움직이고, stop이라면 멈추기
        if move_prediction[0] == move_labels[0]:
            #move
            # 왼쪽
            servoL.setAngle(0)
          
            #오른쪽
            servoR.setAngle(180)
            
        else:
            #stop
            # 왼쪽
            servoL.setAngle(90)
            # 오른쪽
            servoR.setAngle(90)

        # image로 trash 분류 실행
        trash_prediction = trash_classify(trash_model, trash_labels, image)
        report_text2 = trash_prediction[0]+str(trash_prediction[1]*100)+'%'

        # 만약 trash라면 열고, 아니면 가만히 있고, 압력센서가 눌리면 닫기
        if trash_prediction[0] == trash_labels[0]:
            servo.setAngle(180)

        
        # 이미지 표시하기
        cv2.imshow('trashcan', image)

        # ESC 키가 눌리면 루프 종료
        if cv2.waitKey(1) == 27:
            break
    
    cap.release() # 영상 캡쳐 중지
    cv2.destroyAllWindows() # 윈도우 닫기

if __name__=='__main__':
    main()
