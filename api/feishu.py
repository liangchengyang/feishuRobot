# coding: utf8
import time
import requests
import hashlib
import base64
import hmac
import logging
from api.config import settings
from app.exception import FeishuException

logger = logging.getLogger(__name__)


class FeiShuPush():
    def __init__(self, push_url, secret=None):
        self.push_url = push_url
        self.secret = secret

    def _build_sign(self):
        timestamp = time.time()
        string_to_sign = f'{timestamp}\n{self.secret}'
        hmac_code = hmac.new(string_to_sign.encode(
            "utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(hmac_code).decode('utf-8')

    def _real_request(self, params):
        logger.debug("feishu request with [%s]", params)
        r = requests.post(self.push_url, json=params, timeout=30)
        logger.debug("feishu response <%d> with [%s]", r.status_code, r.text)
        try:
            rj = r.json()
        except Exception as e:
            if r.status_code != 200:
                raise FeishuException(f"推送消息异常: {r.text}") from e
            return f"推送消息成功：{r.text}"
        if rj.get("StatusCode", -1) != 0:
            raise FeishuException(rj.get("StatusMessage", "飞书消息推送错误"))

        return rj

    def push_text(self, content):
        params = {
            "msg_type": "text",
            "content": {
                "text": content
            },
        }
        self._real_request(params=params)

    def push_post(self, title, content):
        params = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }

                }
            }
        }
        self.real_request(params=params)

    def push_image():
        pass

    def push_share_chat():
        pass

    def push_interactive(self, content, at_userids=None, buttons=None, btn_same_line=True):
        params = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True,
                    "enable_forward": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [{
                            "text": {
                                "tag": "lark_md",
                                "content": content
                            }
                        }],
                    }
                ]
            }
        }
        if at_userids:
            for user_id in at_userids:
                params["card"]["elements"].append(
                    {"tag": "at", "user_id": user_id})
        if buttons and btn_same_line:
            params["card"]["elements"].append(
                {"tag": "action", "layout": "bisected", "actions": buttons})
        elif buttons:
            for button in buttons:
                params["card"]["elements"].append(
                    {"tag": "action", "layout": "bisected", "actions": [button]})
        self.real_request(params=params)


feishu_push = FeiShuPush(settings.ROBOT_WEBHOOK)
