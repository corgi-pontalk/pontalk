Categories: Productivity
Tags: Productivity, Django, Coding Skills
---

# Creating a Productivity App with Django and SQLite

---

## Introduction

In today's fast-paced world, staying organized and productive is more crucial than ever. While there are countless productivity tools available, building your own can be an incredibly rewarding experience, offering a tailored solution and a deep dive into web development fundamentals.

This tutorial will guide you through creating a simple, yet functional, productivity application using **Django**, a high-level Python web framework, and **SQLite**, a lightweight, file-based database that comes pre-installed with Python. By the end, you'll have a web application capable of managing your tasks, and you'll have a solid foundation for building more complex Django projects.

---

## Prerequisites

Before we begin, ensure you have the following installed on your system:

*   **Python 3.x**: You can download it from [python.org](https://www.python.org/).
*   **pip**: Python's package installer (usually comes with Python).

---

## 1. Setting Up Your Django Project

Let's start by creating a virtual environment, which is good practice to isolate your project's dependencies.

### 1.1 Create a Virtual Environment

Open your terminal or command prompt and run:

```bash
python3 -m venv venv
```

Activate the virtual environment:

*   **macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```
*   **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```

### 1.2 Install Django

With your virtual environment activated, install Django:

```bash
pip install Django
```

### 1.3 Create a New Django Project and App

Now, let's create our Django project (`productivity_app`) and a specific application within it (`tasks`).

```bash
django-admin startproject productivity_app .
python manage.py startapp tasks
```

The `.` after `productivity_app` tells Django to create the project in the current directory, avoiding an extra nested folder.

### 1.4 Register Your App

For Django to recognize our `tasks` app, we need to add it to the `INSTALLED_APPS` list in `productivity_app/settings.py`.

```python
# productivity_app/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks', # Add your new app here
]
```

---

## 2. Defining the Data Model (SQLite)

Django uses an Object-Relational Mapper (ORM) to interact with databases. We'll define our `Task` model in `tasks/models.py`. By default, Django uses SQLite, which is perfect for this simple application.

### 2.1 Create the Task Model

Edit `tasks/models.py` to define our `Task` model:

```python
# tasks/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

*   `CharField`: For short text inputs like the task title.
*   `TextField`: For longer text, like a description. `blank=True` allows it to be empty in forms, and `null=True` allows it to be `NULL` in the database.
*   `DateTimeField`: Automatically sets the creation time.
*   `DateField`: For the due date.
*   `BooleanField`: For a simple true/false status (completed or not).

### 2.2 Make and Apply Migrations

After defining your model, you need to create database migrations and apply them. This tells Django to create the corresponding table in your SQLite database.

```bash
python manage.py makemigrations tasks
python manage.py migrate
```

You'll see output indicating that Django created a `db.sqlite3` file in your project root.

---

## 3. Creating the Views

Views are Python functions or classes that receive web requests and return web responses. They are where we'll implement the logic for listing, creating, updating, and deleting tasks.

Edit `tasks/views.py`:

```python
# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm # We'll create this next!

def task_list(request):
    tasks = Task.objects.all().order_by('due_date', 'created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'page_title': 'Create Task'})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'page_title': 'Update Task'})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
```

Notice we're importing `TaskForm`. We haven't created it yet, but it's a Django convenience for handling forms automatically from models.

### 3.1 Create Forms

Create a new file `tasks/forms.py` for our `TaskForm`:

```python
# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}), # HTML5 date picker
        }
```

Here, `ModelForm` automatically generates form fields based on our `Task` model. We customize the `due_date` widget for a better user experience with an HTML5 date picker.

---

## 4. Designing the URLs

URLs map web addresses to the views we just created.

### 4.1 App-Level URLs

Create a new file `tasks/urls.py`:

```python
# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
]
```

### 4.2 Project-Level URLs

Include the app's URLs in the main project's `productivity_app/urls.py`:

```python
# productivity_app/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')), # Include your tasks app URLs here
]
```
Now, all requests to the root path (`/`) will be handled by our `tasks` app.

---

## 5. Building the Templates

Templates define the HTML structure of our web pages. Create a `templates` directory inside your `tasks` app, and then a `tasks` directory inside that: `tasks/templates/tasks/`.

### 5.1 Base Template (`tasks/templates/base.html`)

It's good practice to have a base template for consistent navigation and styling. Create `tasks/templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Productivity App - {% block title %}{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1, h2 { color: #0056b3; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { list-style: none; padding: 0; }
        li { background: #e9ecef; margin-bottom: 10px; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
        .completed { text-decoration: line-through; color: #6c757d; }
        .button { background-color: #007bff; color: white; padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; }
        .button:hover { background-color: #0056b3; }
        .delete-button { background-color: #dc3545; }
        .delete-button:hover { background-color: #c82333; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input[type="text"],
        .form-group input[type="date"],
        .form-group textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box; /* Ensures padding doesn't affect total width */
        }
        .form-group input[type="checkbox"] {
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

### 5.2 Task List Template (`tasks/templates/tasks/task_list.html`)

This template will display all our tasks.

```html
{% extends 'base.html' %}

{% block title %}Task List{% endblock %}

{% block content %}
    <h1>My Tasks</h1>
    <a href="{% url 'task_create' %}" class="button">Add New Task</a>
    {% if tasks %}
        <ul>
            {% for task in tasks %}
                <li>
                    <span class="{% if task.completed %}completed{% endif %}">
                        <strong>{{ task.title }}</strong>
                        {% if task.due_date %} - Due: {{ task.due_date|date:"M d, Y" }}{% endif %}
                    </span>
                    <div>
                        <a href="{% url 'task_update' task.pk %}" class="button">Edit</a>
                        <a href="{% url 'task_delete' task.pk %}" class="button delete-button">Delete</a>
                    </div>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No tasks yet. Why not <a href="{% url 'task_create' %}">add one</a>?</p>
    {% endif %}
{% endblock %}
```

### 5.3 Task Form Template (`tasks/templates/tasks/task_form.html`)

This template will be used for both creating and updating tasks.

```html
{% extends 'base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
    <h1>{{ page_title }}</h1>
    <form method="post">
        {% csrf_token %}
        {% for field in form %}
            <div class="form-group">
                {{ field.label_tag }}
                {{ field }}
                {% if field.help_text %}
                    <small>{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <p style="color: red;">{{ error }}</p>
                {% endfor %}
            </div>
        {% endfor %}
        <button type="submit" class="button">Save Task</button>
        <a href="{% url 'task_list' %}" class="button">Cancel</a>
    </form>
{% endblock %}
```

### 5.4 Task Confirm Delete Template (`tasks/templates/tasks/task_confirm_delete.html`)

This template asks for confirmation before deleting a task.

```html
{% extends 'base.html' %}

{% block title %}Confirm Delete{% endblock %}

{% block content %}
    <h1>Delete Task</h1>
    <p>Are you sure you want to delete the task: "<strong>{{ task.title }}</strong>"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="button delete-button">Confirm Delete</button>
        <a href="{% url 'task_list' %}" class="button">Cancel</a>
    </form>
{% endblock %}
```

---

## 6. Running the Application

You're almost there! Run the Django development server:

```bash
python manage.py runserver
```

Open your web browser and navigate to `http://127.0.0.1:8000/`.

You should see your task list application.
*   Click "Add New Task" to create a new task.
*   Fill out the form and save.
*   You can edit or delete existing tasks using the respective buttons.

---

## Conclusion and Next Steps

Congratulations! You've successfully built a basic productivity application using Django and SQLite. You've touched upon core Django concepts including:

*   Project and App structure
*   Models (ORM) and migrations
*   Views (business logic)
*   URL routing
*   Templates (HTML rendering with Django Template Language)
*   Forms (ModelForm)

This is just the beginning. Here are some ideas to expand your app:

*   **User Authentication**: Allow users to create accounts and manage their own tasks.
*   **Categories/Tags**: Add fields to categorize tasks.
*   **Priorities**: Implement different priority levels for tasks.
*   **Due Date Reminders**: Send email or in-app notifications.
*   **Better Styling**: Integrate a CSS framework like Bootstrap or Tailwind CSS.
*   **Deployment**: Learn how to deploy your Django app to a production server (e.g., Heroku, Vercel, AWS).

Django's power lies in its comprehensive ecosystem and "batteries-included" philosophy. Keep experimenting and building! If you have any questions or further ideas, feel free to share them in the comments below.
