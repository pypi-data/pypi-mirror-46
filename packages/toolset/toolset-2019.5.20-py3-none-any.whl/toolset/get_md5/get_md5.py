from hashlib import md5


def get_md5(file_path):
    _md5 = md5()
    with open(file_path, 'rb') as f:
        while True:
            binary = f.read(4096)
            if not binary:
                break
            _md5.update(binary)
    return _md5.hexdigest()
