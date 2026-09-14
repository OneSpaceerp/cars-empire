from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'author',
            'featured_image', 'created_at', 'updated_at',
            'published_at', 'is_published', 'is_featured',
            'meta_description', 'meta_keywords'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at'] 