import hashlib
import os
from multiprocessing import Queue

# path_queue = Queue()

# 把文件夹下的视频放到队列中
def putFileVideo():
    path_queue = Queue()
    for filename in os.listdir('E:\\video'):
        filepath = os.path.join('E:\\video', filename)
        path_queue.put(filepath)
    return path_queue

# queue = putFileVideo()
# for _ in range(queue.qsize()):
#     print(queue.get())


# 对所要上传的视频进行md5加密
# def getFileMd5ByName1(video_path):
#     with open(video_path, 'rb') as fd:
#         myhash = hashlib.md5()
#         while True:
#             b = fd.read(os.path.getsize(video_path))
#             if not b:
#                 break
#             myhash.update(b)
#         return myhash.hexdigest()
#
# # 对所要上传的视频进行sha1加密
# def getFileShaByName1(video_path):
#     with open(video_path, 'rb') as fa:
#         myhash = hashlib.sha1()
#         while True:
#             b = fa.read(os.path.getsize(video_path))
#             if not b:
#                 break
#             myhash.update(b)
#         return myhash.hexdigest()

# 对每一块上传的视频进行sha1加密
def blockSizeSha(fb):
    myhash = hashlib.sha1()
    while True:
        b = fb.read(1048576)
        if not b:
            break
        myhash.update(b)
        return myhash.hexdigest()

# 对所要上传的视频进行md5加密
def getFileMd5ByName1(fd):
    myhash = hashlib.md5()
    while True:
        b = fd.read(24484783)
        if not b:
            break
        myhash.update(b)
    return myhash.hexdigest()

# 对所要上传的视频进行sha1加密
def getFileShaByName1(fa):
    myhash = hashlib.sha1()
    while True:
        b = fa.read(24484783)
        if not b:
            break
        myhash.update(b)
    return myhash.hexdigest()


if __name__ == "__main__":
    # with open('E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4','rb') as fd:
    #     d5 = getFileMd5ByName1(fd)
    #     print(d5)
    # with open('E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4', 'rb') as fd:
    #     a1 = getFileShaByName1(fd)
    #     print(a1)
    with open('E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4', 'rb') as fb:
        # b = fb.read(100)
        # print(b)
        # r = ' '.join(format(x, 'b') for x in bytearray(b))
        # print(r)
        for index, offset in enumerate(range(0, os.path.getsize('E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4'), 1048576)):
            ba = blockSizeSha(fb)
            print(ba)




s = '''
<script type="text/javascript">
        (function() {
            var s = "_" + Math.random().toString(36).slice(2);
            document.write('<div style="" id="' + s + '"></div>');
            (window.slotbydup = window.slotbydup || []).push({
                id: "u4526818",
                container: s
            });
        })();
</script>
<!-- 多条广告如下脚本只需引入一次 -->
<script type="text/javascript" src="//cpro.baidustatic.com/cpro/ui/c.js" async="async" defer="defer" >
</script>
'''
# id_list = ['u4526818','u4526819','u4526820','u4526821','u4526822','u4526823','u4526826','u4526827','u4526828','u4526829','u4526830','u4526831','u4526833','u4526835','u4526837','u4526838','u4526839','u4526841','u4526843','u4526845','u4526846','u4526847','u4526849','u4526850','u4526852','u4526853','u4526855','u4526856','u4526858','u4526860']
# with open('百青藤1.txt','w',encoding='utf-8') as f:
#     # for i,v in enumerate(id_list):
#     #     f.write(str(i+1)+s)
#     for i in range(30):
#         f.write(str(i+1)+s)


# with open('E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4','rb') as f:
#     bt = f.read(104)
#     print(bt)






