import json
from urllib import parse
import requests
import time
from encryption_processing import *

class Penguin(object):
    def __init__(self):
        self.base_url = 'https://om.qq.com/videouploader/'
        self.headers = {
                'authority': 'om.qq.com',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': 'pgv_info=ssid=s9651489717; pgv_pvid=2022055997; ts_uid=2998079680; _qpsvr_localtk=0.5700688985139273; pgv_pvi=9583096832; pgv_si=s6607249408; ptisp=cnc; RK=YPZIVBL9YD; ptcz=f854ad3f014d7ce9e0a3cbb15a2070cb67776086b3a70bf620c76e1c3edb8ae7; tvfe_boss_uuid=2460ac626417c478; video_guid=cb8dfb9501704c24; video_platform=2; pac_uid=0_e08ff68e44333; uin=o0327045929; appDownClose=1; ptui_loginuin=2580198728; ts_refer=www.google.com/; userid=17056626; omaccesstoken=85cdc1186e8024b0ff0c3f933a2f47e161aa0078fff9845e52e70454f09813aa25a79b6ba20587f42e8789bea3ffa96548ef69e82a6aa3b688d567fdbb11a65731db39640bc1c61128e5cbe83bda0f24; omaccesstoken_expire=1566807547; wxky=1; rmod=1; TSID=2t944jl2qvuk7in8m4uj1eadl2; alertclicked=%7C1%7C',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }

    # 初始化要进行上传的视频
    def initUpload(self):
        _queue = putFileVideo()
        time.sleep(0.2)
        while True:
            if not _queue.empty():
                video_path = _queue.get()
                # 从队列中获取视频并进行拆分为存储路径和视频名称
                # dirname, filename = os.path.split(video_path)
                _, filename = os.path.split(video_path)
                # 请求参数
                params = {
                    'fileSize': os.path.getsize(video_path),
                    # 'fileName': parse.quote(filename),
                    'fileName': filename,
                    'fileMd5': getFileMd5ByName1(video_path), # md5加密
                    'fileSha': getFileShaByName1(video_path), # sha1加密
                    'agreedSize': '1048576',
                    'uploadSource': '10',
                    'relogin': '1'
                }
                # 拼接初始化的url
                init_url = self.base_url + 'initUpload?'
                # 发请求对要上传的视频进行初始化
                res = requests.get(init_url, params=params, headers=self.headers, verify=False)
                print(res.status_code)
                # 初始化信息返回的是字典 {'code': 0, 'msg': 'success', 'result': {'uploadKey': 'MTU2NjE4NjU2Nz...'}}
                init_info = json.loads(res.text)
                # 获取uploadKey拼接上传post请求的url
                if init_info['result']:
                    uploadKey = init_info['result']['uploadKey']
                    self.uploadBlock(uploadKey, video_path, filename)
            else:
                break

    def uploadBlock(self, uploadKey, video_path, filename):
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "1048576",
            "content-type": "application/octet-stream",
            "Cookie": "pgv_info=ssid=s9651489717; pgv_pvid=2022055997; ts_uid=2998079680; _qpsvr_localtk=0.5700688985139273; pgv_pvi=9583096832; pgv_si=s6607249408; ptisp=cnc; RK=YPZIVBL9YD; ptcz=f854ad3f014d7ce9e0a3cbb15a2070cb67776086b3a70bf620c76e1c3edb8ae7; tvfe_boss_uuid=2460ac626417c478; video_guid=cb8dfb9501704c24; video_platform=2; pac_uid=0_e08ff68e44333; uin=o0327045929; appDownClose=1; ptui_loginuin=2580198728; ts_refer=www.google.com/; userid=17056626; omaccesstoken=85cdc1186e8024b0ff0c3f933a2f47e161aa0078fff9845e52e70454f09813aa25a79b6ba20587f42e8789bea3ffa96548ef69e82a6aa3b688d567fdbb11a65731db39640bc1c61128e5cbe83bda0f24; omaccesstoken_expire=1566807547; wxky=1; rmod=1; TSID=2t944jl2qvuk7in8m4uj1eadl2; alertclicked=%7C1%7C",
            "Host": "om.qq.com",
            "Origin": "https://om.qq.com",
            "Referer": "https://om.qq.com/article/articlePublish",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }
        # 获取已经处理的视频文件
        handle_list = handleFile(video_path)
        for dic in handle_list:
            # 如果索引值等于视频总共需要分的块数，那么最后一块的字节数等于总的字节数减去步长，
            # 否则每一块视频的字节大小等于1048576
            if dic['index'] == os.path.getsize(video_path) // 1048576:
                blockSize = abs(os.path.getsize(video_path) - dic['offset'])
            else:
                blockSize = 1048576
            # 构造请求参数
            params = {
                'uploadKey': uploadKey,
                # 'fileName': parse.quote(filename),
                'fileName': filename,
                'fileSize': os.path.getsize(video_path),
                'offset': dic['offset'],
                'blockSize': blockSize,
                'blockSha': dic['blocksha']  # 对每一个块上传的视频进行sha1加密
            }
            files = {'Filedata': (filename, open(video_path, 'rb'), 'application/octet-stream')}
            # files = {"field": (filename, open(video_path, "rb").read(1048576), "application/octet-stream", {"Content-Type": "application/octet-stream"})}

            upload_url = self.base_url + 'uploadBlock?'
            res = requests.post(upload_url, params=params, headers=header, files=files, verify=False)
            print(len(res.request.body))
            res_dic = json.loads(res.text)
            print(res_dic)
            if res_dic['result']:
                if res_dic['result']['uploadDone'] == True:
                    self.finishUpload(uploadKey, video_path, filename)


    def finishUpload(self, uploadKey, video_path, filename):
        # 检测是否上传完成的url
        finish_url = self.base_url + 'finishUpload?'
        params = {
            'uploadKey': uploadKey,
            'fileName': filename,
            'fileMd5': getFileMd5ByName1(video_path),  # f107a1ae2ac52f68422857c181459b5a
            'fileSha': getFileShaByName1(video_path),  # 1974a3457cc9a3d134a38fa459a64180a789cd73
            'fileSize': os.path.getsize(video_path),
            'uploadSource': '10',
        }
        res = requests.get(finish_url, headers=self.headers, params=params,verify=False)
        finish_dic = json.loads(res.text)
        if finish_dic['msg'] == 'success':
            self.publish()

    def publish(self):
        pass


if __name__ == '__main__':
    om = Penguin()
    om.initUpload()













