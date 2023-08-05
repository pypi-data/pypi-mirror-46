# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
# 课程
class Course(models.Model):
    title = models.CharField(max_length=180, verbose_name='课程标题')  # 名字
    subtitle = models.CharField(max_length=180, null=True, verbose_name='课程副标题', blank=True)  # 副标题
    level = models.IntegerField(default=0, verbose_name='课程的level', blank=True)  # 课程的level
    is_del = models.IntegerField(default=0)
    is_auto_open = models.BooleanField(default=False, verbose_name='是否自动开启')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'bee_django_course_simple_course'
        app_label = 'bee_django_course_simple'
        ordering = ["-id"]
        permissions = [
            ('can_manage_course', '可以进入课程管理页'),
            ('view_all_courses', '可以查看所有课程'),
        ]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bee_django_course_simple:course_detail', kwargs={'pk': self.pk})


# 课件
class Section(models.Model):
    course = models.ForeignKey(Course, verbose_name='属于的课程')
    group_name = models.CharField(max_length=180, verbose_name='组名',null=True,blank=True,help_text='如课件前不需显示，则不用填写')
    # pre_title =models.CharField(max_length=180, verbose_name='标题前缀',null=True,blank=True)
    title = models.CharField(max_length=180, verbose_name='课件标题')  # 名字
    extra_title = models.CharField(max_length=180, verbose_name='额外标题',null=True,blank=True)  # 名字
    number = models.IntegerField(verbose_name='排序', default=1)  # 排序
    info = models.TextField(null=True, blank=True, verbose_name='介绍')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'bee_django_course_simple_section'
        app_label = 'bee_django_course_simple'
        ordering = ["number"]
        permissions = [
            ('view_all_sections', '可以查看所有课件'),
        ]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bee_django_course_simple:section_detail', kwargs={'pk': self.pk})


# 小节
class Part(models.Model):
    section = models.ForeignKey(Section, verbose_name='属于的课件')
    # pre_title =models.CharField(max_length=180, verbose_name='标题前缀',null=True,blank=True)
    title = models.CharField(verbose_name='标题', max_length=180)
    extra_title = models.CharField(verbose_name='额外标题', max_length=180,null=True,blank=True)
    number = models.IntegerField(verbose_name='排序', default=1)  # 排序
    type = models.IntegerField(verbose_name='类型', default=1)  # 1-视频 2-单选问题
    has_answer = models.BooleanField(default=False, verbose_name='是否有正确答案')

    class Meta:
        db_table = 'bee_django_course_simple_part'
        app_label = 'bee_django_course_simple'
        ordering = ["number"]
        verbose_name = '小节'

    def __unicode__(self):
        return self.title

    def get_type(self):
        if self.type == 1:
            return '视频'
        elif self.type == 2:
            if self.has_answer:
                return '选择题'
            elif not self.has_answer:
                return '无答案选择题'
        return ''


# 问题
class Question(models.Model):
    course = models.ForeignKey(Course, null=True, verbose_name='课程', blank=True)
    section = ChainedForeignKey(
        Section,
        chained_field="course",
        chained_model_field="course",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        verbose_name='课件')
    part = ChainedForeignKey(
        Part,
        chained_field="section",
        chained_model_field="section",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        verbose_name='小节')
    # part = models.ForeignKey(Part, verbose_name='小节')  # 属于哪个小节
    # city = ChainedForeignKey(
    #     City,
    #     chained_field="province",
    #     chained_model_field="province",
    #     show_all=False,
    #     auto_choose=True,
    #     sort=True,
    #     null=True,
    #     blank=True,
    #     verbose_name='市')
    number = models.IntegerField(verbose_name='排序', default=1)  # 排序
    title = models.CharField(max_length=180, verbose_name='问题', null=True)  # 问题
    tip_wrong = models.TextField(null=True, verbose_name="错误时提示词")
    tip_correct = models.TextField(null=True, verbose_name="正确时提示词")

    class Meta:
        db_table = 'bee_django_course_simple_question'
        app_label = "bee_django_course_simple"
        ordering = ['number']
        permissions = (
            ('view_question', '可以查看问题列表'),
        )


# 选项
class Option(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题')
    title = models.CharField(max_length=180, verbose_name='选项')
    number = models.IntegerField(default=0, verbose_name='顺序')
    is_correct = models.BooleanField(default=False, verbose_name='是否正确答案')

    class Meta:
        db_table = 'bee_django_course_simple_option'
        app_label = "bee_django_course_simple"
        ordering = ['number']


# 视频
class Video(models.Model):
    part = models.ForeignKey(Part, verbose_name='小节')  # 属于哪个小节
    number = models.IntegerField(verbose_name='排序', default=1)  # 排序
    file_name = models.CharField(max_length=180, verbose_name='视频文件名')
    content = models.TextField(verbose_name='内容')

    class Meta:
        db_table = 'bee_django_course_simple_video'
        app_label = "bee_django_course_simple"
        ordering = ['number']


# 富文本上传的图片
class UserImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='simple_user_image')
    image = models.ImageField(verbose_name='图片', upload_to='bee_django_course_simple/video_image/%Y/%m/%d')
    upload_at = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    model_name = models.CharField(max_length=180, verbose_name='model名', null=True)
    model_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'bee_django_course_simple_user_image'
        app_label = 'bee_django_course_simple'


