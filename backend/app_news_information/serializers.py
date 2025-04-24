from rest_framework import serializers

from.models import NewsTopic, NewsArticle


class NewsTopicSerializer(serializers.ModelSerializer):
    article_list = serializers.SerializerMethodField()
    class Meta:
        model = NewsTopic
        fields = ['id', 'name', 'description', 'article_list']

    def get_article_list(self, obj):
        articles = obj.news_topic_article.all()
        if not articles:
            return []
        
        results = []
        for article in articles:
            results.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'image': article.image.url if article.image else None,
                'author': article.author
            })
        return results
    
class NewsTopicOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTopic
        fields = ['id', 'name']

class NewsArticleSerializer(serializers.ModelSerializer):
    news_topic = serializers.SerializerMethodField()
    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'content', 'image', 'author', 'news_topic']

    def get_news_topic(self, obj):
        if not obj.news_topic:
            return None
        return {
            'id': obj.news_topic.id,
            'name': obj.news_topic.name,
            'description': obj.news_topic.description
        }
    
class NewsArticleOverviewSerializer(serializers.ModelSerializer):
    news_topic = serializers.SerializerMethodField()
    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'image', 'news_topic']

    def get_news_topic(self, obj):
        if not obj.news_topic:
            return None
        return {
            'id': obj.news_topic.id,
            'name': obj.news_topic.name,
            'description': obj.news_topic.description
        }