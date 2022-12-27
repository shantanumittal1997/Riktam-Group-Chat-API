from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from chats.models import ChatGroup, GroupMember, Message
from chats.serializers import ChatGroupSerializer, MembersSerializer, MessageSerializer
from users.serializers import UserSerializer
from core.utils import create_response

class ChatGroupViewSet(ModelViewSet):

    """
    Viewset for CRUD operations related to chat groups
    """

    serializer_class = ChatGroupSerializer
    queryset = ChatGroup.objects.all()
    permission_classes = [IsAuthenticated,]

class AddMemberView(APIView):

    """
    View to add users to group and searching users to add
    """

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        users = User.objects.filter(is_superuser=False, is_staff=False)
        if 'search' in request.query_params:
            search = request.query_params.get('search')
            users = users.filter(Q(email__ilike = search)|Q(firstname__ilike = search)|Q(lastname__ilike = search))

        ser = UserSerializer(users, many=True)
        return create_response(
            message="Success",
            status=status.HTTP_200_OK,
            data=ser.data()
        )

    def post(self, request):
        if 'group_id' not in request.data:
            return create_response(
                message="Missing key 'group_id' in payload",
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'members' not in request.data:
            return create_response(
                message="Missing key 'members' in payload",
                status=status.HTTP_400_BAD_REQUEST
            )

        group_id = request.data.get('group_id')
        members = request.data.get('members')
        if not isinstance(members, list):
            return create_response(
                message="Invalid payload",
                status=status.HTTP_400_BAD_REQUEST
            )

        member_objs = list()
        for member in members:
            member_obj = GroupMember(
                user_id=member,
                group_id=group_id
            )
            member_objs.append(member_obj)

        try:
            GroupMember.objects.bulk_create(member_objs)
        except:
            return create_response(
                message="Error while adding members",
                status=status.HTTP_400_BAD_REQUEST
            )

        return create_response(
            message="Success",
            status=status.HTTP_200_OK
        )

class ViewMembers(APIView):

    """
    API to view group members
    """

    permission_classes = [IsAuthenticated,]

    def get(self, request, group_id):
        members = GroupMember.objects.filter(group_id=group_id)
        if not members.filter(user=request.user).exists():
            return create_response(
                message="Not a group member",
                status=status.HTTP_400_BAD_REQUEST
            )
        ser = MembersSerializer(members, many=True)
        return create_response(
            message="Success",
            status=status.HTTP_200_OK,
            data=ser.data()
        )

class MessageViewSet(ModelViewSet):

    """
    Viewset for CRUD operations related to messages
    """

    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = MessageSerializer