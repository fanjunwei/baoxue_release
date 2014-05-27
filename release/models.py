from django.db import models

# Create your models here.
class Branch(models.Model):
    project = models.CharField(max_length=255)
    custom = models.CharField(max_length=255)
    branch_number = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    version_number = models.CharField(max_length=255)


class SubBranch(models.Model):
    branch = models.ForeignKey(Branch)
    sub_branch_name = models.CharField(max_length=255)
    timestamp = models.IntegerField(default=0)
    is_ex = models.BooleanField(default=False)
    released = models.BooleanField(default=False)


class SubBranchExLink(models.Model):
    sub_branch = models.ForeignKey(SubBranch, related_name='sub_branch_ex_link_sub_branch')
    sub_branch_ex = models.ForeignKey(SubBranch, related_name='sub_branch_ex_link_sub_branch_ex')


class Change(models.Model):
    sub_branch = models.ForeignKey(SubBranch)
    type = models.CharField(max_length=100)
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


class File(models.Model):
    file_name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

