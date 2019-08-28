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
                'cookie': 'pgv_info=ssid=s9651489717; pgv_pvid=2022055997; ts_uid=2998079680; _qpsvr_localtk=0.5700688985139273; pgv_pvi=9583096832; pgv_si=s6607249408; ptisp=cnc; RK=YPZIVBL9YD; ptcz=f854ad3f014d7ce9e0a3cbb15a2070cb67776086b3a70bf620c76e1c3edb8ae7; tvfe_boss_uuid=2460ac626417c478; video_guid=cb8dfb9501704c24; video_platform=2; pac_uid=0_e08ff68e44333; uin=o0327045929; appDownClose=1; ptui_loginuin=2580198728; ts_refer=www.google.com/; userid=17056626; wxky=1; omaccesstoken=344192fc43e008b36dd60e781d1122c191da172f038b83aa3f4a50d8cd92f66f2898b7ca8276d94fcfadf6515505723a3c30da51ba7936bf00f01976f46bdf91499255b1c9dca51a8f07293d2d5fc94c; omaccesstoken_expire=1567068180; rmod=1; TSID=a25fcjahs2ei49khiegfm6aqm6; alertclicked=%7C1%7C',
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
                print(init_info)
                # 获取uploadKey拼接上传post请求的url
                if init_info['result']:
                    uploadKey = init_info['result']['uploadKey']
                    self.uploadBlock(uploadKey, video_path, filename)
            else:
                break

    # 分块上传视频
    def uploadBlock(self, uploadKey, video_path, filename):
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "1048576",
            "content-type": "application/octet-stream",
            "Cookie": "pgv_info=ssid=s9651489717; pgv_pvid=2022055997; ts_uid=2998079680; _qpsvr_localtk=0.5700688985139273; pgv_pvi=9583096832; pgv_si=s6607249408; ptisp=cnc; RK=YPZIVBL9YD; ptcz=f854ad3f014d7ce9e0a3cbb15a2070cb67776086b3a70bf620c76e1c3edb8ae7; tvfe_boss_uuid=2460ac626417c478; video_guid=cb8dfb9501704c24; video_platform=2; pac_uid=0_e08ff68e44333; uin=o0327045929; appDownClose=1; ptui_loginuin=2580198728; ts_refer=www.google.com/; userid=17056626; wxky=1; omaccesstoken=344192fc43e008b36dd60e781d1122c191da172f038b83aa3f4a50d8cd92f66f2898b7ca8276d94fcfadf6515505723a3c30da51ba7936bf00f01976f46bdf91499255b1c9dca51a8f07293d2d5fc94c; omaccesstoken_expire=1567068180; rmod=1; TSID=a25fcjahs2ei49khiegfm6aqm6; alertclicked=%7C1%7C",
            "Host": "om.qq.com",
            "Origin": "https://om.qq.com",
            "Referer": "https://om.qq.com/article/articlePublish",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }
        # 对视频加密和计算偏移量的信息列表
        block_sha_list = handleFile(video_path)
        # 每一次上传视频块的大小和当前读取的视频内容
        deal_video_list = dealVideo(video_path)
        for sha_dic, video_dic in zip(block_sha_list, deal_video_list):
            params = {
                'uploadKey': uploadKey,
                # 'fileName': parse.quote(filename),
                'fileName': filename,
                'fileSize': os.path.getsize(video_path),
                'offset': sha_dic['offset'],
                'blockSize': video_dic['blockSize'],
                'blockSha': sha_dic['blocksha']  # 对每一个块上传的视频进行sha1加密
            }
            upload_url = self.base_url + 'uploadBlock?'
            res = requests.post(upload_url, params=params, headers=header, data=video_dic['blockVideo'], verify=False)
            res_dic = json.loads(res.text)
            print(res_dic)
            if res_dic['result']:
                if res_dic['result']['uploadDone'] == True:
                    self.finishUpload(uploadKey, video_path, filename)

    # 完成上传
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
            self.checkVideoParam()
            self.batchPublish()

    def checkVideoParam(self):
        check_url = 'https://om.qq.com/videoManager/checkVideoParam?'
        params = {
            'title': '在星爷电影中就连他也变得搞笑了',
            'tags': '电影 搞笑',
            'desc': '',
            'relogin': '1'
        }
        res = requests.get(check_url, headers=self.headers, params=params, verify=False)
        # 检查发布的参数成功返回json
        check_dict = json.loads(res.text) # '{"response":{"code":0,"msg":"suc"},"data":null}'
        # if check_dict['response']['code'] == 0:
            # self.batchPublish()

    def batchPublish(self):
        batch_url = 'https://om.qq.com/article/batchPublish?relogin=1'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '3280',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'pgv_info=ssid=s9651489717; pgv_pvid=2022055997; ts_uid=2998079680; _qpsvr_localtk=0.5700688985139273; pgv_pvi=9583096832; pgv_si=s6607249408; ptisp=cnc; RK=YPZIVBL9YD; ptcz=f854ad3f014d7ce9e0a3cbb15a2070cb67776086b3a70bf620c76e1c3edb8ae7; tvfe_boss_uuid=2460ac626417c478; video_guid=cb8dfb9501704c24; video_platform=2; pac_uid=0_e08ff68e44333; uin=o0327045929; appDownClose=1; ptui_loginuin=2580198728; ts_refer=www.google.com/; userid=17056626; wxky=1; omaccesstoken=344192fc43e008b36dd60e781d1122c191da172f038b83aa3f4a50d8cd92f66f2898b7ca8276d94fcfadf6515505723a3c30da51ba7936bf00f01976f46bdf91499255b1c9dca51a8f07293d2d5fc94c; omaccesstoken_expire=1567068180; rmod=1; TSID=674eor8faoro5uk8vcoq7t0lg3; alertclicked=%7C1%7C',
            'origin': 'https://om.qq.com',
            'referer': 'https://om.qq.com/article/articlePublish',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'videos': [{"title":"在星爷电影中就连他也变得搞笑了","tags":"电影 搞笑","desc":"","newcat":"电影","newsubcat":"电影剪辑","apply_video_originalFlag":0,"activity":"","vid":"k0919k7yif5","imgurl":"http://puap.qpic.cn/vpic/0/k0919k7yif5_fast_5.jpg/0","user_original":0,"tagsid":"{}","isOriginal":0,"sf_type":"tencent","apply_video_vrFlag":0,"user_vr":0,"copyright_creation_info":[],"is_commercial":0,"commodity":"","outlink":"","activity_type":"","apply_push_flag":0,"tabtype":"","img_direct":0,"yooExclusive":0,"needpub":1,"uid":"f1566970133771023698369175406464","imgurlsrc":"system"}],
            'articles': [{"vid":"k0919k7yif5","title":"在星爷电影中就连他也变得搞笑了","is_commercial":0,"user_original":0,"sf_type":"tencent","isOriginal":0,"user_vr":0,"commodity":"","apply_push_flag":0,"activity":"","yooExclusive":0,"cover_type":"","type":"56","content":"<p><iframe allowfullscreen=\"\" f=\"no\" frameborder=\"0\" height=\"270\" src=\"//v.qq.com/iframe/preview.html?vid=k0919k7yif5&amp;width=480&amp;height=270&amp;auto=0\" type=\"video\" width=\"480\"></iframe></p>","video":"{\"vid\":\"k0919k7yif5\",\"title\":\"在星爷电影中就连他也变得搞笑了\",\"type\":\"video\",\"desc\":\"\",\"duration\":\"0:00:00\",\"img\":{}}","needpub":1,"copyright_creation_info":[]}]
        }
        res = requests.post(batch_url, headers=headers, data=data, verify=False)
        # 返回值json中如果data中有数据则发布成功
        batch_dict = json.loads(res.text)  # {"response":{"code":0,"msg":""},"data":{"j0919fcajuo":{"aid":"20190828V0D6GU","ret":0}}}
        print(batch_dict)
        if batch_dict['data']:
            print('发布成功！')


if __name__ == '__main__':
    om = Penguin()
    om.initUpload()













