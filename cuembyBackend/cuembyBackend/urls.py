"""cuembyBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from graphql_jwt.decorators import login_required
from graphql_jwt.middleware import JSONWebTokenMiddleware

from cuembyBackend import schema

class AuthMiddleware(object):
    @login_required
    def resolve(self, next, root, info, **args):
        from django.conf import settings
        from django.shortcuts import redirect
        if not info.context.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, info.context.path))
        return next(root, info, **args)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql-login/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema.schemaLogin))),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema.schema))), # middleware=[AuthMiddleware(), JSONWebTokenMiddleware()]

]
