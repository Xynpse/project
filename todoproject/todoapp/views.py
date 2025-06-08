from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django import forms
from .models import Todo

# Create your views here.

class TodoListView(ListView):
    """View for displaying the list of todos with filtering and sorting."""
    model = Todo
    template_name = 'todoapp/todo_list.html'
    context_object_name = 'todos'
    ordering = ['-created_at']

    def get_queryset(self):
        """Return filtered and sorted queryset based on request parameters."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        sort_by = self.request.GET.get('sort', '-created_at')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        """Add status choices to the context."""
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Todo.STATUS_CHOICES
        return context


class TodoCreateView(CreateView):
    """View for creating new todos."""
    model = Todo
    template_name = 'todoapp/todo_form.html'
    fields = ['title', 'description', 'due_date']
    success_url = reverse_lazy('todoapp:todo-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        form.fields['description'].widget.attrs.update({'class': 'form-control w-100'})
        return form

    def form_valid(self, form):
        """Add success message after form validation."""
        messages.success(self.request, 'Todo created successfully!')
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    """View for updating existing todos."""
    model = Todo
    template_name = 'todoapp/todo_form.html'
    fields = ['title', 'description', 'status', 'due_date']
    success_url = reverse_lazy('todoapp:todo-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        form.fields['description'].widget.attrs.update({'class': 'form-control w-100'})
        return form

    def form_valid(self, form):
        """Add success message after form validation."""
        messages.success(self.request, 'Todo updated successfully!')
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    """View for deleting todos."""
    model = Todo
    template_name = 'todoapp/todo_confirm_delete.html'
    success_url = reverse_lazy('todoapp:todo-list')

    def delete(self, request, *args, **kwargs):
        """Add success message after deletion."""
        messages.success(request, 'Todo deleted successfully!')
        return super().delete(request, *args, **kwargs)
