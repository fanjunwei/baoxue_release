from django.db import models

# Create your models here.
class Logo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    prefix = models.CharField(max_length=100)
    uboot_build_list = models.CharField(max_length=255)
    kernel_build_name = models.CharField(max_length=255)


class LogoFile(models.Model):
    logo = models.ForeignKey(Logo)
    file_name = models.CharField(max_length=255)


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


class ChangeItem(models.Model):
    change_group = models.ForeignKey(ChangeGroup)
    p1 = models.CharField(max_length=1000)
    p2 = models.CharField(max_length=1000)
    p3 = models.CharField(max_length=1000)
    p4 = models.CharField(max_length=1000)
    p5 = models.CharField(max_length=1000)
    p6 = models.CharField(max_length=1000)
    p7 = models.CharField(max_length=1000)
    p8 = models.CharField(max_length=1000)
    p9 = models.CharField(max_length=1000)
    p10 = models.CharField(max_length=1000)
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
