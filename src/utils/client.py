import requests as rq

# send user id
def send_user_id(service_id, url , user_id):

    headers = {
        "Content-Type":"application/json"
    }

    data = {
        "service_id":service_id,
        "user_id":user_id
    }

    res = rq.post(url=url, data=data, headers=headers)

    return res.json()