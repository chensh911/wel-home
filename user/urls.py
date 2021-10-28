from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from user.views import RegisterView, LoginView, LogoutView, IndexView, \
    DashboardView, UserView, ModifyUser, DeleteUser, FamilyView, AddFamily, DeleteFamily, ModifyFamily, ProfileView, \
    ProfileBasicView, ProfileUserView, ProfileManuView, ShopView, CartView, PopularView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^shop$', ShopView.as_view(), name='shop'),
    url(r'^cart$', CartView.as_view(), name='cart'),
    url(r'^popular$', PopularView.as_view(), name='popular'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),

    url(r'^user/user/(?P<page>\d+)$', UserView.as_view(), name='user'),
    url(r'^user/modifyUser$', ModifyUser.as_view(), name='modifyUser'),
    url(r'^user/deleteUser$', DeleteUser.as_view(), name='deleteUser'),

    url(r'^user/family/(?P<page>\d+)$', FamilyView.as_view(), name='family'),
    url(r'^user/addFamily$', AddFamily.as_view(), name='addFamily'),
    url(r'^user/modifyFamily$', ModifyFamily.as_view(), name='modifyFamily'),
    url(r'^user/deleteFamily$', DeleteFamily.as_view(), name='deleteFamily'),

    url(r'^profile$', ProfileView.as_view(), name='profile'),
    url(r'^profileBasic$', ProfileBasicView.as_view(), name='profileBasic'),
    url(r'^profileUser$', ProfileUserView.as_view(), name='profileUser'),
    url(r'^profileManu$', ProfileManuView.as_view(), name='profileManu'),
]
