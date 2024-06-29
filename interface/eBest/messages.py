import os
from urllib.parse import urljoin
from dataclasses import dataclass

from interface.eBest.tr_code import TRCode
from interface.eBest.endpoint import Endpoint
from interface.base.messages_factory import MessageStrategy, BaseMessage

class GetToken(MessageStrategy):
    @staticmethod
    def create_message(**kwargs) -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.get_token)
        headers = BaseMessage.from_kwargs(content_type="application/x-www-form-urlencoded").to_dict()
        data = BaseMessage.from_kwargs( grant_type="client_credentials",
                                        appkey=os.getenv("EBEST_RAPP"),
                                        appsecretkey=os.getenv("EBEST_RSEC"),
                                        scope="oob").to_dict()
        return BaseMessage.from_kwargs(url=url, headers=headers, data=data).to_dict()

class GetChartData(MessageStrategy):
    """
        차트 데이터 요청 메세지 생성 클래스
        https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=12320341-ad85-429a-90bd-5b3771c5e89f

    Args:
        MessageStrategy (_type_): _description_

    Returns:
        _type_: _description_
    """
    @staticmethod
    def create_message(chart_type,
                        shcode: str,
                        tr_cont: str = "N",
                        tr_cont_key: str = "",
                        ncnt: int = 1,
                        qrycnt: int = 500,
                        nday: str = "0",
                        sdate: str = "",
                        stime: str = "",
                        edate: str = "99999999",
                        etime: str = "",
                        cts_date: str = "",
                        cts_time: str = "",
                        comp_yn: str = "N",
                        ) -> BaseMessage:
        url = urljoin(Endpoint.base_url, Endpoint.chart_data)
        headers = BaseMessage.from_kwargs(
                                            authorization=os.getenv("EBEST_TOKEN"),
                                            tr_cd= TRCode.minute_chart if chart_type == "minute" else TRCode.tick_chart,
                                            tr_cont = tr_cont,
                                            tr_cont_key = tr_cont_key
                                            ).add_attribute(key="Content-Type", value="application/json; charset=UTF-8").to_dict()
        
        if chart_type != "minute":
            block_type = "t8411InBlock" # 틱 차트
        else:
            block_type = "t8412InBlock" # 분봉 차트

        data = BaseMessage.from_kwargs(**{
            block_type: BaseMessage.from_kwargs(
                shcode = shcode,
                ncnt = ncnt,
                qrycnt = qrycnt,
                nday = nday,
                sdate = sdate,
                stime = stime,
                edate = edate,
                etime = etime,
                cts_date = cts_date,
                cts_time = cts_time,
                comp_yn = comp_yn
            ).to_dict()
        }).to_json()
            
        return BaseMessage.from_kwargs(url=url, headers=headers, data=data).to_dict()

