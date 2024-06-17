from django.urls import path
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskListByStatusView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskRetrieveUpdateDestroyView.as_view(), name="task-detail"),
    path(
        "status/<str:task_status>/",
        TaskListByStatusView.as_view(),
        name="task-list-by-status",
    ),
]
