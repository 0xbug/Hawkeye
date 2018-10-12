import hashlib


def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def sha1(data):
    return hashlib.sha1(data.encode('utf-8')).hexdigest()


def md5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    results = m.hexdigest()
    return results
