from bs4 import BeautifulSoup, Tag
import requests
from requests import Response
from urllib.parse import urlparse
from datetime import datetime
from airflow.models.baseoperator import BaseOperator
from common.kakao_api import send_kakao_msg

class FinanceReportOperator(BaseOperator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._url = "https://finance.naver.com/research/company_list.naver?page=2"
        self.urlparse = urlparse(self._url)
        self._count = 1
    
    def execute(self, context):
        date: datetime = context['data_interval_end']
        self._get_report_list(date=date.strftime("%Y.%m.%d")[2:])
        self._count = 1

    def _get_report_list(self, date):
        response: Response = requests.get(self.urlparse.geturl())
        bs = BeautifulSoup(response.text, "lxml")
        table_tag: Tag = bs.find("table")

        content_lst = []
        for idx, row in enumerate(table_tag.find_all("tr")):
            date_tag = row.find(attrs={"class": "date"})
            if not date_tag or date_tag.text != date:
                continue
                            
            tags: list[Tag] = row.find_all("a")
            company = tags[0].text
            title = tags[1].text
            report_link = tags[2]["href"]
            content_lst.append({
                "company": company,
                "title": title,
                "report_link": report_link
            })

            if len(content_lst) % 3 == 0:
                send_kakao_msg(f"daily_report_{self._count}", content_lst, self._url)
                self._count += 1
                content_lst = []
        
        if not content_lst:
            send_kakao_msg(f"daily_report_{self._count}", content_lst, self._url)
            self._count += 1