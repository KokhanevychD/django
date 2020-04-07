from django.urls import path
from posts.views import article_edit_view
from cabinet.views import user_page, delete_view


app_name = 'cabinet'
urlpatterns = [
    path('', user_page, name='cabinet'),
    path('edit/<int:id>', article_edit_view, name='edit'),
    path('<int:id>/', delete_view, name='del_obj'),
]
