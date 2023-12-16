# trashcan
This trash can recognizes trash, opens the lid, and moves with motion recognition

카메라, 모터, LED, 서보
학습용 박스
카메라, LED, 디스플레이

<주기능>
1. 쓰레기통 열고 닫기 - 쓰레기 학습. (모터 1개)
	뚜껑에 압력센서 
2. 움직이기 - 보자기: 움직이기, 주먹: 멈추기 (모터 2개 아니면 3개)

<코드 구성>
1) button setting
2) servo setting
3) 움직임 분류 함수 move_classify
4) 쓰레기 분류 함수 trash_classify
5) 비디오캡처 시작
	5-1) 캡처 오류: 프로그램 종료
	5-2) 움직임 분류 실행
		5-2-1) 만약 go 라면, 움직이기
		5-2-2) 만약 stop 이라면, 멈추기
	5-3) 쓰레기 분류 실행
		5-3-1) 만약 trash 라면, 열리기
	5-4) 이미지 표시하기
	5-5) ESC 키가 눌리면 루프 종료
  
https://github.com/mariahwy/trashcan/assets/124486478/efd03482-5acd-48c0-8d91-3d25bf4eecec
