from users.models import User
import jwt
from rest_framework.utils.encoders import JSONEncoder
from rest_framework_jwt.compat import  jwt_decode, jwt_version
from rest_framework_jwt.settings import api_settings
from users.models import RSAPair
import base64 as b64
# from jwt.algorithms import RSAAlgorithm
# jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

def user_get_services(user: User):
    all = {}
    for i in  user.services.all():
        all[i.service.service_id] = i.service.service_key
    return all

def user_get_me(*, user: User):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'services':user_get_services(user)
    }
    
    
def get_rsa_key(type: str):
    
    key = RSAPair.objects.first()
    
    if type == "public":
        return key.public_key
    
    if type == "private":
        return key.private_key
    
    return None



def jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    return {
        'token': token,
        'user': user_get_me(user=user),
    }
    
    
def jwt_encode_payload(payload):
    """Encode JWT token claims."""

    headers=None

    signing_algorithm = "RS256"
    #private key
    key = get_rsa_key("private")
    key = b64.b64decode()          
    print(f"""
          
          {key}
          
          """)

    if isinstance(key, dict):
        kid, key = next(iter(key.items()))
        headers = {"kid": kid}
    elif isinstance(key,list):
        key = key[0]

    enc = jwt.encode(payload, key, signing_algorithm, headers=headers, json_encoder=JSONEncoder)
    return enc


def jwt_decode_token(token):
    """Decode JWT token claims."""

    if jwt_version == 2 and type(token) == bytes:
        token = token.decode()

    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }

    algorithms = api_settings.JWT_ALGORITHM
    if not isinstance(algorithms, list):
        algorithms = [algorithms]

    hdr = jwt.get_unverified_header(token)
    alg_hdr = hdr["alg"]
    if alg_hdr not in algorithms:
        raise jwt.exceptions.InvalidAlgorithmError

    kid = hdr["kid"] if "kid" in hdr else None
    #public key
    keys = get_rsa_key("public")

    # if keys are named and the jwt has a kid, only consider exactly that key
    # otherwise if the JWT has no kid, JWT_INSIST_ON_KID selects if we fail
    # or try all defined keys
    if isinstance(keys, dict):
        if kid:
            try:
                keys = keys[kid]
            except KeyError:
                raise jwt.exceptions.InvalidTokenError
        elif api_settings.JWT_INSIST_ON_KID:
            raise jwt.exceptions.InvalidTokenError
        else:
            keys = list(keys.values())

    if not isinstance(keys, list):
        keys = [keys]

    ex = None
    for key in keys:
        try:
            return jwt_decode(
                token, key, verify=api_settings.JWT_VERIFY, options=options,
                leeway=api_settings.JWT_LEEWAY,
                audience=api_settings.JWT_AUDIENCE,
                issuer=api_settings.JWT_ISSUER, algorithms=[alg_hdr]
            )
        except (jwt.exceptions.InvalidSignatureError) as e:
                ex = e
    raise ex
