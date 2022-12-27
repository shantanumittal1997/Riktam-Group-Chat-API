from django.db import models
from django.contrib.auth.models import User
from core.models import CreatedByModel, CreateAndUpdateModel

class ChatGroup(CreatedByModel):
    name = models.CharField(max_length=512)

class GroupMember(CreateAndUpdateModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)

class Message(CreateAndUpdateModel):
    text = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    member = models.ForeignKey(GroupMember, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
