from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from twitter.views import UserViewSet,PostagemViewSet,ComentarioViewSet,FeedUser,PostagemUser,ComentariosPostagem,ComentarioPostagem

router = routers.DefaultRouter()
router.register('usuarios',UserViewSet,'Usuários')
router.register('postagens',PostagemViewSet,'Postagens')
router.register('comentarios',ComentarioViewSet,basename='Comentarios')

urlpatterns = [
    path('usuario/<int:pk>/feed/',FeedUser.as_view(),name='feed_usuario'),
    path('postagem/<int:pk>/editar/',PostagemUser.as_view(),name='editar_postagem_usuario'),
    path('postagem/<int:pk>/comentarios/',ComentariosPostagem.as_view(),name='comentarios_postagem'),
    path('comentario/<int:pk>/editar/',ComentarioPostagem.as_view(),name='editar_comentario'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
