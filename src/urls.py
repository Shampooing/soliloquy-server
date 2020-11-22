from django.contrib import admin

from django.urls import include, path
from rest_framework import routers
from soliloquy import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'entries', views.EntryViewSet)
router.register(r'references', views.ReferenceViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'notebooks', views.NotebookViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'sagas', views.SagaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('', include(router.urls)),
]

