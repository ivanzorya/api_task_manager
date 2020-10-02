from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Task, Change
from .serializers import TaskSerializer, ChangeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', ]

    def perform_create(self, serializer):
        serializer.save(is_active=True)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        queryset = self.queryset.filter(author=self.request.user)
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        if self.request.query_params.get('status'):
            queryset = queryset.filter(
                status=self.request.query_params.get('status')
            )
        if self.request.query_params.get('after'):
            queryset = queryset.filter(
                completed__gte=self.request.query_params.get('after')
            )
        if self.request.query_params.get('before'):
            queryset = queryset.filter(
                completed__lte=self.request.query_params.get('before')
            )
        if self.request.query_params.get('date'):
            queryset = queryset.filter(
                completed=self.request.query_params.get('date')
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        task = get_object_or_404(
            Task,
            pk=self.kwargs.get('pk')
        )
        fields = ['title', 'description', 'completed', 'status']
        changes = {}
        for field in fields:
            data = self.request.data.get(field)
            if data:
                changes[field] = data
        for key in changes:
            Change.objects.create(
                author=self.request.user,
                task=task,
                field_name=key,
                old_value=getattr(task, key),
                new_value=changes[key],
            )
        serializer.save(
            author=self.request.user,
        )


class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        task = get_object_or_404(
            Task,
            pk=self.kwargs.get('task_id')
        )
        return task.changes.all()
