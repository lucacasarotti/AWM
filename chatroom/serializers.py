from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chatroom.models import MessageModel, Room
from rest_framework.serializers import ModelSerializer, CharField


class MessageModelSerializer(ModelSerializer):

    user = CharField(source='user.username', read_only=True)
    recipient = CharField(max_length=255)

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            Room, id=validated_data['recipient'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('id','title',)
