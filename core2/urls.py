# From settings get basdir
import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.static import serve  # add static views
from rest_framework.authtoken.views import obtain_auth_token  # Authentication (not used here)
from rest_framework_jwt.views import obtain_jwt_token   # JWT Authentication
from rest_framework.documentation import include_docs_urls  # docs
from rest_framework.permissions import AllowAny

from data_api.urls import router as data_api_router
from transfer_api.urls import router as transfer_api_router
from auth_api.urls import router as auth_api_router
# Import Internal routers

root_dir = os.path.abspath(settings.BASE_DIR)
upload_dir = os.path.join(root_dir, 'media', 'upload')
'''
@Author: HpMa
@Date: 2018-08-08

'''
"""core2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

urlpatterns = [
    path(r'admin/', admin.site.urls),
]

# **********************************************************
# ******************** Back end routers ********************
# **********************************************************

# =============================================
#  data api path
# =============================================
urlpatterns += [
    path(r'data_api/token/', obtain_jwt_token, name='data_api_token'),
    path(r'data_api/', include(data_api_router.urls)),
]

# =============================================
#  transfer api path
# =============================================

urlpatterns += [
    path(r'transfer_api/token/', obtain_jwt_token, name='transfer_api_token'),
    path(r'transfer_api/', include(transfer_api_router.urls)),
]

# =============================================
#  auth api path
# =============================================
urlpatterns += [
    path(r'auth_api/token/', obtain_jwt_token, name='auth_api_token'),
    path(r'auth_api/', include(auth_api_router.urls)),
]
# =============================================
#  static serve
# =============================================
urlpatterns += [
    url(r'media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# =============================================
#  API Docs
# =============================================
urlpatterns += [
    path(r'docs/',
         include_docs_urls(title='API docs', permission_classes=[AllowAny])),
]
