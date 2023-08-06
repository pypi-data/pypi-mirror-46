#!/usr/bin/env python
# coding=utf-8
"""
synopsis: AES加解密工具
author: haoranzeus@gmail.com (zhanghaoran)
"""
from Crypto import Random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# padding算法
def pad(s):
    BS = AES.block_size     # aes数据分组长度为128 bit
    return s + (BS - len(s) % BS) * chr(0)


class AesTool:
    def __init__(self, key, mode):
        self.key = key
        self.mode = mode

    def encrypt(self, plaintext):
        # 生成随机初始向量IV
        iv = Random.new().read(AES.block_size)
        cryptor = AES.new(self.key, self.mode, iv)
        ciphertext = cryptor.encrypt(pad(plaintext))
        # 统一把加密后的字符串转化为十六进制字符串
        return b2a_hex(iv + ciphertext)

    def decrypt(self, ciphertext):
        ciphertext = a2b_hex(ciphertext)
        iv = ciphertext[0:AES.block_size]
        ciphertext = ciphertext[AES.block_size: len(ciphertext)]
        cryptor = AES.new(self.key, self.mode, iv)
        plaintext = cryptor.decrypt(ciphertext)
        return plaintext.rstrip(str.encode(chr(0)))

    def encrypt_file(self, plainfile, cipherfile):
        """
        加密一个文件，并输出
        :plainfile: 加密前的文件路径
        :cipherfile: 加密后输出的密文文件
        """
        with open(plainfile, 'r') as f:
            content = f.read()

        encrypt_content = self.encrypt(content)
        with open(cipherfile, 'wb+') as f:
            f.write(encrypt_content)

    def decrypt_read(self, cipherfile):
        """
        读取一个加密过的文件，返回解密后的内容
        :cipherfile: 加密后的文件路径
        """
        with open(cipherfile, 'r') as f:
            ciphertext = f.read()
            return ciphertext


if __name__ == '__main__':
    demo = AesTool('__16_bytes_key__', AES.MODE_CBC)
    import sys
    e = demo.encrypt(sys.argv[1])
    d = demo.decrypt(e)
    print('加密: ', e)
    print('解密: ', d.decode('utf8'))

    # e = demo.encrypt_file(sys.argv[1], sys.argv[2])

    # d = demo.decrypt_read(sys.argv[1])
