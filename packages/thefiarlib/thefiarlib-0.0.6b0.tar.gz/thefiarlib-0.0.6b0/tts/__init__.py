# -*- coding: utf-8 -*-
import os
from zlib import crc32

from config import settings
from library.tts.nuance_tts import NuanceTTS

if __name__ == "__main__":
    waiting_list = [
        "fdsfdsf"
    ]

    for item in waiting_list:
        NuanceTTS.parse_and_save(item,
                                 os.path.join(os.path.dirname(os.path.relpath(__file__)), item.replace(' ', '_')+".mp3"),
                                 False,
                                 'en',
                                 os.path.join(settings.BASE_DIR, 'docs', 'nuance_credentials', 'credentials_fantianjiao.json')
                                 )
