from django.contrib import admin

from soliloquy.models import User, Entry, Note, Notebook, Event, Saga, Task, Project, Tag, Reference

# Register your models here.


for m in [User, Entry, Note, Notebook, Event, Saga, Task, Project, Tag, Reference]:
    admin.site.register(m)
