from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)


class TaskListByStatusView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        task_status = self.kwargs['task_status']
        if self.request.user.is_superuser:
            return Task.objects.filter(status=task_status)
        return Task.objects.filter(status=task_status, user=self.request.user)
