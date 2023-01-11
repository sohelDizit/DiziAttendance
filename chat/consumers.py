import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        print("connect")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message=None
        UID=None
        Redirect=None
        OtherMessage=None
        if 'message' in text_data_json:
            message = text_data_json['message']

        if 'UID' in text_data_json:
            UID= text_data_json['UID']

        if 'Redirect' in text_data_json:
            Redirect= text_data_json['Redirect']

        if 'OtherMessage' in text_data_json:
            OtherMessage= text_data_json['OtherMessage']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'UID':UID,
                'Redirect':Redirect,
                'OtherMessage':OtherMessage
            }
        )

    def chat_message(self, event):
        message=None
        UID=None
        Redirect=None
        OtherMessage=None

        if 'message' in event:
            message = event['message']

        if 'UID' in event:
            UID= event['UID']

        if 'Redirect' in event:
            Redirect= event['Redirect']

        if 'OtherMessage' in event:
            OtherMessage= event['OtherMessage']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'UID':UID,
            'Redirect':Redirect,
            'OtherMessage':OtherMessage
        }))