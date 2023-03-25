from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPageNumberPagination
from api.serializers import FollowSerializer
from users.models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    @action(detail=True, permission_classes=[IsAuthenticated],
            methods=['POST', 'DELETE'])
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)

        if self.request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого автора!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(
                Follow.objects.create(user=user, author=author),
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if user == author:
                return Response(
                    {'errors': 'Нельзя отписаться от самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=user, author=author).exists():
                Follow.objects.filter(user=user, author=author).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'errors': 'Отписка уже произведена!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=['GET'])
    def subscriptions(self, request):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages, many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)
