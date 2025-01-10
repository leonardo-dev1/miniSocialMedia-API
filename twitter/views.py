from django.contrib.auth.models import User
from twitter.models import Postagem,Comentario
from twitter.serializers import UserSerializer,PostagemSerializer,ComentarioSerializer
from twitter.authenticate import AutorOuAdmin
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import JSONParser 

#-------------- Registro/Visualização Usuários

class UserRegister(generics.CreateAPIView):
    """
    Descrição da View:
    - Endpoint para POST de novos usuarios.

    Métodos HTTP Permitidos:
    - POST /register/ -> Cria um novo usuário.

    Classe de Serializador:
    - UserSerializer -> Usado para serializar os dados, tendo métodos de:
        validação dos dados do usuário.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

class UserViewSet(viewsets.ModelViewSet):
    """
    Descrição da View:
    - Endpoint para GET de todos os usuarios.

    Métodos HTTP Permitidos:
    - GET /usuarios/ -> Lista todos os usuários.

    Classe de Serializador:
    - UserSerializer -> Usado para serializar os dados.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ('get',)
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['username','first_name','email']
    ordering_fields =['username','first_name']

#-------------- ViewSet de Postagens/Comentarios

class PostagemViewSet(viewsets.ModelViewSet):
    """
    Descrição da View:
    - Endpoint para GET e POST de novas publicações.

    Métodos HTTP Permitidos:
    - GET /postagens/ -> Listar todas as postagens de todos usuarios.
    - POST /postagens/ -> Cria uma nova publicação para um usuário.

    Classe de Serializador:
    - PostagemSerializer.
    """
    queryset = Postagem.objects.all().order_by('-editado')
    serializer_class = PostagemSerializer
    http_method_names = ('get','post',)
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['postagem','usuario','titulo']
    ordering_fields =['postagem','editado']

    def perform_create(self,serializer):
        serializer.save(usuario=self.request.user)

class ComentarioViewSet(viewsets.ModelViewSet):
    """
    Descrição da View:
    - Endpoint para GET e POST de novos comentarios.

    Métodos HTTP Permitidos:
    - GET /comentarios/ -> Listar todos os comentarios de todos usuarios.
    - POST /comentarios/ -> Cria um novo novo comentario em uma publicacao.

    Classe de Serializador:
    - ComentarioSerializer.
    """
    queryset = Comentario.objects.all().order_by('editado')
    serializer_class = ComentarioSerializer
    http_method_names = ('get','post',)
    filter_backends = [SearchFilter]
    search_fields = ['comentario','titulo']
    ordering_fields =['comentario','editado']

    def perform_create(self,serializer):
        serializer.save(usuario=self.request.user)

#-------------- Método para Selecionar, Editar ou Excluir Feed ou Postagem única de um Usuário
                        
class FeedUser(generics.ListAPIView):
    """
    Descrição da View:
    - Endpoint para GET do FEED de um usuario.

    Métodos HTTP Permitidos:
    - GET /usuario/<int:pk>/feed/ -> Lista todas as publicações de um único usuário.

    Classe de Serializador:
    - UserSerializer.
    """
    def get_queryset(self):
        queryset = Postagem.objects.filter(usuario_id=self.kwargs['pk']).order_by('-editado')
        return queryset
    serializer_class = PostagemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['postagem','titulo']
    ordering_fields =['postagem','editado']

class PostagemUser(generics.RetrieveUpdateDestroyAPIView):
    """
    Descrição da View:
    - Endpoint para GET, PUT, PATCH, DELETE de uma publicação de um usuario.

    Métodos HTTP Permitidos:
    - GET /postagem/<int:pk>/editar/ -> Seleciona uma publicação de um usuário.
    - PUT /postagem/<int:pk>/editar/ -> Permite editar uma publicação de atualizar sua hora de edição.
    - PATCH /postagem/<int:pk>/editar/ -> Permite editar uma publicação parcialmente.
    - DELETE /postagem/<int:pk>/editar/ -> Permite excluir a postagem, permissões apenas para o usuario da postagem e superadmin
    
    Classe de Serializador:
    - PostagemSerializer.
    """
    def get_queryset(self):
        queryset = Postagem.objects.filter(id=self.kwargs['pk'])
        return queryset
    serializer_class = PostagemSerializer
    permission_classes = [AutorOuAdmin]

#-------------- Método para Selecionar, Editar ou Excluir Feed ou Postagem única de um Usuário

class ComentariosPostagem(generics.ListAPIView):
    """
    Descrição da View:
    - Endpoint para GET de um comentario de uma postagem.

    Métodos HTTP Permitidos:
    - GET /postagem/<int:pk>/comentarios/ -> Lista todos os comentarios de uma publicação.
    
    Classe de Serializador:
    - ComentarioSerializer.
    """
    def get_queryset(self):
        queryset = Comentario.objects.filter(postagem_id=self.kwargs['pk']).order_by('editado')
        return queryset
    serializer_class = ComentarioSerializer
    filter_backends = [SearchFilter]
    search_fields = ['usuario','comentario','titulo']
    ordering_fields =['usuario','editado']

class ComentarioPostagem(generics.RetrieveUpdateDestroyAPIView):
    """
    Descrição da View:
    - Endpoint para GET, PUT, PATCH, DELETE de uma publicação de um usuario.

    Métodos HTTP Permitidos:
    - GET /postagem/<int:pk>/comentario/ -> Seleciona um comentario de uma publicação.
    - PUT /postagem/<int:pk>/comentario/ -> Permite editar um comentario e atualizar sua hora de edição.
    - PATCH /postagem/<int:pk>/comentario/ -> Permite editar um comentario parcialmente.
    - DELETE /postagem/<int:pk>/comentario/ -> Permite excluir um comentario, permissões apenas para o usuario da postagem e superadmin
    
    Classe de Serializador:
    - ComentarioSerializer.
    """
    def get_queryset(self):
        queryset = Comentario.objects.filter(id=self.kwargs['pk'])
        return queryset
    serializer_class = ComentarioSerializer
    permission_classes = [AutorOuAdmin]

#-------------- Authentication Token JWT COOKIE

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Descrição da View:
    - Endpoints permitidos POST, método que permite salvar o token e refresh do usuario nos cookies da api.

    Métodos HTTP Permitidos:
    - POST /login/ -> permite fazer o login na API.
    """
    def post(self,request,*args,**kwargs):
        try:    
            response = super().post(request,*args,**kwargs)
            token = response.data

            access_token = token['access']
            refresh_token = token['refresh']

            res = Response()
            res.data={"sucess":True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )
            return res
        except:
            return Response({'success':False})

class CustomTokenRefreshView(TokenRefreshView):
    """
    Descrição da View:
    - Endpoints permitidos POST, método que permite salvar o token e refresh do usuario nos cookies da api.

    Métodos HTTP Permitidos:
    - POST /token/refresh/ -> Permite obter um novo token de acesso, apenas o Raw Data como método de POST.
    """
    parser_classes = [JSONParser,]
    def post(self,request,*args,**kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token

            response = super().post(request,*args,**kwargs)
            tokens = response.data
            access_token = tokens['access']

            res = Response()
            res.data = {"success":True}
            res.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/',
                )
            return res
        except:
            return Response({"success":False})