# ======学生相关======
class UserCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='simple_course_user')
    course = models.ForeignKey(Course, verbose_name='课程')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, verbose_name='状态')  # 0 学习中，1 已完成
    passed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bee_django_course_simple_user_course'
        app_label = 'bee_django_course_simple'
        ordering = ['-created_at']
        permissions = [
            ('assign_user_course', '能给学生分配课程'),
        ]

    # 给学生添加自动添加的课程
    @classmethod
    def auto_add(cls, user):
        for course in Course.objects.filter(is_auto_open=True):
            user_course = UserCourse()
            user_course.user = user
            user_course.course = course
            user_course.save()

    # 为学生添加course下的所有section
    def add_user_sections(self):
        section_list = self.course.section_set.all()
        for section in section_list:
            us = UserSection()
            us.user_course = self
            us.section = section
            us.status = 0
            us.save()
        return


class UserSection(models.Model):
    user_course = models.ForeignKey(UserCourse)
    section = models.ForeignKey(Section)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    passed_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)  # 0 未开始， 1 学习中，2 通过

    class Meta:
        db_table = 'bee_django_course_simple_user_section'
        app_label = 'bee_django_course_simple'
        ordering = ['section__number']
        permissions = [
            ('pass_ucs', '能通过学生课件'),
            ('close_ucs', '能关闭学生课件'),
            ('open_ucs', '能开启学生课件'),
        ]

    # 为学生添加section下的所有part
    def add_user_parts(self):
        part_list = self.section.part_set.all()
        for part in part_list:
            up = UserPart()
            up.user_section = self
            up.part = part
            up.status = 0
            up.save()
        return

    def next_user_section(self, status=None):
        number = self.section.number
        section_list = UserSection.objects.filter(user_course=self.user_course, section__number__gt=number)
        if not status == None:
            section_list = section_list.filter(status=status)
        if section_list.exists():
            return section_list.first()
        return None

    # 判断该section是否可以通过
    def can_pass(self):
        part_list = self.section.part_set.all()
        for part in part_list:
            user_part = UserPart.objects.filter(user_section=self, part=part, passed_at__isnull=True)
            if user_part.exists():
                return False
        return True

    def _open(self):
        self.started_at = timezone.now()
        self.status = 1
        self.save()
        return

    def _pass(self):
        self.passed_at = timezone.now()
        self.status = 2
        self.save()
        return

    def _close(self):
        self.status = 0
        self.save()
        return

    def is_close(self):
        return self.status == 0

    def is_open(self):
        return self.status == 1

    def is_pass(self):
        return self.status == 2


class UserPart(models.Model):
    user_section = models.ForeignKey(UserSection)
    part = models.ForeignKey(Part)
    created_at = models.DateTimeField(auto_now_add=True)
    passed_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)  # 0 未开始， 1 学习中，2 通过

    class Meta:
        db_table = 'bee_django_course_simple_user_part'
        app_label = 'bee_django_course_simple'
        ordering = ['part__number']

    def next_user_part(self, status=None):
        number = self.part.number
        part_list = UserPart.objects.filter(user_section=self.user_section, part__number__gt=number)
        if not status == None:
            part_list = part_list.filter(status=status)
        if part_list.exists():
            return part_list.first()
        return None

    def _open(self):
        self.status = 1
        self.save()
        return

    def _pass(self):
        self.status = 2
        self.passed_at = timezone.now()
        self.save()
        return

    def _close(self):
        self.status = 0
        self.save()
        return

    def is_close(self):
        return self.status == 0

    def is_open(self):
        return self.status == 1

    def is_pass(self):
        return self.status == 2

    # 判断该小节是否可以通过
    def can_pass(self):
        video_list = self.part.video_set.all()
        for video in video_list:
            user_video = UserVideo.objects.filter(user_part=self, video=video)
            if not user_video.exists():
                return False
        question_list = self.part.question_set.all()
        for question in question_list:
            user_question = UserQuestion.objects.filter(user_part=self, question=question)
            if not user_question.exists():
                return False
        return True


@receiver(post_save, sender=UserCourse)
def add_user_sections(sender, **kwargs):
    user_course = kwargs['instance']
    if kwargs['created']:
        user_course.add_user_sections()
        user_section_list = user_course.usersection_set.all()
        if user_section_list.exists():
            user_section = user_section_list.first()
            user_section._open()
    return


@receiver(post_save, sender=UserSection)
def add_user_parts(sender, **kwargs):
    user_section = kwargs['instance']
    if kwargs['created']:
        user_section.add_user_parts()
        user_part_list = user_section.userpart_set.all()
        if user_part_list.exists():
            user_part = user_part_list.first()
            user_part._open()
    return


class UserVideo(models.Model):
    user_part = models.ForeignKey(UserPart)
    video = models.ForeignKey(Video)
    passed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bee_django_course_simple_user_video'
        app_label = 'bee_django_course_simple'
        ordering = ['video__number']


class UserQuestion(models.Model):
    user_part = models.ForeignKey(UserPart)
    question = models.ForeignKey(Question)
    passed_at = models.DateTimeField(auto_now_add=True)
    answer_option_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'bee_django_course_simple_user_question'
        app_label = 'bee_django_course_simple'
        ordering = ['question__number']
