import json
from channels.generic.websocket import WebsocketConsumer

class TestBotConsumer(WebsocketConsumer):

    def connect(self):
        return super().connect()

    
    def disconnect(self, code):
        return super().disconnect(code)


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        try:
            if text_data_json["type"] == "q":

                # handle questions
                print(text_data_json)

                reply = {
                    "type":"a",
                    "answer": "answer"
                }
                self.send(
                    json.dumps(reply)
                )
        except:
            pass 

        return None

