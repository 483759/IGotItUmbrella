from urllib.request import urlopen, Request
import urllib
import bs4

location = input()
enc_location = urllib.parse.quote(location + ' + 날씨')

url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ enc_location

req = Request(url)
page = urlopen(req)
html = page.read()
soup = bs4.BeautifulSoup(html,)
print('현재 ' + location + ' 온도는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.')
