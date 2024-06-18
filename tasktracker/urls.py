from django.urls import path
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskListByStatusView,
    AllTasksListView,
    MarkTaskAsCompletedView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("all/", AllTasksListView.as_view(), name="all-tasks-list"),
    path("<int:pk>/", TaskRetrieveUpdateDestroyView.as_view(), name="task-detail"),
    path(
        "status/<str:task_status>/",
        TaskListByStatusView.as_view(),
        name="task-list-by-status",
    ),
    path("<int:pk>/complete/", MarkTaskAsCompletedView.as_view(), name="mark-task-as-completed"),
]
