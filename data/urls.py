from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from data.views import BasicChartsView, DataView, AddData, ModifyData, DeleteData, DistributionChartsView, \
    ContractChartsView, MyHomeView

urlpatterns = [
    url(r'^basic$', BasicChartsView.as_view(), name='basic_charts'),
    url(r'^distribution$', DistributionChartsView.as_view(), name='distribution'),
    url(r'^contract$', ContractChartsView.as_view(), name='contract'),

    url(r'^data/(?P<page>\d+)$', DataView.as_view(), name='data'),
    url(r'^addData$', AddData.as_view(), name='addData'),
    url(r'^modifyData$', ModifyData.as_view(), name='modifyData'),
    url(r'^deleteData$', DeleteData.as_view(), name='deleteData'),

    url(r'^home$', MyHomeView.as_view(), name='home'),

]
