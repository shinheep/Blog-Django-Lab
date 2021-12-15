from django.urls import path
from .views.users import SignUp, SignIn, SignOut, ChangePassword
from .views.blogs import BlogsView, BlogView
from .views.comments import CommentsView, CommentView

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blogs/<int:pk>', BlogView.as_view(), name='blog'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('comments/<int:pk>', CommentView.as_view(), name='comment'),
]