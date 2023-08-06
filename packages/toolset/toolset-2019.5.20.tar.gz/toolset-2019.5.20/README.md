# ToolSet
[English](https://github.com/Czw96/ToolSet) | [中文](https://github.com/Czw96/ToolSet/blob/master/README-CN.md)

Tool set.

## Install
```
pip3 install toolset --upgrade
```

## ToolList
- [Combiner](#combiner) : list all combinations of elements.
- [get_localhost](#get_localhost) : get local host.
- [get_md5](#get_md5) : Get the file md5 value.
- [text_encryptor](#text_encryptor) : Encrypt/decrypt text.

### Combiner
List all combinations of elements.
```
from toolset.combiner import Combiner

for item in Combiner(ele_set=[1, 2, 3], min_eles=1, max_eles=2):
    print(item)
    
# print: [1], [2], [3], [1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]
```
- ele_set: element set.
- min_eles: minimum number of elements.
- max_eles: maximum number of elements.

### get_localhost
Get local host.
```
>>> from toolset import get_localhost
>>> localhost = get_localhost()
localhost: 192.168.0.112
```

### get_md5
Get the file md5 value.
```
>>> from toolset import get_md5
>>> file_md5 = get_md5('demo.txt')
file_md5: 2e37db575bdab271fbd8d36e29afd737
```

### text_encryptor
Encrypt/decrypt text.
```
>>> from toolset import TextEncryptor
>>> ciphertext = TextEncryptor.encrypt(token='123456', text='hello world!')
ciphertext: b'gAAAAABc4qW9v-0UH0nuVkv9749QDm_8NCJmvWMHcnqSWx8WX1nOiO8Zi-kRmKmVjGQdsn1buoQV8wTCcI-7uHGutQ6tAVQQ4A=='
>>> text = TextEncryptor.decrypt(token='123456', ciphertext=ciphertext)
text: 'hello world!'
```
