from django.urls import path
from . import views
 
urlpatterns = [
    # Admin dashboard
    path('dashboard/',        views.dashboard,     name='dashboard'),
 
    # Public
    path('',                  views.home,          name='home'),
    path('item/<int:pk>/',    views.item_detail,   name='item_detail'),
 
    # Admin only
    path('manage/',           views.manage_items,  name='manage_items'),
    path('post/',             views.post_item,     name='post_item'),
    path('edit/<int:pk>/',    views.edit_item,     name='edit_item'),
    path('delete/<int:pk>/',  views.delete_item,   name='delete_item'),
    path('resolve/<int:pk>/', views.mark_resolved, name='mark_resolved'),
 
    # Auth
    path('login/',            views.login_view,    name='login'),
    path('logout/',           views.logout_view,   name='logout'),
]
 