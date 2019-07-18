from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth.views import (
    login,
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)

urlpatterns = [
    path('',login,{'template_name': 'webapp/login.html'}),

    url(r'^login/$',login,{'template_name': 'webapp/login.html'}),
    url(r'^logout/$',logout,{'template_name': 'webapp/logout.html'}),
    url(r'^auth/', include('social_django.urls', namespace='social')), 
    url(r'^signup/$', views.signup, name = 'signup'),
    url(r'^profile/$',views.view_profile, name='view_profile'), 
    url(r'^profile/edit/$',views.edit_profile, name='edit_profile'),  
    url(r'^change-password/$',views.change_password, name='change_password'), 
    url(r'^reset-password/$', password_reset, name = 'reset_password'),
    url(r'^reset-password/done/$', password_reset_done, name = 'password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name = 'password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete, name = 'password_reset_complete'),
    url(r'^past/$',views.past, name='past'), 
    path('view-post/<int:pk>/', views.view_post, name='view_post'),  
    path('edit-post/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:pk>/',views.delete_post, name='delete_post'),
    path('home/',views.home,name='home'),
    path('add/', views.add, name = 'add'), 
    path('success/', views.success, name = 'success'), 
    path('post_to_fb/',views.post_to_fb, name = 'post_to_fb'),
    path('share/',views.share, name = 'share'),    
]
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 

