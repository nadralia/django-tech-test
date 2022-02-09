import uuid
from rest_framework import generics, permissions, status, response
from techtest.profiles.models import Profile
from techtest.articles.models import Article
from rest_framework.response import Response
from django.template.defaultfilters import slugify
from .serializers import (ArticleSerializer, ArticleRegionSerializer)

from .renderers import (ArticleJSONRenderer, ArticlesJSONRenderer)

from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.exceptions import (
    PermissionDenied, ParseError, NotFound, ValidationError)


class ArticlesListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer
    renderer_classes = (ArticlesJSONRenderer,)

    def post(self, request):
        article = request.data.get('article', {})
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(
            author=Profile.objects.get(user=self.request.user)
        )
        article_ob = Article.objects.get(title=article['title'])
        region_data = article['regions']
        for region in region_data:
            regions_serializer_class = ArticleRegionSerializer
            regions_serializer = regions_serializer_class(
                data=region, partial=True)
            regions_serializer.is_valid(raise_exception=True)
            regions_serializer.save(article=article_ob)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def retrieve(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            serializer = self.serializer_class(
                article, context={'request': request})
            return Response(serializer.data)
        except Article.DoesNotExist:
            response = {
                'error': 'Article does not exist'
            }
            return Response(response, status.HTTP_404_NOT_FOUND)

    def update(self, request, article_id):
        data = request.data.get('article', {})
        try:
            article = Article.objects.get(id=article_id)
            if article.author != request.user:
                raise PermissionDenied(
                    {"error": "You do not have permission to"
                        "perform this action."})
            serializer = self.serializer_class(
                article, data=data,
                context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data
            response['message'] = "Article updated successfully."
            return Response(response, status=status.HTTP_201_CREATED)
        except Article.DoesNotExist:
            raise NotFound(
                {'error': 'Article does not exist'})

    def destroy(self, request, article_id):
        print('herere')
        article_instance = get_object_or_404(Article, id=article_id)
        if article_instance.author != request.user:
            raise PermissionDenied
        self.perform_destroy(article_instance)
        return Response(
            {"message": "Article is deleted"},
            status=status.HTTP_200_OK
        )