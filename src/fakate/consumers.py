import json
from channels.generic.websocket import WebsocketConsumer
from .answer_my_question import answer_now
from .tasks import async_save_intents, async_save_labels

class TestBotConsumer(WebsocketConsumer):

    def connect(self):
        return super().connect()

    
    def disconnect(self, code):
        return super().disconnect(code)


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        try:
            if text_data_json["type"] == "q":

                # handle questions
                print(text_data_json)
                _, answer = answer_now(text_data_json["botname"], text_data_json["question"])
                reply = {
                    "type":"a",
                    "answer": answer
                }
                self.send(
                    json.dumps(reply)
                )

            elif text_data_json["type"] == "labels":
                labels = text_data_json["data"]
                print("received labels")
                res = async_save_labels.delay(text_data_json["botname"], labels)
                print(res)
                if res != None and res != "no changes":
                    reply = {
                        "type":'labels',
                        "status":"saved"
                    }
                    self.send(
                        json.dumps(reply)
                    )
                    print(intents)
                else:
                    reply = {
                        "type":'labels',
                        "status":"failed to save labels"
                    }
                    self.send(
                        json.dumps(reply)
                    )
                    print("failed to save")

            elif text_data_json["type"] == "intents":
                intents = text_data_json["data"]
                print("received intents")

                res = async_save_intents.delay(text_data_json["botname"], intents)
                if res != None and res != "no changes":
                    reply = {
                        "type":'intents',
                        "status":"saved"
                    }
                    self.send(
                        json.dumps(reply)
                    )
                    print(intents)
                else:
                    reply = {
                        "type":'intents',
                        "status":"failed to save intents"
                    }
                    self.send(
                        json.dumps(reply)
                    )
                    print("failed to save")

        except:
            pass 

        return None

