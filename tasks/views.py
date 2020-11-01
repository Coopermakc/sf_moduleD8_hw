from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.cache import cache_page
from tasks.models import TodoItem, Category, PriorityHigh, PriorityLow, PriorityMedium
from collections import Counter
from datetime import datetime

def index(request):

    # 1st version
    # counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}

    # 2nd version
    # counts = {t.name: t.taggit_taggeditem_items.count()
    # for t in Tag.objects.all()}

    # 3rd version
    
    counts = Category.objects.all().order_by("-todos_count")
    counts = {c.name: c.todos_count for c in counts}
    
    priorities = {
        'high': PriorityHigh.objects.first().count if PriorityHigh.objects.first() else 0,
        'medium': PriorityMedium.objects.first().count if PriorityMedium.objects.first() else 0,
        'low': PriorityLow.objects.first().count if PriorityLow.objects.first() else 0,
    }

    return render(request, "tasks/index.html", {"counts": counts, "priorities": priorities})


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        categories = []
        for t in user_tasks:
            tags.append(list(t.category.all()))

           
            for cat in t.category.all():
                if cat not in categories:
                    categories.append(cat)
        context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"


@cache_page(60*3)
def cached(request):
    data = datetime.now()
    data_parsed = {
        'year': data.year,
        'month': data.month,
        'day': data.day,
        'hours': data.hour,
        'minutes': data.minute,
        'seconds': data.second,
    }
    return render(request, 'tasks/cached.html', {'data': data_parsed})
