from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category, PriorityLow, PriorityHigh, PriorityMedium
from collections import Counter

@receiver(m2m_changed, sender=TodoItem.category.through)
def tasks_old_cat(sender, instance, action, model, **kwargs):
    if action != "pre_save":
        return
    try:
        old_categories = TodoItem.objects.get(pk=instance.pk).category.all()
        
        current_categories = instance.category.all()
        if old_categories != current_categories:
            for cat in old_categories:
                if cat not in current_categories:
                    slug = cat.slug

                    new_count = 0

                    for task in TodoItem.objects.all():
                        new_count += task.category.filter(slug=slug).count()
                    new_count -= 1
                    Category.objects.filter(slug=slug).update(todos_count=new_count)

    except TodoItem.DoesNotExist:
        return


@receiver(m2m_changed, sender=TodoItem.category.through)
def tasks_cats_added(sender, instance, action, model, **kwargs):
    if action !="post_add":
        return

    for cat in instance.category.all():
        slug = cat.slug

        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()
        
        Category.objects.filter(slug=slug).update(todos_count=new_count)
    

@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cat_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return
    
    cat_counter = Counter()
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1
    
    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)

@receiver(pre_save, sender=TodoItem)
def task_priority_check(instance, **kwargs):
    try:
        old_priority= TodoItem.objects.get(pk=instance.pk).priority
        if old_priority != instance.priority:
            if old_priority == instance.PRIORITY_HIGH:
                priority = PriorityHigh.objects.first()
                priority.count -= 1
                priority.save()
            elif old_priority == instance.PRIORITY_MEDIUM:
                priority = PriorityMedium.objects.first()
                priority.count -= 1
                priority.save()
            else:
                priority = PriorityLow.objects.first()
                priority.count -= 1
                priority.save()
    except TodoItem.DoesNotExist:
        return




@receiver(post_save, sender=TodoItem)
def task_priority_add(instance, **kwargs):
    
    if instance.priority == 1:
        priority, created = PriorityHigh.objects.get_or_create()
        if created:
            priority.count = 1
        else:
            priority.count +=1
        priority.save()

    if instance.priority == 2:
        priority, created = PriorityMedium.objects.get_or_create()
        if created:
            priority.count = 1
        else:
            priority.count +=1
        priority.save()  
    
    if instance.priority == 3:
        priority, created = PriorityLow.objects.get_or_create()
        if created:
            priority.count = 1
        else:
            priority.count +=1
        priority.save() 
    
    


