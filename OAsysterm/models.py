from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# 职位,分别为'Staff','Manager','Boss'
class Position(models.Model):
    position_name = models.CharField(max_length=20)

    @staticmethod
    def insert_positions():
        '''将职位自动添加到数据库中'''
        positions = ['Staff', 'Manager', 'Boss', ]
        for p in positions:
            position = Position.objects.filter(position_name=p).first()
            if position is None:
                Position.objects.create(position_name=p)


class MyUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):#u=models.MyUser(username='wangjie',real_name='WangJie',position='Boss'
        now = timezone.now()
        user = self.model(username=username, last_login=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(username, password, **extra_fields)
        u.is_admin = True
        u.save()
        return u


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, db_index=True)
    password = models.CharField(max_length=128)
    real_name = models.CharField(max_length=20, default=None)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['real_name']
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    objects = MyUserManager()


#  流程模型
class Processes(models.Model):
    theme = models.CharField(max_length=256)
    contents = models.TextField()
    #  发起流程的开始时间
    initial_time = models.DateTimeField(default=timezone.now())
    #  审批一次,timestamp改变一次
    timestamp = models.DateTimeField(default=timezone.now())
    # 下一个审批人的名字,'None'表示走到尽头,审批完成
    next_approver = models.CharField(max_length=20, default=None, null=True)
    #  序列号
    process_serial_num = models.CharField(max_length=128, default=datetime.utcnow().strftime('%Y%m%d%H%M%S'))
    # level:High,Normal
    level = models.CharField(max_length=10)
    #  状态，有两种，同意或者不同意
    status = models.CharField(max_length=20, default='agree')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class ProcessComments(models.Model):
    comments = models.TextField()
    comments_stauts = models.CharField(max_length=20)  # 同意或者不同意
    comments_time = models.DateTimeField(default=timezone.now())
    comments_author = models.CharField(max_length=20)
    process = models.ForeignKey(Processes, on_delete=models.CASCADE)
