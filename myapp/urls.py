from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserView, CustomTokenObtainPairView, PasswordEntriesViewSet, PasswordEntryListView, GeneratePasswordView

router = DefaultRouter()
router.register(r'password-entries', PasswordEntriesViewSet,basename='password-entry')

urlpatterns =[
    path('', include(router.urls)),
    path("sign-in/", UserView.as_view(), name="create user"),
    path("token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("reveal-password/", PasswordEntryListView.as_view(), name="reveal-password"),
    path("generate-password/", GeneratePasswordView.as_view(), name="generate-password"),
]