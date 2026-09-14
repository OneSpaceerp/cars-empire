from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.BlogPostListView.as_view(), name='blog-post-list'),
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
] 