from rest_framework.serializers import ModelSerializer
from chats.models import ChatGroup, GroupMember, Message
from users.serializers import UserSerializer

class ChatGroupSerializer(ModelSerializer):

    class Meta:
        model = ChatGroup
        fields = "__all__"

class MembersSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ('user',)

class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"


