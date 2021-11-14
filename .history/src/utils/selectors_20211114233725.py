from users.models import User


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


def jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    return {
        'token': token,
        'user': user_get_me(user=user),
    }
    
    
def jwt_encode_payload(payload):
    """Encode JWT token claims."""

    headers=None

    signing_algorithm = "RS256"
    
    key = ""

    if isinstance(key, dict):
        kid, key = next(iter(key.items()))
        headers = {"kid": kid}
    elif isinstance(key,list):
        key = key[0]

    enc = jwt.encode(payload, key, signing_algorithm, headers=headers, json_encoder=JSONEncoder)
    if jwt_version == 1:
        enc = enc.decode()
    return enc