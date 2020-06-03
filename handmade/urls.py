"""handmade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from category.views import CategoryViewSet
from comment.views import CommentViewSet
from favourites.views import FavouriteViewSet
from item.views import ItemViewSet
from offer.views import OfferViewSet
from post.views import PostViewSet
from tag.views import TagViewSet
from upload_image.views import ImageViewSet, PostImageViewSet
from user.views import UserViewSet
from chat.views import MessageViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'favourites', FavouriteViewSet)
router.register(r'upload_images', ImageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'images', ImageViewSet)
router.register(r'postImages', PostImageViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', views.obtain_auth_token, name='login'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)