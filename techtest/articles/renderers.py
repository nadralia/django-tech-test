import json

from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if 'errors' in data or 'detail' in data or 'error' in data:
            return super().render(data)
        return json.dumps({'article': data})


class ArticlesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if 'errors' in data or 'detail' in data or 'error' in data:
            return super().render(data)
        return json.dumps({'articles': data})