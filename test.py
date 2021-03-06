from message import app
from nose import *
from nose.tools import *
from datetime import datetime

from flask import json

class TestAPI:


    @classmethod
    def setup_class(self):
        self.app = app.test_client()

    @classmethod
    def teardown_class(self):
        print("teardown_class():")

    def setup(self):
        pass
        
    def teardown(self):
        pass

    def get_message(self, index):
        response = self.app.get('/messages/api/message/'+str(index))

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 200)

        body = json.loads(response.data)
        message = body['messages']
        eq_(message['id'],index)
        eq_(message['is_read'], True)

        return message


    def create_message(self, message):
        response = self.app.post('/messages/api/message',
                                data = json.dumps(message),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 201)

        body = json.loads(response.data)
        message_received = body['message']
        eq_(message_received['sender'], message['sender'])

        # Retreive the last message and test that is the message created
        last_message = self.get_message(message_received['id'])
        eq_(last_message['sender'], message['sender'])

        return message_received
        

    def test_create_messages(self):
        message = {
                'sender': 'Peter',
                'message': 'test test'
                }

        self.create_message(message)


    def test_create_message_bad_request(self):

        # Request without json
        response = self.app.post('messages/api/message',
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code,400)

        # Request without 'message'
        response = self.app.post('messages/api/message',
                                data = json.dumps({'sender':u'Phill'}),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code,400)

        # Request with 'message' but not unicode
        response = self.app.post('messages/api/message',
                                data = json.dumps({'message':234534634}),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code,400)


    def test_get_message(self):
        self.get_message(1)

    def test_get_message_not_found(self):
        response = self.app.get('/messages/api/message/45')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code,404)

    def test_get_all_messages(self):
        response = self.app.get('/messages/api/message/all')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code,200)

        body = json.loads(response.data)
        message = body['messages']
        assert_true(len(message) > 0)


    def test_edit_message(self):
        response = self.app.put('messages/api/message/3',
                                data = json.dumps({'message':u'content edited'}),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 200)

        body = json.loads(response.data)
        message = body['message']
        eq_(message['sender'], 'Peter')
        eq_(message['message'], 'content edited')


    def test_edit_message_not_found(self):
        response = self.app.put('messages/api/message/14',
                                data = json.dumps({'message':u'content edited'}),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 404)


    def test_edit_message_bad_request(self):

        # Request without json
        response = self.app.put('messages/api/message/3',
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 400)

        # Request without 'message'
        response = self.app.put('messages/api/message/3',
                                data = json.dumps({'sender':u'Phill'}),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 400)

        # Request with 'message' but not unicode
        response = self.app.put('messages/api/message/3',
                                data = json.dumps({'message':56546}),
                                content_type='application/json')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 400)


    def test_delete_message(self):
        message = {
            'sender':'Paul',
            'message': 'deleted'
        }
        message_received = self.create_message(message)

        response = self.app.delete('messages/api/message/' + str(message_received['id']))

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 200)

        body = json.loads(response.data)
        assert_true(body['deleted'])

    def test_delete_message_not_found(self):

        response = self.app.delete('messages/api/message/35')

        eq_(response.headers['Content-Type'], 'application/json')
        eq_(response.status_code, 404)
