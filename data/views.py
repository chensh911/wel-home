from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from data.models import Data, Home
from data.read import main_demo, publish_data
from device.models import Device
from user.models import ManufacturerInfo, UserInfo
from user.views import warning


class BasicChartsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'basic_charts.html', {'warn': warning(request), })


class MyHomeView(LoginRequiredMixin, View):
    def get(self, request):
        #main_demo()       #hereeeeeeeeee
        home = Home.objects.get(id=1)
        return render(request, 'home.html', {'warn': warning(request), 'home': home, })

    def post(self, request):
        print("====================")
        type = request.POST.get('type')
        data = request.POST.get('data')
        home = Home.objects.get(id=1)
        if type == 'light':
            if home.lightness == data:
                return redirect(reverse('data:home'))
        publish_data(type, data)
        return redirect(reverse('data:home'))


class DistributionChartsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'data_distribution.html', {'warn': warning(request), })

    def post(self, request):
        type = request.POST.get('type')
        id = request.POST.get('id')
        if id:
            try:
                device = Device.objects.get(id=id)
                data = Data.objects.filter(device=device, type=type)
            except Exception as e:
                data = Data.objects.filter(type=type)
        else:
            data = Data.objects.filter(type=type)
        if type == 'humidity':
            one = data.filter(data__lte=40).count()
            two = data.filter(data__lte=50, data__gt=40).count()
            three = data.filter(data__lte=60, data__gt=50).count()
            four = data.filter(data__gte=60).count()
        else:
            one = data.filter(data__lte=15).count()
            two = data.filter(data__lte=20, data__gt=15).count()
            three = data.filter(data__lte=25, data__gt=20).count()
            four = data.filter(data__gte=30).count()

        context = {
            "type": type,
            'range': range,
            'one': one,
            'two': two,
            'three': three,
            'four': four,
            'warn': warning(request),
        }
        return render(request, 'data_distribution.html', context)


class ContractChartsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'data_contract.html', {'warn': warning(request), })

    def post(self, request):
        id1 = request.POST.get('id1')
        if id1 != '':
            device1 = Device.objects.get(id=id1)
            data1 = Data.objects.filter(device=device1)
        else:
            data1 = Data.objects.all()
        id2 = request.POST.get('id2')
        if id2 != '':
            device2 = Device.objects.get(id=id2)
            data2 = Data.objects.filter(device=device2)
        else:
            data2 = Data.objects.all()
        data1h = data1.filter(type='humidity')
        one1h = data1h.filter(data__lte=40).count()
        two1h = data1h.filter(data__lte=50, data__gt=40).count()
        three1h = data1h.filter(data__lte=60, data__gt=50).count()
        four1h = data1h.filter(data__gte=60).count()

        data2h = data2.filter(type='humidity')
        one2h = data2h.filter(data__lte=40).count()
        two2h = data2h.filter(data__lte=50, data__gt=40).count()
        three2h = data2h.filter(data__lte=60, data__gt=50).count()
        four2h = data2h.filter(data__gte=60).count()

        data1t = data1.filter(type='temperature')
        one1t = data1t.filter(data__lte=15).count()
        two1t = data1t.filter(data__lte=20, data__gt=15).count()
        three1t = data1t.filter(data__lte=25, data__gt=20).count()
        four1t = data1t.filter(data__gte=30).count()

        data2t = data2.filter(type='temperature')
        one2t = data2t.filter(data__lte=15).count()
        two2t = data2t.filter(data__lte=20, data__gt=15).count()
        three2t = data2t.filter(data__lte=25, data__gt=20).count()
        four2t = data2t.filter(data__gte=30).count()

        context = {
            "type": type,
            'one1t': one1t,
            'two1t': two1t,
            'three1t': three1t,
            'four1t': four1t,
            'one2t': one2t,
            'two2t': two2t,
            'three2t': three2t,
            'four2t': four2t,
            'one1h': one1h,
            'two1h': two1h,
            'three1h': three1h,
            'four1h': four1h,
            'one2h': one2h,
            'two2h': two2h,
            'three2h': three2h,
            'four2h': four2h,
            'id1': id1,
            'id2': id2,
            'warn': warning(request),
        }
        return render(request, 'data_contract.html', context)


def helper_data(request, data, page):
    type = ['temperature', 'humidity', 'door', 'window', 'distance', 'lightness', 'foggy', 'rain', 'earthquake']
    paginator = Paginator(data, 12)
    try:
        page = int(page)
    except Exception as e:
        page = 1

    if page > paginator.num_pages:
        page = 1
    skus_page = paginator.page(page)
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)

    context = {
        "skus_page": skus_page,
        "pages": pages,
        "count": paginator.count,
        "type": type,
        'warn': warning(request),
    }
    return render(request, 'data.html', context)


class DataView(LoginRequiredMixin, View):
    def get(self, request, page):
        try:
            user = request.user
            data = Data.objects.all()
            if user.is_superuser == 0 and user.is_staff == 1:
                device = Device.objects.filter(manufacture=user)
                data = data.filter(device__in=device)
            elif user.is_superuser == 0 and user.is_staff == 0:
                family = UserInfo.objects.get(user=user).family
                device = Device.objects.filter(family=family)
                data = data.filter(device__in=device)
        except Device.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_data(request, data, page)

    def post(self, request, page):
        try:
            user = request.user
            data = Data.objects.all()
            if user.is_superuser == 0 and user.is_staff == 1:
                device = Device.objects.get(manufacture=user)
                data = data.filter(device__in=device)
            elif user.is_superuser == 0 and user.is_staff == 0:
                family = UserInfo.objects.get(user=user).family
                device = Device.objects.filter(family=family)
                data = data.filter(device__in=device)
            type = request.POST.get('type')
            low = request.POST.get('low')
            high = request.POST.get('high')
            if type != '-----All-----':
                data = data.filter(type=type)
            if low:
                data = data.filter(data__gte=low)
            if high:
                data = data.filter(data__lte=high)
        except Device.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_data(request, data, page)


class AddData(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = request.POST.get('data')
            type = request.POST.get('type')
            device_id = request.POST.get('device_id')
            device = Device.objects.get(id=device_id)
            new_item = Data.objects.create(data=data, type=type, device=device)
        except Exception as e:
            return redirect('data/1')
        return redirect('data/1')


class ModifyData(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            data = request.POST.get('data')
            type = request.POST.get('type')
            device_id = request.POST.get('device_id')
            device = Device.objects.get(id=device_id)

            item = Data.objects.get(id=id)
            item.data = data
            item.type = type
            item.device = device
            item.save()
        except Exception as e:
            return redirect('data/1')
        return redirect('data/1')


class DeleteData(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            item = Data.objects.get(id=id)
            item.delete()
        except Exception as e:
            return redirect('data/1')
        return redirect('data/1')
