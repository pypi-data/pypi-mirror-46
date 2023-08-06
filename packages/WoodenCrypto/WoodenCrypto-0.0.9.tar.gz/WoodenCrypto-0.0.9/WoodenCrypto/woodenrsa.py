#!/usr/bin/env python
# coding=utf-8
"""
synopsis: RSA加解密工具
author: haoranzeus@gmail.com (zhanghaoran)
"""
import binascii
import getopt
import sys

import rsa


def usage():
    print('usage:\n')
    print('operational arguments:')
    print('  --help:                          show this help message and exit')
    print('  -f, --function {function name}   do some function')
    print('  -a, --args {arg_name=arg_value}  function arguments')
    print('  --pubkey {pub key path}          public key path')
    print('  --privkey {priv key path}        private key path')
    print('\nexample:')
    print('  python woodenrsa.py -f encryptone --pubkey '
          '/home/zhr/tmp/key_dir/sshkey/id_rsa.pub.pem -a data=123456')


class RsaTool:
    def __init__(self, pub_file=None, priv_file=None):
        self.pub_file = pub_file
        self.priv_file = priv_file

    def usage(self):
        usage()

    def do_func(self, func_name, **paras):
        func = getattr(self, func_name)
        func(**paras)

    @property
    def pubkey(self):
        with open(self.pub_file, 'rb') as f:
            data = f.read()
        pubkey = rsa.PublicKey.load_pkcs1(data)
        return pubkey

    @property
    def privkey(self):
        with open(self.priv_file, 'rb') as f:
            data = f.read()
        pubkey = rsa.PrivateKey.load_pkcs1(data)
        return pubkey

    @staticmethod
    def data_to_hex(data, pubkey):
        """
        将数据加密为hex形式的字符串
        :data: 待加密的字符串
        :privkey: 公钥
        """
        byte_data = data.encode('utf8')
        crypto_data = rsa.encrypt(byte_data, pubkey)
        crypto_hex_data = binascii.b2a_hex(crypto_data)
        crypto_str_data = crypto_hex_data.decode()
        return crypto_str_data

    def _encrypt(self, datas):
        """
        对一系列数进行加密，返回的是字符串列表
        :datas: 待加密的字符串组成的数组
        """
        pubkey = self.pubkey
        ciphertexts = []
        for data in datas:
            crypto_str_data = self.data_to_hex(data, pubkey)
            ciphertexts.append(crypto_str_data)
        return ciphertexts

    def encrypt(self, datas):
        print(self._encrypt(datas))

    def encryptone(self, data):
        ciphertexts = self._encrypt([data, ])
        print(ciphertexts[0])
        return ciphertexts[0]

    def _decrypt(self, ciphertexts):
        """
        对一系列已加密的数据进行解密，返回的是字符串列表
        :ciphertexts: 已经加密的字符串列表
        """
        privkey = self.privkey
        datas = []
        for ciphertext in ciphertexts:
            crypto_hex_data = ciphertext.encode()
            crypto_data = binascii.a2b_hex(crypto_hex_data)
            byte_data = rsa.decrypt(crypto_data, privkey)
            data = byte_data.decode()
            datas.append(data)
        return datas

    def decryptone(self, ciphertext):
        datas = self._decrypt([ciphertext, ])
        print(datas[0])
        return datas[0]


def main(argv):
    try:
        opts, args = getopt.getopt(
                argv, "f:a:",
                ["function=", "args=", "pubkey=", "privkey=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit()

    function = 'usage'
    pub_file = None
    priv_file = None
    arg_str = None
    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('-f', '--function'):
            function = arg
        elif opt == '--pubkey':
            pub_file = arg
        elif opt == '--privkey':
            priv_file = arg
        elif opt in ('-a', '--args'):
            arg_str = arg
        else:
            usage()
    args_dict = {}
    if arg_str:
        arg_str.replace('', ' ')
        args_equal_list = arg_str.split(',')
        for args_equal in args_equal_list:
            k, v = args_equal.split('=')
            if v == "True":
                v = True
            args_dict[k] = v
    rsatool = RsaTool(pub_file=pub_file, priv_file=priv_file)
    rsatool.do_func(function, **args_dict)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
