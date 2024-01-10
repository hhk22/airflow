import pendulum
from dateutil.relativedelta import relativedelta
import os
import json
import requests
from airflow.models import Variable

def _refresh_token_to_variable():
    client_id = Variable.get("kakao_client_secret")
    tokens = eval(Variable.get("kakao_tokens"))
    refresh_token = tokens.get('refresh_token')
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": f"{client_id}",
        "refresh_token": f"{refresh_token}"
    }
    response = requests.post(url, data=data)
    rslt = response.json()
    new_access_token = rslt.get('access_token')
    new_refresh_token = rslt.get('refresh_token')         # Refresh 토큰 만료기간이 30일 미만이면 refresh_token 값이 포함되어 리턴됨.
    if new_access_token:
        tokens['access_token'] = new_access_token
    if new_refresh_token:
        tokens['refresh_token'] = new_refresh_token

    now = pendulum.now('Asia/Seoul').strftime('%Y-%m-%d %H:%M:%S')
    tokens['updated'] = now
    os.system(f'airflow variables set kakao_tokens "{tokens}"')
    print('variable 업데이트 완료(key: kakao_tokens)')

def send_kakao_msg(talk_title: str, content_lst: list, url):    
    try_cnt = 0
    while True:
        tokens = eval(Variable.get("kakao_tokens"))
        access_token = tokens.get('access_token')
        contents = []

        for item in content_lst:
            contents.append(
                {
                    "title": item["title"],
                    "description": item["company"],
                    "image_url": "https://mud-kage.kakao.com/dn/QNvGY/btqfD0SKT9m/k4KUlb1m0dKPHxGV8WbIK1/openlink_640x640s.jpg",
                    "image_width": 640,
                    "image_height": 640,
                    "link": {
                        "web_url": item["report_link"],
                        "mobile_web_url": item["report_link"],
                        "android_execution_params": "",
                        "ios_execution_params": ""
                    }
                }
            )

        buttons = [
            {
                "title": "리포트 홈으로 이동",
                "link": {
                    "web_url": url,
                    "mobile_web_url": url
                }
            }
        ]

        list_data = {
            'object_type': 'list',
            'header_title': f'{talk_title}',
            'header_link': {
                'web_url': '',
                'mobile_web_url': '',
                'android_execution_params': 'main',
                'ios_execution_params': 'main'
            },
            'contents': contents,
            'buttons': buttons
        }

        send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {
            "Authorization": f'Bearer {access_token}'
        }

        data = {'template_object': json.dumps(list_data)}
        response = requests.post(send_url, headers=headers, data=data)
        print(f'try횟수: {try_cnt}, reponse 상태:{response.status_code}')
        try_cnt += 1

        if response.status_code == 200:         # 200: 정상
            return response.status_code
        elif response.status_code == 400:       # 400: Bad Request (잘못 요청시), 무조건 break 하도록 return
            return response.status_code
        elif response.status_code == 401 and try_cnt <= 2:      # 401: Unauthorized (토큰 만료 등)
            _refresh_token_to_variable()
        elif response.status_code != 200 and try_cnt >= 3:      # 400, 401 에러가 아닐 경우 3회 시도때 종료
            return response.status_code