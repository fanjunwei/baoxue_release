# coding=utf-8
import os
import datetime
from django.conf import settings
from django.db import models
from release.helper import *
# Create your models here.
import time


class Logo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    prefix = models.CharField(max_length=100)
    uboot_build_list = models.CharField(max_length=255)
    kernel_build_name = models.CharField(max_length=255)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)


class LogoFile(models.Model):
    logo = models.ForeignKey(Logo)
    file_name = models.CharField(max_length=255)
    img_width = models.IntegerField(default=0)
    img_height = models.IntegerField(default=0)

    class Meta:
        unique_together = (('logo', 'file_name'),)


class Branch(models.Model):
    project = models.CharField(max_length=255)
    custom = models.CharField(max_length=255)
    branch_number = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    version_number = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    decompress_time = models.DateTimeField(null=True)
    screen_width = models.IntegerField()
    screen_height = models.IntegerField()
    logo_name = models.CharField(max_length=100)

    def getFilePath(self):
        branch_base_dir = os.path.join(settings.MEDIA_ROOT, 'branch_base/')
        return os.path.join(branch_base_dir, self.file_name)

    def getDecompressPath(self):
        branch_base_dir = os.path.join(settings.MEDIA_ROOT, 'branch_base/')
        dir = os.path.join(branch_base_dir, self.full_name)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        return dir

    def getEmptyDecompressPath(self):
        branch_base_dir = os.path.join(settings.MEDIA_ROOT, 'branch_base/')
        dir = os.path.join(branch_base_dir, self.full_name)
        if os.path.isdir(dir):
            delDir(dir)
        os.makedirs(dir)
        return dir

    def decompress(self):
        need_decompress = False
        zip_file_path = self.getFilePath()
        if self.decompress_time:
            file_modify_time = datetime.datetime.fromtimestamp(os.stat(zip_file_path).st_mtime)
            if file_modify_time > self.decompress_time:
                need_decompress = True
        else:
            need_decompress = True
        if need_decompress:
            decompress_path = self.getEmptyDecompressPath()
            os.system('unzip %s -d %s' % (zip_file_path, decompress_path))
            if not self.checkDecompress():
                self.decompress_time = datetime.datetime.now()
                self.save()

    def checkDecompress(self):
        decompress_path = self.getDecompressPath()
        release_img_path = os.path.join(decompress_path, 'release_img')
        if not os.path.isdir(release_img_path):
            return '不存在release_img目录'

        return None


    class Meta:
        unique_together = (('project', 'custom', 'branch_number'),)


class SubBranch(models.Model):
    branch = models.ForeignKey(Branch)
    sub_branch_name = models.CharField(max_length=255)
    timestamp = models.IntegerField(default=0)
    is_ex = models.BooleanField(default=False)
    released = models.BooleanField(default=False)
    description = models.TextField(max_length=1024)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('branch', 'sub_branch_name', 'timestamp'),)


class SubBranchExLink(models.Model):
    sub_branch = models.ForeignKey(SubBranch, related_name='sub_branch_ex_link_sub_branch')
    sub_branch_ex = models.ForeignKey(SubBranch, related_name='sub_branch_ex_link_sub_branch_ex')


class ChangeGroup(models.Model):
    sub_branch = models.ForeignKey(SubBranch)
    type = models.CharField(max_length=100)
    type_ex = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1024)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    order = models.IntegerField()
    p1 = models.CharField(max_length=1000, null=True)
    p2 = models.CharField(max_length=1000, null=True)
    p3 = models.CharField(max_length=1000, null=True)
    p4 = models.CharField(max_length=1000, null=True)
    p5 = models.CharField(max_length=1000, null=True)
    p6 = models.CharField(max_length=1000, null=True)
    p7 = models.CharField(max_length=1000, null=True)
    p8 = models.CharField(max_length=1000, null=True)
    p9 = models.CharField(max_length=1000, null=True)
    p10 = models.CharField(max_length=1000, null=True)


class ChangeItem(models.Model):
    change_group = models.ForeignKey(ChangeGroup)
    p1 = models.CharField(max_length=1000, null=True)
    p2 = models.CharField(max_length=1000, null=True)
    p3 = models.CharField(max_length=1000, null=True)
    p4 = models.CharField(max_length=1000, null=True)
    p5 = models.CharField(max_length=1000, null=True)
    p6 = models.CharField(max_length=1000, null=True)
    p7 = models.CharField(max_length=1000, null=True)
    p8 = models.CharField(max_length=1000, null=True)
    p9 = models.CharField(max_length=1000, null=True)
    p10 = models.CharField(max_length=1000, null=True)
    description = models.TextField(max_length=1024)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


class ChangeItemFile(models.Model):
    change_item = models.ForeignKey(ChangeItem)
    file_name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    img_width = models.IntegerField(null=True)
    img_height = models.IntegerField(null=True)
    package_name = models.CharField(max_length=255)


class Upload(models.Model):
    file_name = models.CharField(max_length=255)
    save_name = models.CharField(max_length=255)
    img_width = models.IntegerField(null=True)
    img_height = models.IntegerField(null=True)
    package_name = models.CharField(max_length=255, null=True)
