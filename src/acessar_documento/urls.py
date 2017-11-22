from django.conf.urls import url
from . import views

app_name = 'acessar_documento'
urlpatterns = [
    url(r'^upload_file', views.upload_file, name='upload_file'),
    url(r'^documentsAll', views.documentsAll, name='documentsAll'),
    url(r'^viewpdf/(?P<pk>[^/]+)/', views.viewpdf, name='viewpdf'),
    url(r'^legislation', views.legislation, name='legislation'),
    url(r'^upload_legislation', views.upload_legislation, name='upload_legislation'),

]
