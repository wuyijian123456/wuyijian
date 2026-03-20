import hashlib
import time
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from core.logger import log

class SignUtil:
    """接口签名/加密工具：MD5、SHA256、RSA"""
    @staticmethod
    def md5_sign(data, secret_key):
        """MD5签名：data(字典) + 秘钥 → 签名串"""
        # 1. 按key排序
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        # 2. 拼接成字符串
        sign_str = "".join([f"{k}{v}" for k, v in sorted_data]) + secret_key
        # 3. MD5加密
        md5 = hashlib.md5()
        md5.update(sign_str.encode("utf-8"))
        sign = md5.hexdigest().upper()
        log.info(f"MD5签名：原始数据={data}，签名串={sign_str}，签名结果={sign}")
        return sign

    @staticmethod
    def sha256_sign(data, secret_key):
        """SHA256签名"""
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        sign_str = "".join([f"{k}{v}" for k, v in sorted_data]) + secret_key
        sha256 = hashlib.sha256()
        sha256.update(sign_str.encode("utf-8"))
        sign = sha256.hexdigest().upper()
        return sign

    @staticmethod
    def generate_rsa_key():
        """生成RSA密钥对（公钥+私钥）"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        # 保存密钥（示例）
        with open("private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open("public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        return private_key, public_key

    @staticmethod
    def rsa_encrypt(data, public_key):
        """RSA加密"""
        encrypted = public_key.encrypt(
            data.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted.hex()

    @staticmethod
    def get_timestamp():
        """获取时间戳（签名常用）"""
        return str(int(time.time() * 1000))

# 全局实例
sign_util = SignUtil()