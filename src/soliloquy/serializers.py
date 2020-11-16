from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from soliloquy.models import DjangoUser, User, Client, Tag, Entry, Reference, Note, Notebook, Task, Project, Event, Saga


class DjangoUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    django_user = DjangoUserSerializer(required=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('django_user')
        django_user = DjangoUserSerializer.create(DjangoUserSerializer(), validated_data=user_data)
        user, created = User.objects.update_or_create(django_user=django_user, **validated_data)
        return user


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'url', 'name', 'owner']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('source') == attrs.get('target'):
            raise serializers.ValidationError(
                "Self-references are not allowed. Attempted by Entry '{}'."
                .format(attrs.get('source'))
            )
        return attrs


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    references = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='reference-detail')
    referenced_by = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='reference-detail')

    creation_date = serializers.DateTimeField(format="iso-8601")

    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = Entry
        fields = ['id', 'client', 'creation_date', 'active', 'name', 'content', 'tags', 'references', 'referenced_by']


class AbstractEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ['url', 'id', 'client', 'creation_date', 'active', 'name', 'content', 'tags', 'references',
                  'referenced_by', 'specialized_url']


class NoteSerializer(EntrySerializer):
    specialized_url = serializers.HyperlinkedIdentityField(view_name='note-detail')

    class Meta:
        model = Note
        fields = AbstractEntrySerializer.Meta.fields + ['parent_notebook']
        extra_kwargs = {
            'url': {'view_name': 'entry-detail', 'lookup_field': 'pk'},
        }


class NoteBookSerializer(EntrySerializer):
    specialized_url = serializers.HyperlinkedIdentityField(view_name='notebook-detail')

    class Meta:
        model = Notebook
        fields = AbstractEntrySerializer.Meta.fields + ['notes']
        extra_kwargs = {
            'url': {'view_name': 'entry-detail', 'lookup_field': 'pk'},
            'notes': {'read_only': True}
        }


class TaskSerializer(EntrySerializer):
    specialized_url = serializers.HyperlinkedIdentityField(view_name='task-detail')

    class Meta:
        model = Task
        fields = AbstractEntrySerializer.Meta.fields + ['due_date', 'expiration_date', 'recurrence', 'priority',
                                                        'effort_estimate', 'unit_of_work', 'parent_project', 'assignee',
                                                        'done']
        extra_kwargs = {
            'url': {'view_name': 'entry-detail', 'lookup_field': 'pk'},
        }

    def validate(self, attrs):
        if (attrs.get('expiration_date') and attrs.get('due_date')
                and attrs.get('due_date') > attrs.get('expiration_date')):
            raise serializers.ValidationError(
                "Due date {} on task '{}' cannot be set after after expiration date {}."
                .format(attrs['due_date'], attrs['name'], attrs['expiration_date'])
            )
        if attrs.get('parent_project') and attrs.get('due_date'):
            dd = attrs['due_date']
            p = attrs['parent_project']
            pdd = p.due_date
            if pdd and dd > pdd:
                raise serializers.ValidationError(
                    "Due date {} on task '{}' cannot be set after due date {} of project {}"
                        .format(dd, attrs['name'], pdd, p)
                )
        return attrs


class ProjectSerializer(EntrySerializer):
    specialized_url = serializers.HyperlinkedIdentityField(view_name='project-detail')

    class Meta:
        model = Project
        fields = AbstractEntrySerializer.Meta.fields + ['due_date', 'priority', 'unit_of_work', 'tasks']
        extra_kwargs = {
            'url': {'view_name': 'entry-detail', 'lookup_field': 'pk'},
            'tasks': {'read_only': True}
        }


class EventSerializer(EntrySerializer):
    specialized_url = serializers.HyperlinkedIdentityField(view_name='event-detail')

    class Meta:
        model = Event
        fields = AbstractEntrySerializer.Meta.fields + [
            'start_date', 'end_date', 'all_day', 'start_time', 'end_time', 'parent_saga'
        ]
        extra_kwargs = {
            'url': {'view_name': 'entry-detail', 'lookup_field': 'pk'},
        }


class SagaSerializer(EntrySerializer):
    specialized_url = serializers.HyperlinkedIdentityField(view_name='saga-detail')

    class Meta:
        model = Saga
        fields = AbstractEntrySerializer.Meta.fields + ['events']
        extra_kwargs = {
            'url': {'view_name': 'entry-detail', 'lookup_field': 'pk'},
            'events': {'read_only': True}
        }


class EntryPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Entry: EntrySerializer,
        Note: NoteSerializer,
        Notebook: NoteBookSerializer,
        Task: TaskSerializer,
        Project: ProjectSerializer,
        Event: EventSerializer,
        Saga: SagaSerializer,
    }
