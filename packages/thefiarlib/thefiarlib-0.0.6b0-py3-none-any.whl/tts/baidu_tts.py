# coding: utf-8
import os
import time
from urllib.parse import quote_plus
from uuid import uuid4
import requests


class Buffer(object):
    def __init__(self, resp):
        self.resp = resp
        self.content_type = resp.headers['content-type']
        self.content_length = int(resp.headers['content-length'])

    @property
    def content(self):
        return self.resp.content

    @property
    def stream(self):
        return self.resp.raw

    def iter_content(self, chunk_size):
        return self.resp.iter_content(chunk_size=chunk_size)

    def read(self):
        return self.content

    def write(self, fp, chunk_size=1024):
        with open(fp, 'wb') as f:
            for chunk in self.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)


class TfBaiduTTS(object):
    # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    PER = 1
    # 语速，取值0-15，默认为5中语速
    SPD = 5
    # 音调，取值0-15，默认为5中语调
    PIT = 5
    # 音量，取值0-9，默认为5中音量
    VOL = 5
    # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    AUE = 3

    API_KEY = 'oBp8BUGFFDWIuawOog8fouYy'
    SECRET_KEY = 'uofXMgk6mvxlKrWMpYg1buDAC8oDxnb4'
    APP_ID = '15659552'

    def __init__(self, api_key='', secret_key=''):
        self.cache = {}
        if len(api_key) == 0:
            api_key = self.API_KEY
        if len(secret_key) == 0:
            secret_key = self.SECRET_KEY

        self.api_key = api_key
        self.secret_key = secret_key

    def fetch_access_token(self):
        url = 'https://openapi.baidu.com/oauth/2.0/token'
        key = 'access_token'
        res = self.cache.get(key)
        if res and res['expire_time'] > time.time():
            return res['data']
        resp = requests.get(
            url,
            params={
                'grant_type'   : 'client_credentials',
                'client_id'    : self.api_key,
                'client_secret': self.secret_key
            }
        )
        jsn = resp.json()
        access_token = jsn['access_token']
        expires_in = jsn['expires_in']
        self.cache[key] = {
            'expire_time': time.time() + expires_in - 20,
            'data'       : access_token
        }
        return access_token

    def say(self, text: str):
        """
        :param text:
        :return:
        :rtype Buffer
        """
        text = text.encode('utf-8')
        url = 'http://tsn.baidu.com/text2audio'
        access_token = self.fetch_access_token()

        params = {'tok' : access_token, 'tex': quote_plus(text),
                  'per' : self.PER, 'spd': self.SPD,
                  'pit' : self.PIT, 'vol': self.VOL, 'aue': self.AUE,
                  'cuid': uuid4().hex,
                  'lan' : 'zh', 'ctp': 1}

        resp = requests.post(url, params, stream=True)
        return Buffer(resp)

    def parse_and_save(self, text: str, save_to: str, force=False) -> bool:
        """
        :param text:
        :param save_to:
        :param force:
        :return:
        :rtype bool
        """
        ret_data = self.say(text)
        if os.path.exists(save_to):
            if not force:
                return True
            else:
                os.remove(save_to)

        ret_data.write(save_to)
        return True


class TfWordTts(object):
    def parse_and_save(self, text: str, save_to: str, accent='en', spd=5, force=False) -> bool:
        url = "https://fanyi.baidu.com/gettts"
        param = {
            "lan"   : accent,
            "text"  : text,
            "spd"   : spd,
            "source": "web",
        }
        r = requests.get(url, params=param, allow_redirects=True)

        base_path = os.path.dirname(save_to)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if r.status_code == 200:
            if os.path.exists(save_to):
                if not force:
                    return True
                else:
                    os.remove(save_to)

            open(save_to, 'wb').write(r.content)
            return True
        else:
            return False


if __name__ == '__main__':
    baidu_tts = TfBaiduTTS()
    baidu_tts.parse_and_save('good bye', './test_sentence.mp3')

    word_tts = TfWordTts()
    word_tts.parse_and_save('change', './change_uk.mp3', "uk")
