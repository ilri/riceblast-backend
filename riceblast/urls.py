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
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views 
from riceapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', views.current_user),
    re_path(r'api/labs/(\d*)', views.RiceBlastLabList.as_view()),
    re_path(r'api/collection_sites/(\d*)',views.CollectionSiteList.as_view()),
    re_path(r'api/isolates/(\d*)',views.IsolateList.as_view()),
    re_path(r'api/rice_genotypes/(\d*)',views.RiceGenotypeList.as_view()),
    re_path(r'api/rice_genes/(\d*)', views.RiceGenesList.as_view()),
    re_path(r'api/rgs/(\d*)', views.RGSResultsList.as_view()),
    re_path(r'api/fgs/(\d*)',views.FGSResultsList.as_view()),
    re_path(r'api/pathotyping_results/(\d*)',views.PathotypingResultsList.as_view() ),
    re_path(r'api/vcg_groups/(\d*)',views.vcg_groups),
    re_path(r'api/fungal_small/(\d*)',views.fungal_small),
    re_path(r'api/rice_small/(\d*)',views.rice_small),
    re_path(r'api/vcg_test_results/(\d*)',views.vcg_test_results),
    re_path(r'api/protocol/(\d*)',views.protocol),
    re_path(r'api/rice_gbs/(\d*)',views.rice_gbs),
    re_path(r'api/fungal_gbs/(\d*)',views.fungal_gbs),
    re_path(r'api/register/',views.UserList.as_view()),
    re_path(r'api/user_delete/',views.UserList.as_view()),
    re_path(r'api/people/',views.all_people),
    re_path(r'api/user_activation/',views.activate_user),
    # path('api/user_delete/',views.delete_user),
    # path('/api/')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
