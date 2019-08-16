""" 
Mini Twiter

1. 회원가입
2. 로그인
3. 트윗
4. 다른 회원 팔로우하기
5. 다른 회원 언팔로우하기
6. 타임라인
""" 


from flask import Flask, jsonify, request
from flask.json import JSONEncoder
""" 
- request : 사용자가 HTTP를 통해 전송한 JSON 데이터를 읽어들일 수 있음
- jsonify : dictionary 객체를 JSON으로 변환하여 HTTP 응답으로 보낼 수 있음
- JSONEncoder : JSONEncoder 클래스 확장해서 커스텀 인코더를 구현
"""


app = Flask(__name__)
app.users = {} # 새로 가입한 사용자를 저장할 dictionary를 user란 변수에 저장
app.id_count = 1 # 사용자의 id값을 설정 (가입할때마다 1씩 늘어날 예정)
app.tweets = [] # 사용자들의 트윗을 저장할 디렉터리


# set이 JSON으로 변경하지 못하는것을 해결하기 위한 모듈 직접 생성
class CustomJSONEncoder(JSONEncoder):
    """ 
    - Default JSON encoder는 set을 JSON으로 변환할 수 없음
    - 커스텀으로 작성해 set을 list로 변환해 JSON으로 처리 할 수 있게끔 구현
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        
        return JSONEncoder.default(self, obj)

# jsonify 함수를 호출할 때마다 CustomJSONEncoder 클래스가 사용
app.json_encoder = CustomJSONEncoder


# 1. 회원가입
@app.route("/sign-up", methods=["POST"])
def sign_up():
    new_user = request.json # reqeust.json은 해당 HTTP 요청을 통해 전송된 JSON 데이터를 파이썬 dictionary로 변환해줌
    new_user["id"] = app.id_count # user id를 생성
    app.users[app.id_count] = new_user # 회원가입하는 사용자의 정보를 저장
    app.id_count = app.id_count + 1 # 다음 회원가입을 위해 +1

    return jsonify(new_user) # 회원가입한 정보를 JSON 형태로 전송


# 3. 트윗
@app.route("/tweet", methods=["POST"])
def tweet():
    payload = request.json # 클라이언트에서 입력한 정보를 payload로 접근하겠다는 의미
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400
    
    if len(tweet) > 300:
        return "300자를 초과했습니다", 400
    
    user_id = int(payload["id"])

    app.tweets.append({
        "user_id" : user_id,
        "tweet" : tweet
    })

    return "success", 200


# 4. 다른 회원 팔로우하기
@app.route("/follow", methods=["POST"])
def follow():
    payload = request.json
    user_id = int(payload["id"]) # HTTP 요청으로 전송된 JSON 데이터에서 해당 사용자의 아이디를 읽어들임
    user_id_to_follow = int(payload["follow"]) # HTTP 요청으로 전송된 JSON 데이터에서 해당 사용자가 팔로우할 아이디를 읽어들임

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400
    
    user = app.users[user_id] # app.users dictionary에서 해당 사용자 아이디를 사용해 데이터를 읽어들임
    user.setdefault("follow", set()).add(user_id_to_follow)
    """ 
    - 이미 사용자가 다른 사용자를 팔로우 한적이 있다면, 사용자의 "follow" 키와 연결되어 있는 set에 팔로우하고자 하는 사용자 아이디를 추가
    - 처음 팔로우 하는 것이라면 사용자의 정보를 담고 있는 딕셔너리에 "follow"라는 키를 empth set와 연결하여 추가
    - set을 사용하면 이미 팔로우 하고 있는 사용자를 팔로우하는 요청이 왔을 때 여러번 저장 안되게끔 해주기 때문
    """

    return jsonify(user)


# 5. 다른 회원 언팔로우하기
@app.route("/unfollow", methods=["POST"])
def unfollow():
    payload = request.json
    user_id = int(payload["id"]) # HTTP 요청으로 전송된 JSON 데이터에서 해당 사용자의 아이디를 읽어들임
    user_id_to_follow = int(payload["unfollow"]) # HTTP 요청으로 전송된 JSON 데이터에서 해당 사용자가 언팔로우할 아이디를 읽어들임

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400
    
    user = app.users[user_id] # app.users dictionary에서 해당 사용자 아이디를 사용해 데이터를 읽어들임
    user.setdefault("follow", set()).discard(user_id_to_follow)
    """ 
    - remove : 없는 값을 삭제하려고 하면 오류를 일으킴
    - discard : 없는 값을 삭제하려고 하면 무시함
    """

    return jsonify(user)


# 6. 타임라인
@app.route("/timeline/<int:user_id>", methods=["GET"]) # <int:user_id> : 엔드포인트의 주소에 해당 사용자의 아이디를 지정할 수 있게 해줌
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400
    
    follow_list = app.users[user_id].get("follow", set()) # 사용자가 팔로우하는 사용자들 리스트를 읽어옴
    follow_list.add(user_id) # 팔로우하는 사용자에 해당 사용자의 아이디를 추가
    timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list] # 전체 트윗 중에 해당 사용자 그리고 해당 사용자가 팔로우하는 사용자들의 트윗만 읽어옴

    return jsonify({
        "user_id" : user_id,
        "timeline" : timeline
    }) # 사용자 아이디와 함께 타임라인을 JSON형태로 리턴


# FLASK_APP=miniter.py FLASK_DEBUG=1 flask run 로 실행