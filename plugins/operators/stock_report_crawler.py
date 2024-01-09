# from bs4 import BeautifulSoup, Tag
import requests
from requests import Response
from urllib.parse import urlparse
from airflow.models.baseoperator import BaseOperator
from plugins.common.kakao_api import send_kakao_msg

class FinanceReportOperator(BaseOperator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._url = "https://finance.naver.com/research/company_list.naver?page=1"
        self.urlparse = urlparse(self._url)
    
    def execute(self, context):
        self._get_report_list()

    def _get_report_list(self, date = ""):
        return
        response: Response = requests.get(self.urlparse.geturl())
        bs = BeautifulSoup(response.text, "lxml")
        table_tag: Tag = bs.find("table")
        for row in table_tag.find_all("tr"):
            date_tag = row.find(attrs={"class": "date"})
            if not date_tag:
                continue

            tags: list[Tag] = row.find_all("a")
            company = tags[0].text
            title = tags[1].text
            report_link = tags[2]["href"]
            send_kakao_msg(title, { "company": company, "report_link": report_link })