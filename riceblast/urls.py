"""riceblast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views 
from riceapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', views.current_user),
    path('api/labs/', views.riceblastlabs),
    path('api/collection_sites/',views.fungal_collection_sites),
    path('api/isolates/',views.isolates),
    path('api/rice_genotypes/',views.rice_genotypes),
    path('api/rice_genes/', views.rice_genes),
    path('api/rgs/', views.rgs),
    path('api/fgs/',views.fgs),
    path('api/pathotyping_results/',views.pathotyping_results),
    path('api/vcg_groups/',views.vcg_groups),
    path('api/fungal_small/',views.fungal_small),
    path('api/rice_small/',views.rice_small),
    path('api/vcg_test_results/',views.vcg_test_results),
    path('api/protocol/',views.protocol),
    path('api/rice_gbs/',views.rice_gbs),
    path('api/fungal_gbs/',views.fungal_gbs),
    path('api/register/',views.UserList.as_view()),
    path('api/people/',views.all_people),
    path('api/user_activation/',views.activate_user),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
