from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("upload/",views.upload,name="upload"),
    path('register/',views.register_view, name='register'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path("logout", views.logout_view, name="logout"),
    # api routes
    path("layout/<int:user_id>",views.layout, name="layout"),
    path('delete_file/<int:file_id>/', views.DeleteFileView, name='delete_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)