import markdown
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import MyUser, Processes, Position
from .forms import ApprovalFrom, AddAccountForm

PAGINATION_NUM_PER_PAGE = 5


@login_required
def logout_site(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


class IndexView(LoginRequiredMixin, ListView):
    """此视图为用户登录后进入系统的首页，显示该用户需要审批的流程"""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Processes
    template_name = 'main/index.html'
    context_object_name = 'process'
    paginate_by = PAGINATION_NUM_PER_PAGE

    def get_queryset(self):
        current_user = self.request.user
        return super().get_queryset().filter(next_approver=current_user.username)


# 详情页面，并进行流程审批
class ProcessDetailView(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Processes
    template_name = 'main/detail.html'
    context_object_name = 'process'
    form_class = ApprovalFrom
    success_url = reverse_lazy('OAsysterm:index')

    def get_context_data(self, **kwargs):
        form = ApprovalFrom()
        context = super().get_context_data()
        next_users = None
        #  如果当前用户的职位是Boss，则流程没有下一位审批人,流程结束;
        #   否则下一位审批人是比当前用户职位高一个等级的用户.
        # 职位有三个,从低到到依次为staff, manager,boss, id分别为1,2,3
        if self.request.user.position.position_name != 'Boss':
            next_users = MyUser.objects.filter(
                position=Position.objects.get(pk=self.request.user.position.id + 1)).all()
        context.update({'form': form, 'next_users': next_users})
        return context

    def get_object(self, queryset=None):
        self.process = super().get_object(queryset=None)
        return super().get_object(queryset=None)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.process.next_approver = self.request.POST.get('nextuser')
        self.process.timestamp = timezone.now()
        self.process.save()
        form.save(author=self.request.user, process=self.process)
        return super().form_valid(form)


class AccountManageView(LoginRequiredMixin, ListView):
    """管理帐号,显示账号基本概况.有两种情况,如果当前用户是管理员权限,
    则显示系统所有的用户信息;否则只显示当前用户信息"""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = MyUser
    template_name = 'main/account_manage.html'
    context_object_name = 'users'
    paginate_by = PAGINATION_NUM_PER_PAGE

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_admin:
            return super().get_queryset().order_by('pk')
        else:
            return super().get_queryset().filter(username=current_user.username)


#  增加新账号，仅管理员可用
class AddAccountsView(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'main/add_account.html'
    form_class = AddAccountForm
    success_url = reverse_lazy('OAsysterm:account_manage')

    def form_valid(self, form):
        if form.check_username():
            form.save()
        else:
            messages.add_message(self.request, messages.INFO, "The username already exists,please try another one.")
        return super().form_valid(form)


#  删除账号，仅管理员可用
@login_required
def delete_account(request, pk):
    if request.user.is_admin:
        u = MyUser.objects.get(pk=pk)
        u.delete()
    else:
        messages.add_message(request, messages.INFO, "You can't delete it.")
    return HttpResponseRedirect(reverse('OAsysterm:account_manage'))


@login_required
def edit_account(request, pk):
    """编辑账户信息.有三种情况:
        1,当前用户是管理员且编辑对象是当前用户，则可以编辑账号名、密码、真实姓名、职位、权限;
        2,当前用户是管理员但编辑其他用户信息，则不可以改密码:,可以编辑账号名、真实姓名、职位、权限;
        3,当前用户不是管理员，则只能修改本人密码、真实姓名"""
    edit_user = get_object_or_404(MyUser, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            p = Position.objects.filter(position_name=form.cleaned_data['position']).first()
            is_admin = form.cleaned_data['is_admin']
            edit_user.real_name = form.cleaned_data['realname']
            if current_user == edit_user:
                #  首先检查密码的输入情况.如果没有输入密码或新密码与再一次确认的密码不一致,则密码不改动;
                # 如果输入密码,则验证密码是否正确,随后改动密码
                if form.check_new_and_old_password():
                    # user类内置的验证密码函数:check_password
                    if edit_user.check_password(form.cleaned_data['old_password']):
                        edit_user.password = make_password(form.cleaned_data['new_password'])
                        messages.add_message(request, messages.INFO, 'Password has been changed!')
                    else:
                        messages.add_message(request, messages.INFO, 'The old password is incorrect!')
                else:
                    messages.add_message(request, messages.INFO, 'Password has not been changed!')
                #  仅管理员可修改账号名
                if current_user.is_admin:
                    edit_user.username = form.cleaned_data['username']
                    edit_user.is_admin = is_admin
                    edit_user.position = p
                edit_user.save()
                return HttpResponseRedirect(reverse('OAsysterm:account_manage'))
            else:
                if current_user.is_admin:
                    #  只有用户名和原来的用户名不一样且不与其他用户名重复，才储存到数据库
                    if form.cleaned_data['username'] != edit_user.username and form.check_username():
                        edit_user.username = form.cleaned_data['username']
                    elif form.cleaned_data['username'] != edit_user.username:
                        messages.add_message(request, messages.INFO,
                                             "The username already exists,please try another one.")
                    edit_user.is_admin = is_admin
                    edit_user.position = p
                    edit_user.save()
                    return HttpResponseRedirect(reverse('OAsysterm:account_manage'))
    #  初始化表单，让表单填充原先的数据
    form = AddAccountForm(initial={
        'username': edit_user.username,
        'realname': edit_user.real_name,
        'position': edit_user.position.position_name,
        'is_admin': edit_user.is_admin,
    })
    return render(request, template_name='main/edit_account.html', context={'edit_user': edit_user, 'form': form})


@login_required
def start_process_view(request):
    """发起流程.有两种情况,一种是当前用户职位是Boss，则无需发流程;
    其他情况发流程则需要选中下一个比自己职级高一级的人员"""
    next_users = None
    current_user_position_id = request.user.position_id
    # 判断当前用户职位是否比Boss低，id=3就是BOSS职位
    if current_user_position_id < 3:
        next_users = MyUser.objects.filter(position_id=current_user_position_id + 1).all()
    if next_users is None:
        messages.add_message(request, messages.INFO, "You need not create process!")
        return HttpResponseRedirect(reverse('OAsysterm:index'))
    else:
        #  获取表单数据
        if request.method == 'POST':
            #   渲染Markdown文本
            contets_md = markdown.markdown(request.POST.get('contents'))

            Processes.objects.create(
                theme=request.POST.get('theme'),
                contents=contets_md,
                next_approver=request.POST.get('nextuser'),
                level=request.POST.get('level'),
                author=request.user
            )
            return HttpResponseRedirect(reverse('OAsysterm:index'))
    return render(request, template_name='main/startprocess.html', context={'next_users': next_users})


#  显示当前用户已经发起的流程概况
class MyProcessesView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Processes
    template_name = 'main/myprocess.html'
    context_object_name = 'myprocess'
    paginate_by = PAGINATION_NUM_PER_PAGE

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


#  进入已发起的流程详情页面
class MyProcessDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Processes
    template_name = 'main/myprocess_detail.html'
    context_object_name = 'myprocess'
