# coding=utf-8
import os
import shutil
import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
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
def logo_delete(request, id):
    if id:
        try:
            db_logo = Logo.objects.get(pk=id)
            logo_dir = os.path.join(settings.MEDIA_ROOT, 'logo', db_logo.name)
            db_logo.delete()
            delDir(logo_dir)
        except Logo.DoesNotExist:
            pass

    return HttpResponseRedirect(reverse('logo_manage', args=['']))


@login_required
def logo_manage(request, id):
    name = request.REQUEST.get('name', '')
    prefix = request.REQUEST.get('prefix', '')
    uboot_build_list = request.REQUEST.get('uboot_build_list', '')
    kernel_build_name = request.REQUEST.get('kernel_build_name', '')
    kernel_image_name = None

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
            uploaded_files_id = request.REQUEST.getlist('uploaded_file')
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
            if id:
                for i in uploaded_files_id:
                    try:
                        db_LogoFile = LogoFile.objects.get(pk=i)
                        upload_file_names.append(db_LogoFile.file_name)
                    except LogoFile.DoesNotExist:
                        pass
            for i in uboot_build_array:
                img_name = '%s_%s.bmp' % (prefix, i)
                if not img_name in upload_file_names:
                    has_error = True
                    messages.error(request, u'未上传' + img_name)
            img_name = '%s_%s.bmp' % (prefix, kernel_build_name)
            kernel_image_name = img_name
            if not img_name in upload_file_names:
                has_error = True
                messages.error(request, u'未上传' + img_name)
        if not has_error:
            try:
                if id:
                    db_logo = Logo.objects.get(pk=id)
                else:
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
                if id:
                    db_logo_files = db_logo.logofile_set.all()
                    for i in db_logo_files:
                        logo_file_id = str(i.id)
                        if not logo_file_id in uploaded_files_id:
                            img_path = os.path.join(logo_dir, i.file_name)
                            i.delete()
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
                        if db_upload.img_width != None and db_upload.img_height != None:
                            db_LogoFile.img_width = db_upload.img_width
                            db_LogoFile.img_height = db_upload.img_height
                        db_LogoFile.save()
                        if kernel_image_name and kernel_image_name == db_LogoFile.file_name:
                            db_logo.width = db_LogoFile.img_width
                            db_logo.height = db_LogoFile.img_height
                            db_logo.save()

                    except:
                        pass
                name = ''
                prefix = ''
                if id:
                    messages.success(request, '修改成功')
                    return HttpResponseRedirect(reverse('logo_manage', args=['']))
                else:
                    messages.success(request, '添加成功')
            except Logo.DoesNotExist:
                has_error = True
                messages.error(request, 'id错误')
            except IntegrityError:
                has_error = True
                messages.error(request, '名称重复')

    if id:
        edit_mode = True
        try:
            db_logo = Logo.objects.get(pk=id)
            name = db_logo.name
            prefix = db_logo.prefix
            uboot_build_list = db_logo.uboot_build_list
            kernel_build_name = db_logo.kernel_build_name
            logo_files = []
            db_logo_files = db_logo.logofile_set.order_by('file_name')
            for i in db_logo_files:
                logo_files.append({'id': i.id, 'file_name': i.file_name})
        except Logo.DoesNotExist:
            has_error = True
            messages.error(request, 'id错误')
    else:
        edit_mode = False

    if not edit_mode:
        logo_list = Logo.objects.order_by('name')
    return TemplateResponse(request, 'logo_manage.html', locals())


@login_required
def logo_browse(request, id):
    try:
        db_logo = Logo.objects.get(pk=id)
        uboot_array = db_logo.uboot_build_list.split(',')
        list = []
        kernel = '%s_%s.bmp' % (db_logo.prefix, db_logo.kernel_build_name)

        for i in uboot_array:
            list.append('%s_%s.bmp' % (db_logo.prefix, i))
        logo_base_url = os.path.join(settings.MEDIA_URL, 'logo', db_logo.name).replace('\\', '/')
    except Logo.DoesNotExist:
        pass
    return TemplateResponse(request, 'logo_browse.html', locals())


@login_required
def branch_delete(request, id):
    if id:
        try:
            db_branch = Branch.objects.get(pk=id)
            branch_base_dir = os.path.join(settings.MEDIA_ROOT, 'branch_base/')
            branch_base_file_path = os.path.join(branch_base_dir, db_branch.full_name + '.zip')
            branch_base_dir_path = os.path.join(branch_base_dir, db_branch.full_name)
            db_branch.delete()
            delDir(branch_base_file_path)
            delDir(branch_base_dir_path)
            messages.success(request, '删除成功')
        except Logo.DoesNotExist:
            pass

    return HttpResponseRedirect(reverse('branch_manage', args=['']))


@login_required
def branch_manage(request, id):
    version_number = None
    if request.method == 'POST':
        project = None
        custom = None
        branch_number = None
        full_name = request.REQUEST.get('full_name')
        screen_width = request.REQUEST.get('screen_width')
        screen_height = request.REQUEST.get('screen_height')
        description = request.REQUEST.get('description')
        upload_file_id = request.REQUEST.get('upload_file_id')
        version_number = request.REQUEST.get('version_number')
        logo_name = request.REQUEST.get('logo_name')
        has_error = False
        if not full_name:
            has_error = True
            messages.error(request, '分支名不能为空')
        if not has_error:
            project, custom, branch_number = split_branch_full_name(full_name)
            if not project:
                has_error = True
                messages.error(request, '分支名格式错误')
        if not has_error:
            if not id:
                test_branch = Branch.objects.filter(full_name=full_name)
                if test_branch.count() > 0:
                    has_error = True
                    messages.error(request, "分支名重复")
        if not has_error:
            branch_base_dir = os.path.join(settings.MEDIA_ROOT, 'branch_base/')
            if not os.path.isdir(branch_base_dir):
                os.makedirs(branch_base_dir)
            branch_base_file_path = os.path.join(branch_base_dir, full_name + '.zip')
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
        if not has_error:
            try:
                if id:
                    db_branch = Branch.objects.get(pk=id)
                else:
                    db_branch = Branch()
                db_branch.project = project
                db_branch.custom = custom
                db_branch.branch_number = branch_number
                db_branch.full_name = full_name
                db_branch.file_name = full_name + '.zip'
                db_branch.version_number = version_number
                db_branch.description = description
                db_branch.screen_width = screen_width
                db_branch.screen_height = screen_height
                db_branch.logo_name = logo_name
                db_branch.decompress()
                error_message = db_branch.checkDecompress()
                if error_message:
                    messages.error(request, error_message)
                    has_error = True
                else:
                    db_branch.save()

            except Branch.DoesNotExist:
                has_error = True
                messages.error(request, 'ID错误')
        if not has_error:
            if id:
                messages.success(request, u'修改成功')
                return HttpResponseRedirect(reverse('branch_manage', args=['']))
            else:
                messages.success(request, u'添加成功')
    logos = Logo.objects.order_by('name')
    if id:
        try:
            db_branch = Branch.objects.get(pk=id)
            full_name = db_branch.full_name
            logo_name = db_branch.logo_name
            screen_width = db_branch.screen_width
            screen_height = db_branch.screen_height
            version_number = db_branch.version_number
            description = db_branch.description

        except Branch.DoesNotExist:
            pass
    else:
        list = Branch.objects.order_by('full_name')
        if not version_number:
            version_number = "V01"
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
