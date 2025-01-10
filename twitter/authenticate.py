from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class CookiesAuthentication(JWTAuthentication):
    def authenticate(self,request):
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return None
        
        validated_token = self.get_validated_token(access_token)

        try:
            user = self.get_user(validated_token)
        except:
            return None
        
        return (user, validated_token)

class AutorOuAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user.is_staff or request.user.id == obj.usuario_id:
            return True
        if request.method == 'GET':
            return True
