import re

import django.conf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from data.models import Data
from device.models import Device
from user.models import User, Family, UserInfo, ManufacturerInfo


def warning(request):
    user = request.user
    data = Data.objects.all()
    warn = []
    if user.is_superuser == 0 and user.is_staff == 1:
        device = Device.objects.filter(manufacture=user)
        data = data.filter(device=device)
    elif user.is_superuser == 0 and user.is_staff == 0:
        family = UserInfo.objects.get(user=user).family
        device = Device.objects.filter(family=family)
        data = data.filter(device=device)
    try:
        if data.filter(type='foggy'):
            warn.append('foggy')
    except Exception as e:
        pass
    try:
        if data.filter(type='rain'):
            warn.append('rain')
    except Exception as e:
        pass
    try:
        if data.filter(type='earthquake'):
            warn.append('earthquake')
    except Exception as e:
        pass
    return warn


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('Name')
        password = request.POST.get('Password')
        email = request.POST.get('Email')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': 'The user already exists.'})
        user = User.objects.create_user(username, email, password)
        user_info = UserInfo.objects.create(user=user)

        return redirect(reverse('user:login'))


class LoginView(View):
    def get(self, request):
        # 判断是否已经记录了用户名
        type = request.GET.get('type')
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username': username, 'checked': checked, 'type': type})

    def post(self, request):
        type = request.GET.get('type')
        username = request.POST.get('Name')
        password = request.POST.get('Password')
        remember = request.POST.get('remember')
        try:
            if type == 'admin':
                user = authenticate(username=username, password=password, is_superuser=1)
            elif type == 'manufacturer':
                user = authenticate(username=username, password=password, is_staff=1)
            else:
                user = authenticate(username=username, password=password, is_staff=0, is_superuser=0)
            if user is not None:
                # 用户名密码正确
                login(request, user)
                next_url = request.GET.get('next', reverse('user:dashboard'))
                response = redirect(next_url)
                if remember == 'on':
                    response.set_cookie('username', username)
                else:
                    response.delete_cookie('username')
                return response
        except Exception as e:
            pass
        # 用户名或密码错误
        return render(request, 'login.html', {'errmsg': 'User name or password is error.'})


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        # 自带logout方法请求session信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('user:index'))


class IndexView(View):
    def get(self, request):
        context = None

        user = request.user

        return render(request, 'index.html', context)

class ShopView(View):
    def get(self, request):
        context = None
        user = request.user
        return render(request, 'shop.html', context)

class CartView(View):
    def get(self, request):
        context = None
        user = request.user
        return render(request, 'shop-cart.html', context)

class PopularView(View):
    def get(self, request):
        context = None
        user = request.user
        return render(request, 'shop-popular.html', context)


class DashboardView(View):
    def get(self, request):
        user = request.user
        user_num = User.objects.count()
        device_num = Device.objects.count()
        family_num = Family.objects.count()
        data_num = Data.objects.count()
        context = {
            'user_num': user_num,
            'device_num': device_num,
            'family_num': family_num,
            'data_num': data_num,
            'warn': warning(request),
        }
        return render(request, 'dashboard.html', context)


def helper_user(request, user, page):
    paginator = Paginator(user, 12)
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
    return render(request, 'user.html', context)


class UserView(LoginRequiredMixin, View):

    def get(self, request, page):
        try:
            user = User.objects.all()
        except User.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_user(request, user, page)

    def post(self, request, page):
        try:
            user = User.objects.all()
            u_id = request.POST.get('u_id')
            if u_id:
                user = user.filter(id=u_id)
            u_name = request.POST.get('u_name')
            if u_name:
                user = user.filter(username__contains=u_name)
        except User.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_user(request, user, page)


class ModifyUser(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get('Name')
        id = request.POST.get('id')
        email = request.POST.get('Email')
        item = User.objects.get(id=id)
        item.username = name
        item.email = email
        item.save()
        return redirect('user/1')


class DeleteUser(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        print(id)
        item = User.objects.get(id=id)
        item.delete()
        return redirect('user/1')


def helper_family(request, family, page):
    paginator = Paginator(family, 12)
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
    return render(request, 'family.html', context)


class FamilyView(LoginRequiredMixin, View):
    def get(self, request, page):
        try:
            family = Family.objects.all()
        except Family.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_family(request, family, page)

    def post(self, request, page):
        try:
            family = Family.objects.all()
            f_id = request.POST.get('f_id')
            if f_id:
                family = family.filter(id=f_id)
            address = request.POST.get('address')
            if address:
                family = family.filter(address__contains=address)
        except Family.DoesNotExist as e:
            return redirect(reverse('user:index'))
        return helper_family(request, family, page)


class AddFamily(LoginRequiredMixin, View):
    def post(self, request):
        num = request.POST.get('num')
        zip = request.POST.get('zip')
        area = request.POST.get('area')
        address = request.POST.get('address')
        at_home = request.POST.get('at_home')
        if at_home == 'Yes':
            at_home = 1
        else:
            at_home = 0
        new_item = Family.objects.create(num_of_user=num, zip_code=zip, area=area, address=address, at_home=at_home)
        return redirect('family/1')


class ModifyFamily(LoginRequiredMixin, View):
    def post(self, request):
        num = request.POST.get('num')
        zip = request.POST.get('zip')
        area = request.POST.get('area')
        address = request.POST.get('address')
        at_home = request.POST.get('at_home')
        if at_home == 'Yes':
            at_home = 1
        else:
            at_home = 0
        id = request.POST.get('id')
        item = Family.objects.get(id=id)
        item.num_of_user = num
        item.zip_code = zip
        item.area = area
        item.address = address
        item.at_home = at_home
        item.save()
        return redirect('family/1')


class DeleteFamily(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('id')
        item = Family.objects.get(id=id)
        item.delete()
        return redirect('family/1')


class ProfileView(View):
    def get(self, request):
        user = request.user
        try:
            user_info = UserInfo.objects.get(user=user)
        except Exception as e:
            user_info = None
        try:
            manu_info = ManufacturerInfo.objects.get(user=user)
        except Exception as e:
            manu_info = None
        return render(request, 'profile.html',
                      {'user_info': user_info, 'manu_info': manu_info, 'warn': warning(request), })


class ProfileBasicView(View):
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('name')
        user = request.user
        user.email = email
        user.username = username
        user.save()
        return redirect('user:profile')


class ProfileUserView(View):
    def post(self, request):
        try:
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            family_id = request.POST.get('family_id')
            user = request.user
            user_info = UserInfo.objects.get(user=user)
            user_info.gender = gender
            user_info.phone = phone
            user_info.family_id = family_id
            user_info.save()
        except Exception as e:
            return redirect('user:profile')
        return redirect('user:profile')


class ProfileManuView(View):
    def post(self, request):
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        address = request.POST.get('address')
        user = request.user
        manu_info = ManufacturerInfo.objects.get(user=user)
        manu_info.phone = phone
        manu_info.city = city
        manu_info.address = address
        manu_info.save()
        return redirect('user:profile')
