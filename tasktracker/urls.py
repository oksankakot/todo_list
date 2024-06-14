from django.urls import path
from .views import (
    TaskDetailView,
    TaskListView,
    UserTaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListByStatusView,
)

urlpatterns = [
    path("all-tasks/", TaskListView.as_view(), name="all-tasks-list"),
    path("user-tasks/", UserTaskListView.as_view(), name="user-tasks-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("create-task/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "tasks-by-status/<str:status>/",
        TaskListByStatusView.as_view(),
        name="tasks-by-status",
    ),
]