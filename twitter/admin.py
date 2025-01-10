from django.contrib import admin
from twitter.models import Postagem,Comentario

@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','titulo','postagem','imagem','criado','editado',)
    list_per_page = 5
    search_fields = ('id','usuario','postagem','editado',)
    ordering = ('usuario',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','postagem','titulo','comentario','criado','editado',)
    list_per_page = 5
    search_fields = ('id','usuario','postagem','comentario','editado',)
    ordering = ('usuario',)