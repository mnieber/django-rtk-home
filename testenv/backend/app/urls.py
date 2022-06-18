from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from app.utils.serve_static import serve_static

urlpatterns = (
    [
        path(r"admin/", admin.site.urls),
        path(r"graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    ]
    + serve_static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + serve_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
