from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from graphene_django.views import GraphQLView

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # TODO add urls from other apps
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
