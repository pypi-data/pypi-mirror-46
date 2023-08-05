# -*- coding: utf-8 -*-
from Crypto.Cipher import DES3
from Crypto.Util.Padding import *

__key_bytes = bytes("niugu123niugu456niugu123",encoding="utf-8")
__iv_bytes = bytes("12312300", encoding='utf-8')

def encrypt(plainText):
    """根据明文，做DES加密，并返回Hex字符串"""
    data = bytes(plainText,'utf-8')
    text = pad(data,8)
    cipher = DES3.new(__key_bytes, DES3.MODE_CBC,IV=__iv_bytes)
    m = cipher.encrypt(text)
    s = bytes.hex(m)
    return s

def decrypt(encryptText):
    data = bytes.fromhex(encryptText)
    cipher = DES3.new(__key_bytes, DES3.MODE_CBC,IV=__iv_bytes)
    s = cipher.decrypt(data)
    s = unpad(s,8)
    s = s.decode('utf-8') # unpad and decode bytes to str
    return s

if __name__ == '__main__':
    encryptTxt = "867a6d7640da567387b1343a4ca4067aa24204aed8091440877378ace6656a99313dde056406d33f"
    print(encryptTxt)
    val = decrypt(encryptTxt)    
    print(val)
    en = encrypt(val)
    print(en);