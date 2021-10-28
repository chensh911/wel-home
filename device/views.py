from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import django.conf
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from device.models import Category, Device
from user.models import User, ManufacturerInfo, UserInfo, Family
from user.views import warning


def helper_category(request, category, page):
    paginator = Paginator(category, 12)
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
        'warn': warning(request),
    }
    return render(request, 'category.html', context)


class CategoryView(LoginRequiredMixin, View):

    def get(self, request, page):
        try:
            category = Category.objects.all()
        except Category.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_category(request, category, page)

    def post(self, request, page):
        try:
            category = Category.objects.all()
            c_id = request.POST.get('c_id')
            if c_id:
                category = category.filter(id=c_id)
            c_name = request.POST.get('c_name')
            if c_name:
                category = category.filter(name__contains=c_name)
        except Category.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_category(request, category, page)


class AddCategory(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get('Name')
        new_item = Category.objects.create(name=name)
        return redirect('category/1')


class ModifyCategory(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get('Name')
        id = request.POST.get('id')
        item = Category.objects.get(id=id)
        item.name = name
        item.save()
        return redirect('category/1')


class DeleteCategory(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        print(id)
        item = Category.objects.get(id=id)
        item.delete()
        return redirect('category/1')


def helper_device(request, device, page):
    paginator = Paginator(device, 12)
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
        'warn': warning(request),
    }
    return render(request, 'device.html', context)


class DeviceView(LoginRequiredMixin, View):

    def get(self, request, page):
        try:
            user = request.user
            device = Device.objects.all()
            if user.is_superuser == 0 and user.is_staff == 1:
                device = Device.objects.filter(manufacture=user)
            elif user.is_superuser == 0 and user.is_staff == 0:
                family = UserInfo.objects.get(user=user).family
                device = device.filter(family=family)
        except Device.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_device(request, device, page)

    def post(self, request, page):
        try:
            device = Device.objects.all()
            d_id = request.POST.get('d_id')
            if d_id:
                device = device.filter(id=d_id)
            d_name = request.POST.get('d_name')
            if d_name:
                device = device.filter(name__contains=d_name)
        except Device.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_device(request, device, page)


class AddDevice(LoginRequiredMixin, View):
    def post(self, request):
        try:
            name = request.POST.get('Name')
            description = request.POST.get('Description')
            place = request.POST.get('Place')
            familyID = request.POST.get('FamilyID')
            family = Family.objects.get(id=familyID)
            manufacture = request.user
            category = Category.objects.get(id=request.POST.get('CategoryID'))
            new_item = Device.objects.create(name=name, description=description, place=place, family=family,
                                             manufacture=manufacture, category=category)
        except Exception as e:
            return redirect('device/1')
        return redirect('device/1')


class ModifyDevice(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            name = request.POST.get('Name')
            description = request.POST.get('Description')
            place = request.POST.get('Place')
            familyID = request.POST.get('FamilyID')
            family = Family.objects.get(id=familyID)
            manufacture = request.user
            category = Category.objects.get(id=request.POST.get('CategoryID'))
            item = Device.objects.get(id=id)
            item.name = name
            item.description = description
            item.place = place
            item.family = family
            item.manufacture = manufacture
            item.category = category
            item.save()
        except Exception as e:
            return redirect('device/1')
        return redirect('device/1')


class DeleteDevice(LoginRequiredMixin, View):
    def post(self, request):
        try:
            id = request.POST.get('id')
            item = Device.objects.get(id=id)
            item.delete()
        except Exception as e:
            return redirect('device/1')
        return redirect('device/1')
