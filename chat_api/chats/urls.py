from django.urls import path
from rest_framework.routers import DefaultRouter
from chats.views import *

app_name = "chats"

router = DefaultRouter()
router.register('groups', ChatGroupViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    path('add-member', AddMemberView.as_view(), name="add-member"),
    path('get-member', ViewMembers.as_view(), name="get-member"),
]
urlpatterns += router.urls