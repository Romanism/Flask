# Flask를 사용하기 위해선 먼저 Flask를 import해줘야 함
from flask import Flask 

app = Flask(__name__)
""" 
- import한 클래스를 객체화 시켜서 app이라는 변수에 저장
- 이 app 변수가 API 애플리케이션 (Flask 앱 애플리케이션)
- app 변수에 API의 설정과 엔드포인트들을 추가하면 API 완성
"""

@app.route("/ping", methods=["GET"])
""" 
- Flask의 route 데코레이터를 사용해 엔드포인트(/ping)를 등록
- 고유주소는 ping이며 HTTP 메소드는 GET으로 설정
"""
def ping():
    """ 
    - ping 함수를 정의 (pong이라는 string을 반환하도록)
    - 이러면 Flask가 알아서 HTTP 응답(response)로 변환해 HTTP 요청(request)을 보낸 클라이언트에게 전송
    """
    return "pong"


# FLASK_APP=introduce.py FLASK_DEBUG=1 flask run 로 실행