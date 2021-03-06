import hashlib
import os
from multiprocessing import Queue
import json


# 把文件夹下的视频放到队列中
def putFileVideo():
    path_queue = Queue()
    for filename in os.listdir('E:\\video'):
        filepath = os.path.join('E:\\video', filename)
        path_queue.put(filepath)
    return path_queue

# 对视频分块加密并计算偏移量
def handleFile(video_path):
    block_list = []
    with open(video_path, 'rb') as fb: # 读取视频
        # 对每一块上传的视频进行循环处理，加密
        for index, offset in enumerate(range(0, os.path.getsize(video_path), 1048576)):
            ba = blockSizeSha(fb)   # 对每一块视频进行sha1加密
            # 把加密后的视频段放到字典中
            block_dict = {
                'offset': offset,
                'blocksha': ba,
            }
            block_list.append(block_dict)
    return block_list

# 分块处理要上传的视频
def dealVideo(video_path):
    read_list = []
    with open(video_path, 'rb') as f:
        while True:
            chunk = f.read(1048576)
            if not chunk:
                break
            # print(len(chunk))
            read_dict = {'blockSize': len(chunk), 'blockVideo': chunk}
            read_list.append(read_dict)
    return read_list


# 对所要上传的视频进行md5加密
def getFileMd5ByName1(video_path):
    with open(video_path, 'rb') as fd:
        myhash = hashlib.md5()
        while True:
            b = fd.read(os.path.getsize(video_path))
            if not b:
                break
            myhash.update(b)
        return myhash.hexdigest()

# 对所要上传的视频进行sha1加密
def getFileShaByName1(video_path):
    with open(video_path, 'rb') as fa:
        myhash = hashlib.sha1()
        while True:
            b = fa.read(os.path.getsize(video_path))
            if not b:
                break
            myhash.update(b)
        return myhash.hexdigest()

# 对每一块上传的视频进行sha1加密
def blockSizeSha(fb):
    myhash = hashlib.sha1()
    while True:
        b = fb.read(1048576)
        if not b:
            break
        myhash.update(b)
        return myhash.hexdigest()


# if __name__ == "__main__":
    # print(handleFile())
    # print(dealVideo('E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4'))












