# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import json, os, random

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, reverse, redirect, render, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.core.exceptions import PermissionDenied

from qiniu import Auth
from qiniu import BucketManager

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from dss.Serializer import serializer
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Course, Section, Part, Video, Question, Option, UserCourse, UserSection, UserPart, UserVideo, \
    UserQuestion
from .forms import CourseForm, SectionForm, PartForm, PartUpdateForm, VideoForm, QuestionForm, QuestionSearchForm, \
    OptionForm, \
    UploadImageForm, \
    UserCourseForm

User = get_user_model()


# Create your views here.
def test(request):
    q = Question.objects.all()
    for i in q:
        i.course = i.part.section.course
        i.section = i.part.section
        i.save()
    return


# =======course=======
class CourseList(ListView):
    template_name = 'bee_django_course_simple/course/course_list.html'
    context_object_name = 'course_list'
    paginate_by = 20
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('bee_django_course_simple.view_all_courses'):
            self.queryset = Course.objects.none()
        return super(CourseList, self).get(request, *args, **kwargs)


class CourseDetail(DetailView):
    model = Course
    template_name = 'bee_django_course_simple/course/course_detail.html'
    context_object_name = 'course'


@method_decorator(permission_required('bee_django_course_simple.add_course'), name='dispatch')
class CourseCreate(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'bee_django_course_simple/course/course_form.html'


class CourseUpdate(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'bee_django_course_simple/course/course_form.html'


class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class SectionList(ListView):
    template_name = 'bee_django_course_simple/section/section_list.html'
    context_object_name = 'section_list'
    paginate_by = 20
    queryset = Section.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.has_perm("bee_django_course.view_all_sections"):
            return super(SectionList, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        section_name = self.request.GET.get('section_name')
        if section_name:
            return self.queryset.filter(name__contains=section_name)
        else:
            return self.queryset


class SectionDetail(DetailView):
    model = Section
    template_name = 'bee_django_course_simple/section/section_detail.html'
    context_object_name = 'section'


class SectionCreate(CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'bee_django_course_simple/section/section_form.html'

    def get_context_data(self, **kwargs):
        context = super(SectionCreate, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs["course_id"])
        context['type'] = 'add'
        return context

    def form_valid(self, form):
        form.instance.course_id = self.kwargs["course_id"]
        return super(SectionCreate, self).form_valid(form)


class SectionUpdate(UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'bee_django_course_simple/section/section_form.html'

    def get_context_data(self, **kwargs):
        context = super(SectionUpdate, self).get_context_data(**kwargs)
        section = Section.objects.get(id=self.kwargs["pk"])
        context['course'] = section.course
        context['type'] = 'update'
        return context


class SectionDelete(DeleteView):
    model = Section
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class PartList(ListView):
    template_name = 'bee_django_course_simple/part/part_list.html'
    context_object_name = 'part_list'
    paginate_by = 20
    queryset = Part.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.has_perm("bee_django_course_simple.view_all_parts"):
            return super(PartList, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

            # def get_queryset(self):
            #     section_name = self.request.GET.get('section_name')
            #     if section_name:
            #         return self.queryset.filter(name__contains=section_name)
            #     else:
            #         return self.queryset


class PartDetail(DetailView):
    model = Part
    template_name = 'bee_django_course_simple/part/part_detail.html'
    context_object_name = 'part'


class PartCreate(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'bee_django_course_simple/part/part_form.html'
    part = None

    def get_context_data(self, **kwargs):
        context = super(PartCreate, self).get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs["section_id"])
        context['type'] = 'add'
        return context

    def form_valid(self, form):
        form.instance.section_id = self.kwargs["section_id"]
        self.part = form.instance
        return super(PartCreate, self).form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.POST:
            if self.part.type == 1:
                return reverse_lazy("bee_django_course_simple:video_add", kwargs={'part_id': self.part.id})
            elif self.part.type == 2:
                return reverse_lazy("bee_django_course_simple:question_add", kwargs={'part_id': self.part.id})
        else:
            return reverse_lazy("bee_django_course_simple:section_detail", kwargs={'pk': self.part.section.id})


class PartUpdate(UpdateView):
    model = Part
    form_class = PartUpdateForm
    template_name = 'bee_django_course_simple/part/part_form.html'
    part = None

    def get_context_data(self, **kwargs):
        context = super(PartUpdate, self).get_context_data(**kwargs)
        part = Part.objects.get(id=self.kwargs["pk"])
        context['section'] = part.section
        context['type'] = 'update'
        return context

    def form_valid(self, form):
        self.part = form.instance
        return super(PartUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bee_django_course_simple:section_detail', kwargs={'pk': self.part.section.id})


class PartDelete(DeleteView):
    model = Part
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# ==========Video==========
# 上传视频到七牛，需要先获取的token
def get_qiniu_token(key):
    access_key = settings.QINIU_AK
    secret_key = settings.QINIU_SK
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = settings.QINIU_BUCKET_NAME
    # key 上传后保存的文件名

    # 生成上传 Token，可以指定过期时间等
    # 上传策略示例
    # https://developer.qiniu.com/kodo/manual/1206/put-policy
    policy = {
        # 'callbackUrl':'https://requestb.in/1c7q2d31',
        # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        # 'persistentOps':'imageView2/1/w/200/h/200'
    }
    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name, key=key.encode('utf-8'), expires=3600, policy=policy)
    return token


def uptoken(request):
    key = request.GET.get('key')
    token = get_qiniu_token(key)
    return JsonResponse(data={
        'uptoken': token,
        'domain': settings.QINIU_DOMAIN,
    })


def add_video_to_part(request, part_id):
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        try:
            part = get_object_or_404(Part, pk=part_id)
            video_count = part.video_set.all().count() + 1
            part.video_set.create(file_name=file_name, number=video_count)

            return JsonResponse(data={
                'rc': 0,
                'message': '创建成功'
            })
        except Part.DoesNotExist:
            return JsonResponse(data={
                'rc': -1,
                'message': '未找到对应小节'
            })


# 编辑小节视频的文字
def edit_video_content(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == "POST":
        form = VideoForm(data=request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect(reverse('bee_django_course_simple:part_detail', kwargs={'pk': video.part.id}))
        else:
            pass
    else:
        form = VideoForm(instance=video)

    return render(request, 'bee_django_course_simple/video/video_form.html', context={
        'form': form,
    })


# 视频内容富文本图片上传
@csrf_exempt
def upload_image(request):
    max_size = settings.COURSE_UPLOAD_MAXSIZE
    if request.method == "POST":
        file = request.FILES.get(settings.COURSE_SIMPLE_ATTACH_FILENAME)
        if file.size > max_size:
            return HttpResponse("error|图片大小超过5M!")

        # 保存图片。用户上传的图片，与用户的对应关系也保存到数据库中
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            if request.user.is_authenticated:
                user_image.user = request.user
            user_image.save()
            return HttpResponse(user_image.image.url)
        else:
            print form.errors
            return HttpResponse("error|文件存储错误")
    else:
        return HttpResponse("error|请求错误")


def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    return render(request, 'bee_django_course_simple/video/video_detail.html', context={
        'video': video,
        'url': u'http://' + settings.QINIU_DOMAIN + u'/' + video.file_name
    })


def delete_video(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, pk=video_id)

        if request.user.has_perm('bee_django_course_simple.change_section'):
            video.delete()
            return JsonResponse(data={
                'rc': 0,
                'message': '删除成功'
            })
        else:
            return JsonResponse(data={
                'rc': -1,
                'message': '权限不足'
            })


@receiver(pre_delete, sender=Video, dispatch_uid='video_delete_singal')
def delete_qiniu_video(sender, instance, using, **kwargs):
    key = instance.file_name

    access_key = settings.QINIU_AK
    secret_key = settings.QINIU_SK
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)

    # 要上传的空间
    bucket_name = settings.QINIU_BUCKET_NAME

    # 删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key.encode('utf-8'))
    # print(info)


# ========== 小节为问题==============
class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'bee_django_course_simple/question/question_form.html'
    question = None

    def get_context_data(self, **kwargs):
        context = super(QuestionCreate, self).get_context_data(**kwargs)
        context['part'] = Part.objects.get(id=self.kwargs["part_id"])
        return context

    def form_valid(self, form):
        form.instance.part_id = self.kwargs["part_id"]
        part = Part.objects.get(id=self.kwargs["part_id"])
        form.instance.section_id = part.section.id
        form.instance.course_id = part.section.course.id
        self.question = form.instance
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("bee_django_course_simple:option_add", kwargs={"question_id": self.question.id})


# =======选择题==========
class QuestionList(ListView):
    template_name = 'bee_django_course_simple/question/question_list.html'
    context_object_name = 'question_list'
    paginate_by = 20
    http_method_names = [u'get', u"post"]
    queryset = Question.objects.all()

    def search(self):
        course_id = self.request.GET.get("course")
        section_id = self.request.GET.get("section")
        title = self.request.GET.get("title")

        # 检查权限
        if not self.request.user.has_perm("bee_django_course_simple.view_question"):
            self.queryset = Question.objects.none()
            return self.queryset

        if not course_id in ["", 0, None, "0"]:
            self.queryset = self.queryset.filter(part__section__course__id=course_id)
        if not section_id in ["", 0, None, "0"]:
            self.queryset = self.queryset.filter(part__section__id=section_id)
        if not title in ["", 0, None]:
            self.queryset = self.queryset.filter(title__icontains=title)

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        course_id = self.request.GET.get("course")
        section_id = self.request.GET.get("section")
        title = self.request.GET.get("title")

        context['search_form'] = QuestionSearchForm(
            {"course": course_id, "section": section_id, "title": title})
        return context

    def get(self, request, *args, **kwargs):
        self.queryset = self.search()
        return super(QuestionList, self).get(request, *args, **kwargs)


class QuestionDetail(DetailView):
    model = Question
    template_name = 'bee_django_course_simple/question/question_detail.html'
    context_object_name = 'question'


class QuestionUpdate(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'bee_django_course_simple/question/question_form.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs["pk"])
        context['part'] = question.part
        return context

    def get_success_url(self):
        question = Question.objects.get(id=self.kwargs["pk"])
        return reverse_lazy("bee_django_course_simple:part_detail", kwargs={"pk": question.part.id})


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class OptionCreate(CreateView):
    model = Option
    form_class = OptionForm
    template_name = 'bee_django_course_simple/question/option_form.html'
    question = None

    def get_context_data(self, **kwargs):
        context = super(OptionCreate, self).get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs["question_id"])
        context['question'] = question
        context['type'] = 'add'
        return context

    def form_valid(self, form):
        form.instance.question_id = self.kwargs["question_id"]
        self.question = form.instance.question
        return super(OptionCreate, self).form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.POST:
            return reverse_lazy("bee_django_course_simple:option_add", kwargs=self.kwargs)
        else:
            return reverse_lazy("bee_django_course_simple:section_detail", kwargs={"pk": self.question.part.section.id})


class OptionUpdate(UpdateView):
    model = Option
    form_class = OptionForm
    template_name = 'bee_django_course_simple/question/option_form.html'

    def get_context_data(self, **kwargs):
        context = super(OptionUpdate, self).get_context_data(**kwargs)
        option = Option.objects.get(id=self.kwargs["pk"])
        context['question'] = option.question
        context['type'] = 'update'
        return context

    def get_success_url(self):
        option = Option.objects.get(id=self.kwargs["pk"])
        return reverse_lazy("bee_django_course_simple:part_detail", kwargs={"pk": option.question.part.id})


class OptionDelete(DeleteView):
    model = Option
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# ========用户课件列表=========

# 给用户添加新课程
class UserCourseCreate(CreateView):
    model = UserCourse
    form_class = UserCourseForm
    template_name = 'bee_django_course_simple/course/user_course_form.html'
    user_course = None

    # def get_context_data(self, **kwargs):
    #     context = super(OptionCreate, self).get_context_data(**kwargs)
    #     question = Question.objects.get(id=self.kwargs["question_id"])
    #     context['question'] = question
    #     context['type'] = 'add'
    #     return context
    #
    def form_valid(self, form):
        form.instance.user_id = self.kwargs["user_id"]
        self.user_course = form.instance
        return super(UserCourseCreate, self).form_valid(form)

    #
    def get_success_url(self):
        return reverse_lazy("bee_django_course_simple:user_section_list",
                            kwargs={"user_id": self.kwargs["user_id"], "user_course_id": self.user_course.id})


class UserCourseDelete(DeleteView):
    model = UserCourse
    success_url = reverse_lazy('bee_django_course_simple:course_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# 查看指定用户user的课件列表
class UserSectionList(ListView):
    template_name = "bee_django_course_simple/section/user_section_list.html"
    model = UserSection
    queryset = None
    paginate_by = 30
    context_object_name = 'user_section_list'
    user_course = None
    user_course_list = []

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user_course_id = self.kwargs["user_course_id"]
        self.user_course_list = UserCourse.objects.filter(user__id=user_id).order_by('status', '-created_at')
        if not user_course_id in [None, 0, "0", u"0"]:
            self.user_course = UserCourse.objects.get(id=user_course_id)
        else:
            if self.user_course_list.exists():
                self.user_course = self.user_course_list.first()
        if self.user_course:
            self.section_list = self.user_course.course.section_set.all()
            return self.section_list
        else:
            return UserSection.objects.none()

    def get_context_data(self, **kwargs):
        context = super(UserSectionList, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["user_id"])
        context["user"] = user
        context["user_course"] = self.user_course
        context["user_course_list"] = self.user_course_list
        context["user_section_list"] = UserSection.objects.filter(user_course=self.user_course)
        return context


class CustomUserSectionList(UserSectionList):
    template_name = "bee_django_course_simple/section/custom_user_section_list.html"


class UserSectionDetail(DetailView):
    model = UserSection
    template_name = 'bee_django_course_simple/section/user_section_detail.html'
    context_object_name = 'user_section'


class CustomUserSectionDetailRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user_course_list = UserCourse.objects.filter(user__id=user_id).order_by("status")
        if user_course_list.exists():
            user_course = user_course_list.first()
            #  只找正在学的和已通过的。
            user_section_list = user_course.usersection_set.filter(status__gte=1).order_by("status", "section__number")
            if user_course_list.exists():
                user_section = user_section_list.first()
                self.url = reverse('bee_django_course_simple:custom_user_section_detail',
                                   kwargs={"pk": user_section.id})
            else:
                self.url = reverse('bee_django_course_simple:custom_user_section_empty')
        else:
            self.url = reverse('bee_django_course_simple:custom_user_section_empty')

        return super(CustomUserSectionDetailRedirect, self).get_redirect_url(*args, **kwargs)


class CustomUserSectionDetail(UserSectionDetail):
    template_name = 'bee_django_course_simple/section/custom_user_section_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomUserSectionDetail, self).get_context_data(**kwargs)
        context["qiniu_domain"] = settings.QINIU_DOMAIN
        user_section = UserSection.objects.get(id=self.kwargs["pk"])
        context["next_user_section"] = user_section.next_user_section(status=1)
        return context


class CustomUserSectionEmpty(TemplateView):
    template_name = 'bee_django_course_simple/section/custom_user_section_empty.html'


class UserSectionUpdate(TemplateView):
    def post(self, request, *args, **kwargs):
        user_section_id = self.kwargs["user_section_id"]
        type = self.kwargs["type"]
        user_section = UserSection.objects.get(id=user_section_id)
        msg = ''
        if type == 'open':
            user_section._open()
            msg = '开启'
        elif type == 'pass':
            user_section._pass()
            # user section下的所有user part也通过
            for user_part in user_section.userpart_set.all():
                user_part._pass()
            next_user_section = user_section.next_user_section(status=0)
            if next_user_section:
                next_user_section._open()
            msg = '通过'
        elif type == 'close':
            user_section._close()
            # user section下的所有user part也关闭
            for user_part in user_section.userpart_set.all():
                user_part._close()
            msg = '关闭'
        return JsonResponse(data={
            'rc': 0,
            'message': msg + '成功'
        })


class UserPartUpdate(TemplateView):
    def post(self, request, *args, **kwargs):
        user_part_id = self.kwargs["user_part_id"]
        question_data = self.request.POST.get("question_data")
        video_id = self.request.POST.get("video_id")

        next_user_part_id = None
        next_user_section_id = None
        next_user_section_url = None
        user_part = UserPart.objects.get(id=user_part_id)
        question_count = 0  # 小节中题目数量
        question_correct_count = 0  # 小节中答对题目数量

        # 保存记录,更新part内question或video状态
        if question_data:
            question_data = json.loads(question_data)
            for question in question_data:
                # 记录过则不记录
                u_q = UserQuestion.objects.filter(user_part=user_part, question_id=question['question_id'])
                if u_q.exists():
                    continue
                user_question = UserQuestion()
                user_question.user_part = user_part
                user_question.question_id = question["question_id"]
                user_question.answer_option_id = question["option_id"]
                user_question.save()

                # 该小节问题的数量
                question_count = Question.objects.filter(part=user_part.part).count()
                # 检查答案
                corrent_option = Option.objects.filter(question__id=question["question_id"], id=question["option_id"],
                                                       is_correct=True)
                if corrent_option:
                    question_correct_count += 1

        if video_id:
            video = Video.objects.get(id=video_id)
            # 记录过则不记录
            u_v = UserVideo.objects.filter(user_part=user_part, video=video)
            if not u_v.exists():
                video = Video.objects.get(id=video_id)
                user_video = UserVideo()
                user_video.user_part = user_part
                user_video.video = video
                user_video.save()

        # 判断当前user part是否可以通过，更新user part 状态
        user_part_can_pass = user_part.can_pass()
        if user_part_can_pass and user_part.is_open():
            user_part._pass()

        # 查找下一个user part，检查自动开启
        next_user_part = user_part.next_user_part(status=0)
        if next_user_part:
            next_user_part_id = next_user_part.id
            if user_part_can_pass and next_user_part.is_close():
                next_user_part._open()

        # 判断当前user section是否可以通过
        user_section_can_pass = user_part.user_section.can_pass()
        if user_section_can_pass and user_part.user_section.is_open():
            user_part.user_section._pass()

        # 查找下一个user section，检查自动开启
        next_user_section = user_part.user_section.next_user_section(status=0)
        if next_user_section and user_section_can_pass:
            next_user_section._open()
            next_user_section_id = next_user_section.id
            next_user_section_url = reverse('bee_django_course_simple:custom_user_section_detail',
                                            kwargs={'pk': next_user_section_id})

        return JsonResponse(data={
            'error': 0,
            'message': '成功',
            'next_user_part_id': next_user_part_id,
            'next_user_section_id': next_user_section_id,
            'next_user_section_url': next_user_section_url,
            'user_part_can_pass': user_part_can_pass,
            "user_section_can_pass": user_section_can_pass,
            "question_count": question_count,
            "question_correct_count": question_correct_count,
        })


# VueJS 拉取数据用
class VueUserSection(TemplateView):
    def get(self, request, *args, **kwargs):
        user_section_id = self.kwargs['user_section_id']
        user_section = get_object_or_404(UserSection, pk=user_section_id)
        user_parts = user_section.userpart_set.all()

        for user_part in user_parts:
            user_part.part_type = user_part.part.type
            user_part.part_title = user_part.part.title
            user_part.extra_title = user_part.part.extra_title

            if user_part.part_type == 1:
                videos = []
                for v in user_part.part.video_set.all():
                    videos.append({
                        'id': v.id,
                        'content': v.content,
                        'url': "http://" + settings.QINIU_DOMAIN + "/" + v.file_name
                    })
                user_part.videos = videos
            elif user_part.part_type == 2:
                questions = []
                for q in user_part.part.question_set.all():
                    options = []
                    for o in q.option_set.all():
                        options.append({
                            'id': o.id,
                            'title': o.title
                        })
                    questions.append({
                        'id': q.id,
                        'title': q.title,
                        'options': options
                    })
                user_part.questions = questions

        data = serializer(user_parts, output_type='json', datetime_format='string')

        return JsonResponse(data={
            'user_parts': data,
            'status': user_section.status,
        })
