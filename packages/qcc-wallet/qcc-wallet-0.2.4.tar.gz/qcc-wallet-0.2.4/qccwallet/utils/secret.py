import rsa
import base64
from tweb.error_exception import ErrException, ERROR
from tweb.tools import gen_sha256
from tweb import time
import binascii


def verify_msg(msg):
    pwd = ''
    if 'password' in msg:
        password = msg.get('password')
        if password is not None:
            try:
                pwd_bytes = base64.b64decode(password)
                with open('./rsa_pri_key') as key_file:
                    pri_str = key_file.read()
                    pwd = rsa.decrypt(pwd_bytes, rsa.PrivateKey.load_pkcs1(pri_str.encode())).decode()
            except Exception:
                pwd = password
        else:
            pwd = ''

    message_sign = msg.get('message_sign')
    if message_sign is not None:
        msg.pop('message_sign')
        temp = _json_serialize(msg)
        temp += pwd

        tmp_sign = gen_sha256(temp)
        if tmp_sign != message_sign:
            raise ErrException(ERROR.E40000, extra='verify msg failed, wrong message_sign')

    ts = msg.get('message_ts')
    if ts is not None:
        msg.pop('message_ts')
        if time.millisecond() - ts > 600 * 1000:
            raise ErrException(ERROR.E40000, extra='verify msg failed, message_sign timeout')

    if 'password' in msg:
        msg.pop('password')
    return pwd


def _json_serialize(obj, depth=0):
    if depth >= 5:
        return ''

    temp = ''
    if isinstance(obj, dict):
        for k, v in sorted(obj.items()):
            temp += k
            if isinstance(v, list) or isinstance(v, dict):
                temp += _json_serialize(v, depth=depth + 1)
            else:
                temp += str(v)
    elif isinstance(obj, list):
        for i in obj:
            if isinstance(i, list) or isinstance(i, dict):
                temp += _json_serialize(i, depth=depth + 1)
            else:
                temp += str(i)

    return temp


if __name__ == "__main__":
    msg = {
        "sender": "0x58a81beab5f9948114d267ee834d82928accb030",
        "method": "transfer",
        "user": {
            "name": 'YANG',
            "job": "IT"
        },
        "method_args": [
            "0xe7eaaf9d7ef1d949795a311d2782b9f42bbb0ae0",
            1500000000000000,
            {
                'work': "aaa",
                'level': 12
            },
            [
                'a', 'y', 'c', 121.00112
            ]
        ],
        "password": "123456"
    }
    ret = _json_serialize(msg)
    print(ret)
