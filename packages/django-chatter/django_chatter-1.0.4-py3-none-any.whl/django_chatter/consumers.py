'''AI--------------------------------------------------------------------------
    Django Imports
--------------------------------------------------------------------------AI'''
from django.contrib.auth import get_user_model
from django.db import connection


'''AI--------------------------------------------------------------------------
    Third-party Imports
--------------------------------------------------------------------------AI'''
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import bleach


'''AI--------------------------------------------------------------------------
    App Imports
--------------------------------------------------------------------------AI'''
from .models import Room, Message


'''AI--------------------------------------------------------------------------
    Python Imports
--------------------------------------------------------------------------AI'''
import json
from uuid import UUID


'''
AI-------------------------------------------------------------------
    Database Access methods below
-------------------------------------------------------------------AI
'''
@database_sync_to_async
def get_room(room_id, multitenant=False, schema_name=None):
    if multitenant:
        if not schema_name:
            raise AttributeError("Multitenancy support error: \
                scope does not have multitenancy details added. \
                did you forget to add ChatterMTMiddlewareStack to your routing?")
        else:
            from django_tenants.utils import schema_context
            with schema_context(schema_name):
                return Room.objects.get(id=room_id)
    else:
        return Room.objects.get(id=room_id)


'''
AI-------------------------------------------------------------------
    1. Select the Room
    2. Select the user who sent the message
    3. Select the message to be saved
    4. Save message
    5. Set room update time to message date_modified
-------------------------------------------------------------------AI
'''
@database_sync_to_async
def save_message(room, sender, text, multitenant=False, schema_name=None):
    if multitenant:
        if not schema_name:
            raise AttributeError("Multitenancy support error: \
                scope does not have multitenancy details added. \
                did you forget to add ChatterMTMiddlewareStack to your routing?")
        else:
            from django_tenants.utils import schema_context
            with schema_context(schema_name):
                new_message = Message(room=room, sender=sender, text=text)
                new_message.save()
                new_message.recipients.add(sender)
                new_message.save()
                room.date_modified = new_message.date_modified
                room.save()
                return new_message.date_created
    else:
        new_message = Message(room=room, sender=sender, text=text)
        new_message.save()
        new_message.recipients.add(sender)
        new_message.save()
        room.date_modified = new_message.date_modified
        room.save()
        return new_message.date_created


class ChatConsumer(AsyncJsonWebsocketConsumer):

    '''
    AI-------------------------------------------------------------------
        WebSocket methods below
    -------------------------------------------------------------------AI
    '''
    async def connect(self):
        self.user = self.scope['user']

        self.schema_name = self.scope.get('schema_name', None)
        self.multitenant = self.scope.get('multitenant', False)
        for param in self.scope['path'].split('/'):
            try:
                room_id = UUID(param, version=4)
                break
            except ValueError:
                pass
        try:
            self.room = await get_room(room_id, self.multitenant, self.schema_name)
            if self.multitenant:
                from django_tenants.utils import schema_context
                with schema_context(self.schema_name):
                    if self.user in self.room.members.all():
                        room_group_name = 'chat_%s' % self.room.id
                        await self.channel_layer.group_add(
                            room_group_name,
                            self.channel_name
                        )
                        await self.accept()
                    else:
                        await self.disconnect(403)
            else:
                if self.user in self.room.members.all():
                    room_group_name = 'chat_%s' % self.room.id
                    await self.channel_layer.group_add(
                        room_group_name,
                        self.channel_name
                    )
                    await self.accept()
                else:
                    await self.disconnect(403)
        except Exception as ex:
            raise ex
            await self.disconnect(500)

    async def disconnect(self, close_code):
        room_group_name = 'chat_%s' % self.room.id
        await self.channel_layer.group_discard(
            room_group_name,
            self.channel_name
        )

    async def receive_json(self, data):
        username = self.user.username

        message_type = data['type']
        if message_type == "text":
            message = data['message']
            room_id = data['room_id']

            # Clean code off message if message contains code
            self.message_safe = bleach.clean(message)
            message_harmful = (self.message_safe != message)

            try:
                # room = await self.get_room(room_id)
                room_group_name = 'chat_%s' % room_id
            except Exception as ex:
                raise ex
                await self.disconnect(500)

            time = await save_message(self.room,
                                    self.user,
                                    self.message_safe,
                                    self.multitenant,
                                    self.schema_name
                                    )
            time = time.strftime("%d %b %Y %H:%M:%S %Z")


            if message_harmful:
                warning = "Your message has been escaped due to security reasons.\
                 For more information, see \
                 https://en.wikipedia.org/wiki/Cross-site_scripting"
            else:
                warning = ''

            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'send_to_websocket',
                    'message_type': 'text',
                    'message': self.message_safe,
                    'date_created': time,
                    'warning': warning,
                    'sender': username,
                    'room_id': room_id,
                }
            )

    async def send_to_websocket(self, event):
        await self.send_json(event)
