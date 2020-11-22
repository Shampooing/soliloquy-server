from rest_framework import viewsets

from soliloquy.models import User, Tag, Entry, Note, Reference, Notebook, Task, Project, Event, Saga
from soliloquy.serializers import UserSerializer, NoteSerializer, TagSerializer, \
    ReferenceSerializer, NoteBookSerializer, TaskSerializer, ProjectSerializer, EventSerializer, SagaSerializer, \
    EntryPolymorphicSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntryPolymorphicSerializer


class NotebookViewSet(viewsets.ModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NoteBookSerializer


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SagaViewSet(viewsets.ModelViewSet):
    queryset = Saga.objects.all()
    serializer_class = SagaSerializer

