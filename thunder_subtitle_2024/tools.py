# copy from https://github.com/binux/lixian.xunlei/blob/master/libs/tools.py
import os
import hashlib


def gcid_hash_file(path):
    h = hashlib.sha1()
    size = os.path.getsize(path)
    psize = 0x40000
    while size / psize > 0x200 and psize < 0x200000:
        psize = psize << 1
    with open(path, 'rb') as stream:
        data = stream.read(psize)
        while data:
            h.update(hashlib.sha1(data).digest())
            data = stream.read(psize)
    return h.hexdigest().upper()


def cid_hash_file(path):
    h = hashlib.sha1()
    size = os.path.getsize(path)
    with open(path, 'rb') as stream:
        if size < 0xF000:
            h.update(stream.read())
        else:
            h.update(stream.read(0x5000))
            stream.seek(size / 3)
            h.update(stream.read(0x5000))
            stream.seek(size - 0x5000)
            h.update(stream.read(0x5000))
    return h.hexdigest().upper()
