# Nstockfind
finding m194 stocks in naver having no information on overview
==========================================
## 0. 진행도
2023-06-13 : 크롤링 기능 구현 <br>
2023-06-14 : 초본 작업 완료 <br>

<br><br>

## 1. 사용법

[기본 환경]
Python

[추가 설치 라이브러리]
[ requests, selenium, besutifulsoup]

* c:\에 크롬에 맞는 크롬드라이버를 넣어야한다.
크롬 버전 확인 : 크롬 도구 > 도움말 > chrome 정보
(chromedriver_autoinstaller 모듈을 통해 업데이트 받을것)

* pip ssl 오류 해결법 :
 1) pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install [라이브러리]
 2) C:\Users\KOSCOM\AppData\Local\Programs\Python\Python38\Lib\site-packages\pip\_vendor\requests\session.py
에서 self.verify=False로 변경