import os
from dotenv import load_dotenv
import json
import base64
import hashlib

load_dotenv()


class SignGenerator:

    def __init__(self):
        # Пустой ключ допустим в dev/локальных прогонах (подпись считается без секрета).
        self.__key = os.getenv('HOOK_KEY') or ''

    def __get_sign(self, json_data):
        base64_encoded = base64.b64encode(bytes(json_data, 'utf-8')).decode('utf-8') + self.__key
        md5_hash = hashlib.md5(bytes(base64_encoded, 'utf-8')).hexdigest()
        return md5_hash

    def add_sign(self, json_data):
        data = json.loads(json_data)
        json_unescaped_unicode = json.dumps(data, separators=(',', ':'))
        sign = self.__get_sign(json_unescaped_unicode)
        data['sign'] = sign
        return json.dumps(data)
