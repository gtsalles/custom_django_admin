# -*- coding: utf-8 -*-

from django.core.serializers import serialize
from django.core.mail import send_mail
from django.contrib import admin
from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from django.utils.text import slugify
from django.shortcuts import render
from ckeditor.widgets import CKEditorWidget
from .models import Student, Department, Course, Address, Phone
from .forms import EmailForm


class AddresInline(admin.TabularInline):
    model = Address
    extra = 1


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class StudentAdmin(admin.ModelAdmin):   
    """
    ModelAdmin for the Model Student
    """

    list_display = ('name', 'email', 'department', 'active', 'get_img', 'add_course')
    list_display_links = ('name', 'email')
    list_filter = ('active', 'date_joined')
    search_fields = ('name', 'email', 'department__name')
    list_editable = ('active',)
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
    save_as = True
    inlines = [AddresInline, PhoneInline]
    actions = ['activate_users', 'deactivate_users', 'export_as_json', 'send_msg']
    
    # readonly_fields = ('name',)
    # raw_id_fields = ('department',)
    # list_select_related = ('student',)
    
    def get_img(self, obj):
        if obj.picture:
            return u'<img width="50px" height="50px" src="/media/%s" />' % obj.picture
        else:
            return u'Sem imagem'
    get_img.short_description = 'Imagem'
    get_img.allow_tags = True

    def activate_users(self, request, queryset):
        queryset.update(active=True)
        messages.success(request, 'Usuário(s) ativado(s)!')

    def deactivate_users(self, request, queryset):
        queryset.update(active=False)
        messages.success(request, 'Usuário(s) desativado(s)!')

    def add_course(self, obj):
        return u'<a onclick="return showAddAnotherPopup(this);"' \
               u'href="/admin/university/course_student/add/?student_id=%s">Matricular</a>' % obj.id
    add_course.allow_tags = True
    add_course.short_description = 'Matricular'

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        serialize('json', queryset, stream=response)
        return response

    def send_msg(self, request, queryset):
        if 'post' in request.POST:
            form = EmailForm(request.POST)
            if form.is_valid():
                emails = [q.email for q in queryset]
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                from_email = form.cleaned_data.get('from_mail')
                sent = send_mail(subject=subject,
                                 message=message,
                                 from_email=from_email,
                                 recipient_list=emails)
                if sent:
                    messages.success(request, 'Emails Enviados!')
        else:
            form = EmailForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'messages.html', {'form': form})

admin.site.register(Student, StudentAdmin)


class CourseAdmin(admin.ModelAdmin):
    """
    ModelAdmin for the Model Course
    """

    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        kwargs['exclude'] = 'student'
        return super(CourseAdmin, self).get_form(request, obj=None, **kwargs)

admin.site.register(Course, CourseAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    """
    ModelAdmin for the model responsable for the relation between Students and Courses
    """

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        student_id = request.GET.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return super(RegistrationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'student':
            kwargs['queryset'] = Student.objects.filter(id=student.id)
            kwargs['initial'] = student
        if db_field.name == 'course':
            kwargs['queryset'] = Course.objects.filter(department=student.department)
        return super(RegistrationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course.student.through, RegistrationAdmin)

admin.site.register(Department)