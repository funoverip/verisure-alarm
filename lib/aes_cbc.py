#!/usr/bin/en python

from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

class aes_cbc:
	
    def __init__(self, iv, key):
        self.BS = 16
        self.iv = iv
        self.key = key


    def pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
	
    def unpad(self,s):
        return s[0:-ord(s[-1])]
	
    def decrypt(self, ciphertext, padding=True):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = cipher.decrypt(ciphertext)
        if padding:
            return self.unpad(plaintext)
        else:
            return plaintext
	
        
    def encrypt(self, cleartext, padding=True):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        if padding:
            ciphertext = cipher.encrypt(self.pad(cleartext))
        else:
            ciphertext = cipher.encrypt(cleartext)     # really ??????
        return ciphertext


