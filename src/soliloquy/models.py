import datetime

from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ValidationError
# from django.contrib.postgres.fields import JSONField
from django.db import models
from polymorphic.models import PolymorphicModel


# TODO [audit] remove the on_delete=models.CASCADE and provide a nice mechanism to mark objects as inactive


class User(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.django_user)


# ---- Collaboration

# class Workspace(models.Model):
#     owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="workspaces_owned")
#     contributors = models.ManyToManyField(
#         to="User",
#         blank=True,
#         through="WorkspaceContributors",
#         related_name="workspaces_contributed"
#     )
#
#
# class WorkspaceContributors(models.Model):
#     workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)
#     contributor = models.ForeignKey("User", on_delete=models.CASCADE)


# ---- Decentralization
class Client(models.Model):
    """
    A source of entries, owned by a user. The typical use case is of a user's device that has been registered as a
    client of the application.
    """
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    class Meta:
        constraints = [
            # Proxy for a composite primary key
            models.UniqueConstraint(fields=("owner", "name"), name="client_composite_key_constraint")
        ]

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    """
    A tag is just a word we may use to annotate Entries.
    """
    name = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return str(self.name)


class Entry(PolymorphicModel):
    """
    The basic object we'll keep track of in the journal.
    """

    # ---- We resort to using a string as a primary key because Django does not support composite keys.
    id = models.AutoField(primary_key=True)  # Deprecated, to be retired at some point so that we can create the id
    # of an entry on the client. To be replaced as a primary key by the 'key' field.

    key = models.CharField(max_length=32, null=True, blank=True)  # We allow this to be empty while we retire 'id'.
    # key = models.CharField(max_length=32)  # String of <creation date>,<some counter>,<client id>

    creation_date = models.DateTimeField()
    client = models.ForeignKey("Client", on_delete=models.CASCADE)  # Really clients should never be deleted

    @property
    def author(self):  # we expose the author of the entry for convenience
        return self.client.owner

    active = models.BooleanField(default=True)  # This is how we implement a soft delete

    name = models.CharField(max_length=120, blank=True)  # Not a primary key as we want to allow renaming over time

    content = models.TextField(blank=True)

    tags = models.ManyToManyField("Tag", related_name="entries", blank=True)

    # ---- Extended attributes
    # extra = JSONField(blank=True, null=True)  # TODO: migrate to Postgres and enable this field at some point

    class Meta:
        ordering = ["-creation_date"]  # Show most recent entries first
        verbose_name_plural = "entries"
        constraints = [
            # Proxy for a composite primary key
            models.UniqueConstraint(fields=("id", "client"), name="entry_composite_key_constraint")
        ]

    def __str__(self):
        return str(self.name)


class Reference(models.Model):
    """
    We supplement the many-to-many field in Entry to keep track of the reference_id; this is because an entry may
    reference an arbitrary number of other entries (potentially multiple references to the same entry) - just not
    itself.
    """
    source = models.ForeignKey("Entry", on_delete=models.CASCADE, related_name="references")
    reference_id = models.IntegerField()
    target = models.ForeignKey("Entry", on_delete=models.CASCADE, related_name="referenced_by")

    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            # Proxy for a composite primary key
            models.UniqueConstraint(fields=("source", "reference_id"), name="reference_composite_key_constraint")
        ]

    def clean(self):
        if self.source.id == self.target.id:
            raise ValidationError(
                "Self-references are not allowed. (Attempted by Entry '{}' with id: {})."
                .format(self.source, self.source.id)
            )

    def __str__(self):
        return "{source} --> {target} ({id})".format(
            source=str(self.source),
            target=str(self.target),
            id=self.reference_id
        )


# ---- Specialized entries:

class Note(Entry):
    parent_notebook = models.ForeignKey(
        "NoteBook",
        related_name="notes",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class Notebook(Entry):
    """
    A collection of Notes.
    """
    def get_as_dict(self):
        return dict(
            super().get_as_dict(),
            notes=[note.id for note in self.notes.all()],
        )


class Task(Entry):
    """
    Due date, estimation of the required effort, priority. May be linked to a Project.
    """
    due_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    recurrence = models.IntegerField(null=True, blank=True)  # TODO placeholder for now
    priority = models.IntegerField(null=True, blank=True)
    effort_estimate = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)  # in hours

    done = models.BooleanField(default=False)  # Whether the task has been done or not.

    # Optional: how many minutes should be spent every time the user works on this (à la Pomodoro).
    # If set, the user would get an alert once they worked on the task for longer than the specified duration.
    # To be inherited from the parent project if any.
    unit_of_work = models.IntegerField(null=True, blank=True)

    parent_project = models.ForeignKey(
        "Project",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True
    )
    assignee = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,  # Allow Null value only if the assigned user is deleted,
                    # in which case the assignee becomes the entry's author
    )

    def clean(self):
        if self.expiration_date and self.due_date and self.due_date > self.expiration_date:
            raise ValidationError(
                "Due date {} on task {} cannot be after after expiration date {}."
                .format(self.due_date, self, self.expiration_date)
            )
        if self.parent_project and self.due_date:
            dd = self.due_date
            p = self.parent_project
            pdd = p.due_date
            if pdd and dd > pdd:
                raise ValidationError(
                    "Due date {} on task {} cannot be set after due date {} of project {}".format(dd, self, pdd, p)
                )


class Habit(Entry):
    """
    Something to track over time. Maybe some constraint on a set of metrics (weekly distance run greater than 5km,
    arterial pressure within some range, etc.)
    """
    pass


class Metric(Entry):
    """How much was something, or did something happen or not"""
    # we need a JSON field here so that custom metrics can be captured (eg arterial pressure, weight, distance run...)
    pass


class Project(Entry):
    """
    A project is essentially a collection of Tasks.
    """
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)

    # Optional: default value for the number of minutes the user should spend every time they work on a task in this
    # project (à la Pomodoro).
    # If set, the user would get an alert once they worked on the task for longer than the specified duration.
    unit_of_work = models.IntegerField(null=True, blank=True)


class Saga(Entry):
    """
    A Saga is a collection of Events. We call this a Saga rather than a Calendar to encourage the
    grouping of Events in meaningful clusters.
    """
    pass


class Event(Entry):
    # TODO: timezones
    start_date = models.DateField()
    end_date = models.DateField()
    all_day = models.BooleanField(default=False)
    start_time = models.TimeField(default=datetime.time(0, 0))
    end_time = models.TimeField(default=datetime.time(0, 0))
    parent_saga = models.ForeignKey("Saga", on_delete=models.CASCADE, related_name="events", null=True, blank=True)

