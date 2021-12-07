from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from login import views


urlpatterns = [
    path('login',
         jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),

    path('profile/', views.Profile.as_view()),
    path('',views.Registered_User.as_view()),
    path('change-password',views.ChangePasswordView.as_view()),

    # path('login',views.Login_User),
    # path('user_details/<username>', views.User_Details)


    ]