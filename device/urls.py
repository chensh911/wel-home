from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from device.views import CategoryView, AddCategory, ModifyCategory, DeleteCategory, DeviceView, AddDevice, ModifyDevice, \
    DeleteDevice

urlpatterns = [
    url(r'^category/(?P<page>\d+)$', CategoryView.as_view(), name='category'),
    url(r'^addCategory$', AddCategory.as_view(), name='addCategory'),
    url(r'^modifyCategory$', ModifyCategory.as_view(), name='modifyCategory'),
    url(r'^deleteCategory$', DeleteCategory.as_view(), name='deleteCategory'),
    url(r'^device/(?P<page>\d+)$', DeviceView.as_view(), name='device'),
    url(r'^addDevice$', AddDevice.as_view(), name='addDevice'),
    url(r'^modifyDevice$', ModifyDevice.as_view(), name='modifyDevice'),
    url(r'^deleteDevice$', DeleteDevice.as_view(), name='deleteDevice'),
]
