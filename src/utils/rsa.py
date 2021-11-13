import rsa
from io import BytesIO
import base64 as b64


class RSAKeys():
    
    def __init__(self) -> None:
        (pubkey, privkey) = self.generate_keys()
        
        pubBuffered = BytesIO(pubkey.save_pkcs1())
        privBuffered = BytesIO(privkey.save_pkcs1())
        
        pub = pubBuffered.getvalue()
        priv = privBuffered.getvalue()
        
        self.public = b64.encodebytes(pub).decode('utf-8')
        self.private = b64.encodebytes(priv).decode('utf-8')
        

    @staticmethod
    def generate_keys():
        return rsa.newkeys(2048)
    

    def renew(self):
        (pubkey, privkey) = self.generate_keys()
        
        pubBuffered = BytesIO(pubkey.save_pkcs1())
        privBuffered = BytesIO(privkey.save_pkcs1())
        
        pub = pubBuffered.getvalue()
        priv = privBuffered.getvalue()
        
        self.public = b64.encodebytes(pub).decode('utf-8')
        self.private = b64.encodebytes(priv).decode('utf-8')
        
    def print_keys(self):
        
        print(f"""
              Public key
              
              {self.public}
              
              
              Private key
              
              {self.private}
              
              """)
