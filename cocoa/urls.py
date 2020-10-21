"""cocoa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf.urls import url,include
from django.contrib import admin
from . import view

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^',include('play_page.urls')),
    #url(r'^27f289890009776669c5/',include('interface.urls')),

]

handler400 = view.bad_request
handler403 = view.page_permission_denied
handler404 = view.page_not_found
handler500 = view.page_inter_error