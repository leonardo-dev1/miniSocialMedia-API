from django.contrib import admin
from django.urls import path, include
from twitter.urls import router
from twitter.views import UserRegister, CustomTokenObtainPairView, CustomTokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="Documentação da API",
      default_version='v1',
      description="Documentação da Api SocialMedia",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[AllowAny,]
)

urlpatterns = [
    
    path('register/',UserRegister.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('',include(router.urls)),    
    path('',include('twitter.urls')),
    
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
