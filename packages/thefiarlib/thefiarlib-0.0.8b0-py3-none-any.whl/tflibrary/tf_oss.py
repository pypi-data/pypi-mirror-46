import os
import random
from pprint import pprint

import oss2
import qiniu
import requests
from urllib.parse import urlparse
import json


class TfOss:
    def __init__(self, config):
        self.config = config
        self.bucket_name = config['bucket_name']
        self.bucket_ali = None
        self.bucket_qiniu = None

        if config and config['client_type'] == 'ali':
            auth = oss2.Auth(config['key'], config['sec'])
            self.bucket_ali = oss2.Bucket(auth, config['endpoint'], config['bucket_name'])
        else:
            self.q = qiniu.Auth(config['key'], config['sec'])
            self.bucket_qiniu = qiniu.BucketManager(self.q)
            self.mac_auth = qiniu.QiniuMacAuth(config['key'], config['sec'])

    def put_object_from_file(self, local_file, to_file) -> bool:
        """
        上传文件
        :param local_file:
        :param to_file:
        :return:
        """
        result = False
        if self.bucket_ali:
            ret = self.bucket_ali.put_object_from_file(to_file, local_file)
            if ret.resp.status == 200:
                result = True
        elif self.bucket_qiniu:
            ret, info = self._qiniu_put_file(local_file, to_file)
            if info == 200:
                result = True
        else:
            raise Exception("未初始化")

        return result

    def _qiniu_put_file(self, local_file, to_file):
        key = to_file
        token = self.q.upload_token(self.bucket_name, key, 3600)
        ret, info = qiniu.put_file(token, key, local_file)
        return ret, info

    def _qiniu_private_download_file(self, url, save_file):
        """
               私有空间下载
               :param url  直接输入url的方式下载 'http://domain/key'
               :param save_file 本地路径
        """
        private_url = self.q.private_download_url(url)
        pprint(private_url)
        r = requests.get(private_url)
        try:
            if r.status_code == 200:
                if os.path.exists(save_file):
                    os.remove(save_file)
                f = open(save_file, 'wb')
                f.write(r.content)
                f.close()
                return True
        except Exception as ex:
            pprint(ex)
            pass
        return False

    def _qiniu_private_url(self, url):
        return self.q.private_download_url(url)

    def download_object(self, oss_path, filename, domain_name):
        """
        下载文件
        :param oss_path:
        :return:
        """
        if self.bucket_ali:
            return self.bucket_ali.get_object_to_file(oss_path, filename)
        elif self.bucket_qiniu:
            base_url = 'http://{}/{}'.format(domain_name, oss_path)
            private_url = self.q.private_download_url(base_url, expires=3600)
            r = requests.get(private_url)
            assert r.status_code == 200
            open(filename, 'wb').write(r.content)
            return filename

    def get_object_meta(self, oss_path):
        """
        获取对象信息
        :param oss_path:
        :return:
        """
        if self.bucket_ali:
            return self.bucket_ali.get_object_meta(oss_path)
        elif self.bucket_qiniu:
            return self.bucket_qiniu.stat(self.bucket_name, oss_path)

    def check_exist(self, obj_path):
        if self.bucket_ali:
            return self.bucket_ali.object_exists(obj_path)
        elif self.bucket_qiniu:
            data, info = self.bucket_qiniu.stat(self.bucket_name, obj_path)
            return info.status_code == 200

    def get_oss_client(self):
        """
        获取oss client对象
        :return:
        """
        if self.bucket_ali:
            return self.bucket_ali
        elif self.bucket_qiniu:
            return self.bucket_qiniu

    def get_qiniu_random_pipeline(self):
        """
        获得七牛随机队列
        :return: Str
        """
        lists = ['rocket_audio', 'chicken_audio', 'rocket_mv_0', 'rocket_mv_1']
        return lists[random.randint(0, len(lists) - 1)]
