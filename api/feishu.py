# coding: utf8
import time
import requests
import hashlib
import base64
import hmac
import logging
from api.config import settings

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
                raise
            return f"推送消息成功：{r.text}"
        if rj.get("StatusCode", -1) != 0:
            raise

        return rj

    def push_text(self, content):
        # 推送文本
        params = {
            "msg_type": "text",
            "content": {
                "text": content
            },
        }
        self._real_request(params=params)

    def push_post(self, title, content):
        # 推送富文本
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
        self._real_request(params=params)

    def push_image():
        # 推送图片
        pass

    def push_share_chat():
        # 推送群卡片
        pass

    def push_interactive(self):
        params = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "update_multi": True,  # 是否设置未共享卡片
                    "enable_forward": False  # 是否允许被转发
                },
                "header": {
                    "title": {
                        "tag": "plain_text",  # 标题只支持文本类型
                        "content": "标题",
                        "i18n": {
                            "zh_cn": "中文文本",
                            "en_us": "English text",
                            "ja_jp": "日本語文案"
                        }  # content，i18n二选一 i18n支持多国文本
                    },
                    "template": "red"  # 主题颜色 red,green,orange,grey
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [{
                            "text": {
                                "tag": "lark_md",
                                "content": "yayya"
                            }
                        }],
                    }
                ]
            }
        }

        self._real_request(params=params)


customize_robot = FeiShuPush(settings.ROBOT_WEBHOOK)
