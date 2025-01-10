from django.db import models
from django.contrib.auth.models import User

class Postagem(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255,blank=False)
    postagem = models.TextField(verbose_name='qual a postagem',blank=False)
    imagem = models.ImageField(upload_to='imagem/',blank=True,null=True)
    criado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'
        ordering = ['-editado']

    def __str__(self):
        return self.titulo[:20]
    
class Comentario(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem,on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255,blank=False)
    comentario = models.CharField(max_length=255,blank=False)
    criado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['editado']

    def __str__(self):
        return self.comentario[:20]