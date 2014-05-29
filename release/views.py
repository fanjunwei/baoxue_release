# coding=utf-8
import os
import shutil
import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
import datetime
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from release.helper import *
from release.models import *
# Create your views here.
from django.template.response import TemplateResponse


def login(request):
    next = request.REQUEST.get('next', '')
    if request.method == 'POST':
        username = request.REQUEST.get('username')
        password = request.REQUEST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse(home))
        else:
            messages.error(request, '用户名或密码错误')
    else:
        users = User.objects.all()
        if users.count() == 0:
            user = User()
            user.username = 'SW'
            user.set_password('SW')
            user.is_superuser = True
            user.save()

    return TemplateResponse(request, 'login.html', locals())


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse(login))


@login_required
def home(request):
    return TemplateResponse(request, 'home.html', locals())


@login_required
def logo_manage(request):
    name = request.REQUEST.get('name', '')
    prefix = request.REQUEST.get('prefix', '')
    uboot_build_list = request.REQUEST.get('uboot_build_list', '')
    kernel_build_name = request.REQUEST.get('kernel_build_name', '')

    if not uboot_build_list:
        uboot_build_list = 'uboot,battery,low_battery,charger_ov,num_0,num_1,num_2,num_3,num_4,num_5,num_6,num_7,num_8,num_9,num_percent,bat_animation_01,bat_animation_02,bat_animation_03,bat_animation_04,bat_animation_05,bat_animation_06,bat_animation_07,bat_animation_08,bat_animation_09,bat_animation_10,bat_10_01,bat_10_02,bat_10_03,bat_10_04,bat_10_05,bat_10_06,bat_10_07,bat_10_08,bat_10_09,bat_10_10,bat_bg,bat_img,bat_100'
    if not kernel_build_name:
        kernel_build_name = 'kernel'
    if request.method == 'POST':
        has_error = False
        if not name:
            has_error = True
            messages.error(request, '名称不能为空')
        if not prefix:
            has_error = True
            messages.error(request, '前缀不能为空')
        if not uboot_build_list:
            has_error = True
            messages.error(request, 'uboot编译列表不能为空')
        if not kernel_build_name:
            has_error = True
            messages.error(request, 'kernel编译不能为空')
        if not has_error:

            upload_files_id = request.REQUEST.getlist('upload_file')
            upload_files = []
            upload_file_names = []

            uboot_build_array = uboot_build_list.split(',')

            for i in upload_files_id:
                try:
                    db_upload = Upload.objects.get(pk=i)
                    upload_files.append(db_upload)
                    upload_file_names.append(db_upload.file_name)
                except Upload.DoesNotExist:
                    pass
            for i in uboot_build_array:
                img_name = '%s_%s.bmp' % (prefix, i)
                if not img_name in upload_file_names:
                    has_error = True
                    messages.error(request, u'未上传' + img_name)
            img_name = '%s_%s.bmp' % (prefix, kernel_build_name)
            if not img_name in upload_file_names:
                has_error = True
                messages.error(request, u'未上传' + img_name)
        if not has_error:
            db_logo = Logo()
            db_logo.name = name
            db_logo.prefix = prefix
            db_logo.uboot_build_list = uboot_build_list
            db_logo.kernel_build_name = kernel_build_name
            db_logo.save()
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'upload')
            logo_dir = os.path.join(settings.MEDIA_ROOT, 'logo', name)
            if not os.path.isdir(logo_dir):
                os.makedirs(logo_dir)
            for i in upload_files:
                try:
                    db_upload = i
                    file_path = os.path.join(upload_dir, db_upload.save_name)
                    img_path = os.path.join(logo_dir, db_upload.file_name)
                    shutil.move(file_path, img_path)
                    db_upload.delete()
                    db_LogoFile = LogoFile()
                    db_LogoFile.logo = db_logo
                    db_LogoFile.file_name = db_upload.file_name
                    db_LogoFile.save()

                except Upload.DoesNotExist:
                    pass
            name = ''
            prefix = ''
            messages.success(request, '添加成功')
    logo_list = Logo.objects.all()
    return TemplateResponse(request, 'logo_manage.html', locals())


@login_required
def branch_manage(request):
    if request.method == 'POST':
        branch = request.REQUEST.get('branch')
        description = request.REQUEST.get('description')
        upload_file_id = request.REQUEST.get('upload_file_id')
        has_error = False
        if not branch:
            has_error = True
            messages.error(request, '分支名不能为空')
        if not has_error:
            branch, custom, branch_number = split_branch_full_name(branch)
            if not branch:
                has_error = True
                messages.error(request, '分支名格式错误')
        if not has_error:
            branch_base_dir = os.path.join(settings.MEDIA_ROOT, 'branch_base/')
            if not os.path.isdir(branch_base_dir):
                os.makedirs(branch_base_dir)
            branch_base_file_path = os.path.join(branch_base_dir, branch + '.zip')
            if upload_file_id:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'upload/')

                try:
                    db_upload = Upload.objects.get(pk=upload_file_id)
                    file_path = os.path.join(upload_dir, db_upload.save_name)
                    shutil.move(file_path, branch_base_file_path)
                    db_upload.delete()
                except Upload.DoesNotExist:
                    pass
            if not os.path.isfile(branch_base_file_path):
                has_error = True
                messages.error(request, '文件不能为空')

    return TemplateResponse(request, 'branch_manage.html', locals())


def upload(request):
    file = request.FILES.get('Filedata', None)
    if file:
        name = file.name
        n, e = os.path.splitext(name)
        file_uuid = str(uuid.uuid1())
        new_name = file_uuid + e
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'upload/')
        if not os.path.isdir(upload_dir):
            os.makedirs(upload_dir)
        if os.path.isdir(upload_dir):
            outfile_path = os.path.join(upload_dir, new_name)
            outfile = open(outfile_path, 'wb')
            for chunk in file.chunks():
                outfile.write(chunk)
            outfile.close()
            db_upload = Upload()
            db_upload.file_name = name
            db_upload.save_name = new_name
            file_type = getFileType(name)
            if file_type == 'image':
                width, height = getImageSize(outfile_path)
                db_upload.img_width = width
                db_upload.img_height = height
            elif file_type == 'apk':
                db_upload.package_name = getApkPackageName(outfile_path)
            db_upload.save()
            o = {
                'id': db_upload.pk,
                'name': name,
            }
            return JsonResponse(True, result=o)
    return JsonResponse(False)
