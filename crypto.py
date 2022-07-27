import rsa


class Crypto:
    def generateKeys(self):
        (publicKey, privateKey) = rsa.newkeys(512)
        with open('keys/publicKey.pem', 'wb') as p:
            p.write(publicKey.save_pkcs1('PEM'))
        with open('keys/privateKey.pem', 'wb') as p:
            p.write(privateKey.save_pkcs1('PEM'))

    def loadKeys(self):
        with open('keys/publicKey.pem', 'rb') as p:
            publicKey = rsa.PublicKey.load_pkcs1(p.read())
        with open('keys/privateKey.pem', 'rb') as p:
            privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        return privateKey, publicKey

    def Encrypt(self, message, key):
        # rsa.encrypt method is used to encrypt
        # string with public key string should be
        # encode to byte string before encryption
        # with encode method
        return rsa.encrypt(message.encode('ascii'), key)

    def Decrypt(self, ciphertext, key):
        # the encrypted message can be decrypted
        # with ras.decrypt method and private key
        # decrypt method returns encoded byte string,
        # use decode method to convert it to string
        # public key cannot be used for decryption
        # try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
        # except:
        #     return False


# crypto = Crypto()
# crypto.generateKeys()
# privateKey, publicKey = crypto.loadKeys()
# message = input('Write your message here:')
# ciphertext = crypto.Encrypt(message, publicKey)
# print(ciphertext)
# text = crypto.Decrypt(ciphertext, privateKey)
# print(text)
