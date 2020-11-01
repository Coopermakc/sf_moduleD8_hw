from django.urls import path
from django.views.decorators.cache import cache_page


from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.TaskListView.as_view(), name="list"),
    path("list/c/<slug:cat_slug>", views.tasks_by_cat, name="list_by_cat"),
    path("details/<int:pk>", views.TaskDetailsView.as_view(), name="details"),
    path("cached/", cache_page(60*5)(views.cached), name="cached")
]
