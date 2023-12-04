
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('recipe/',views.recipes,name="recipes"),
    path('delete-recipe/<id>/',views.delete_recipe,name="delete-recipe"),
    path('update-recipe/<id>/',views.update_recipe,name="update-recipe"),
    path('auth/',views.auth,name="auth"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
]
