from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
import urllib
import bs4

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'


app = Flask(__name__)


# 피자 주문 스킬
@app.route('/order', methods=['POST'])
def order():

    # 메시지 받기
    req = request.get_json()

    #pizza_type = req["action"]["detailParams"]["피자종류"]["value"]
    #address = req["action"]["detailParams"]["sys_text"]["value"]
    location = req["action"]["detailParams"]["sys_location"]["value"]

    enc_location = urllib.parse.quote(location + ' + 날씨')
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,)
    rain_pct=soup.find('li',class_='on now merge1').find('dd',class_='weather_item _dotWrapper').text

    if len(location) <= 0:
        answer = ERROR_MESSAGE
    else:
        answer = location + "의 강수확률은" + rain_pct + "입니다 우산 챙겨가세요!"
        #answer = pizza_type + "를 '" + address + "'(으)로 배달하겠습니다.주문 감사합니다~"

    # 메시지 설정
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', threaded=True)