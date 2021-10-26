"""LITReview_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls.static import static
from reviews import views

import reviews.views
import authentication.views

urlpatterns = [
    url(r'^$', reviews.views.home, name='home'),
    url(r'^login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^home/', reviews.views.home, name='home'),
    url(r'^signup/$', authentication.views.signup_page, name='signup'),
    url(r'^view_follows$', reviews.views.view_follows, name='view_follows'),
    url(r'^reviews/ticket_create$', reviews.views.ticket_upload, name='ticket_create'),
    url(r'^reviews/ticket_and_review_create$', reviews.views.review_and_ticket_upload, name='review_and_ticket_create'),
    url(r'^reviews/my_posts$', reviews.views.my_posts, name='my_posts'),
    path('delete_follows/<int:follower_id>', reviews.views.delete_follows, name='delete_follows'),
    path('add_follow/', reviews.views.add_follow, name='add_follow'),
    path('reviews/<int:ticket_id>', reviews.views.view_ticket, name='view_ticket'),
    path('reviews/<int:ticket_id>/edit', reviews.views.edit_ticket, name='edit_ticket'),
    path('reviews/<int:ticket_id>/review_create', reviews.views.review_upload, name='review_create'),
    path('reviews/<int:ticket_id>/<int:review_id>', reviews.views.view_review, name='view_review'),
    path('reviews/<int:ticket_id>/<int:review_id>/edit', reviews.views.edit_review, name='edit_review'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)