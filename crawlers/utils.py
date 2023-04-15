import os
import hashlib
import random


# 创建存储资源文件的目录
def make_all_dirs(p, filepath=False):
    if filepath is True:
        filepath, fullname = os.path.split(p)
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
    else:
        if not os.path.isdir(p):
            os.makedirs(p)


def download_source(bs, save_path):
    # 保证文件夹存在，可以直接创建并写入文件
    make_all_dirs(save_path, filepath=True)
    try:
        # 存在，则删除文件
        if os.path.exists(save_path):
            os.remove(save_path)
        with open(save_path, mode="ab") as f:
            f.write(bs)
        return True
    except:
        return False


# 生成MD5
def md5(s):
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))

    return hl.hexdigest()


def rand_string(length=12):
    s = 'abcdefghijklmnopqrstuvwxyz0123456789'
    rs = ''
    for i in range(0, length):
        rs += random.choice(s)
    return rs
