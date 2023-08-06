#!/usr/bin/env python
# coding=utf-8
"""
synopsis: AES加解密工具
author: haoranzeus@gmail.com (zhanghaoran)
"""
import getopt
import sys

from binascii import b2a_hex, a2b_hex
from Crypto import Random
from Crypto.Cipher import AES


def usage():
    print('usage:\n')
    print('  --help:                          show this help message and exit')
    print('\n')
    print('examples: ')
    print('plainfile to cipherfile:')
    print('  python3 -m WoodenCrypto.woodenaes '
          '-k {16/24/32 bytes long key string} '
          '--encryptfile -i {plainfile} -o {cipherfile to save}')
    print('cipherfile to plainfile:')
    print('  python3 -m WoodenCrypto.woodenaes '
          '-k {16/24/32 bytes long key string} '
          '--decryptfile -i {cipherfile} -o {plainfile to save}')


# padding算法
def pad(s):
    BS = AES.block_size     # aes数据分组长度为128 bit
    return s + (BS - len(s) % BS) * chr(0)


class AesTool:
    def __init__(self, key, mode=AES.MODE_CBC):
        self.key = key
        self.mode = mode

    def usage(self):
        usage()

    def do_func(self, func_name, **paras):
        func = getattr(self, func_name)
        func(**paras)

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
            plaintext = self.decrypt(ciphertext)
            return plaintext.decode('utf8')

    def decrypt_file(self, cipherfile, plainfile='/tmp/a.txt'):
        plaintext = self.decrypt_read(cipherfile)
        with open(plainfile, 'w+') as f:
            f.write(plaintext)


def get_arg(opts, key):
    """
    配合getopt通过key获得value
    """
    for k, v in opts:
        if k == key:
            return v


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv, "f:a:k:i:o:h",
            ["function=", "args=", "key=", "help",
             "encryptfile", "decryptfile"])
    except getopt.GetoptError:
        usage()
        sys.exit()
    function = 'usage'
    arg_str = None
    key = ''
    args_dict = {}
    for opt, arg in opts:
        if opt in '-h, --help':
            usage()
            sys.exit()
        elif opt in ('-k, --key'):
            key = arg
            if len(key) not in (16, 24, 32):
                print('Error: key should be 16, 24 or 32 bytes long')
                sys.exit()
        elif opt in ('-f', '--function'):
            function = arg
        elif opt in ('-a', '--args'):
            arg_str = arg
        elif opt == '--encryptfile':
            function = 'encrypt_file'
            in_path = get_arg(opts, '-i')
            out_path = get_arg(opts, '-o')
            args_dict['plainfile'] = in_path
            args_dict['cipherfile'] = out_path
        elif opt == '--decryptfile':
            function = 'decrypt_file'
            in_path = get_arg(opts, '-i')
            out_path = get_arg(opts, '-o')
            args_dict['plainfile'] = out_path
            args_dict['cipherfile'] = in_path
    if arg_str:
        arg_str.replace('', ' ')
        args_equal_list = arg_str.split(',')
        for args_equal in args_equal_list:
            k, v = args_equal.split('=')
            if v == "True":
                v = True
            args_dict[k] = v
    crypto_tool = AesTool(key)
    crypto_tool.do_func(function, **args_dict)


if __name__ == '__main__':
    # demo = AesTool('__16_bytes_key__', AES.MODE_CBC)
    # e = demo.encrypt(sys.argv[1])
    # d = demo.decrypt(e)
    # print('加密: ', e)
    # print('解密: ', d.decode('utf8'))

    # e = demo.encrypt_file(sys.argv[1], sys.argv[2])

    # d = demo.decrypt_read(sys.argv[1])
    args = sys.argv[1:]
    main(args)
