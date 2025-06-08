from django.db import models
from django.utils import timezone

class Todo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    status = models.CharField(
        max_length = 10,
        choices = STATUS_CHOICES,
        default = 'pending',
    )
    due_date = models.DateField()
    created_at = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Return True if the task is overdue and still pending."""
        return (self.status == 'pending' and 
                self.due_date < timezone.now().date())
