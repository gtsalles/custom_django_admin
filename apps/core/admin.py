from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .models import Student, Department, Course, Address, Phone


class AddresInline(admin.TabularInline):
    model = Address
    extra = 1


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Class CommomUser
    """

    list_display = ('name', 'email', 'department', 'active', 'get_img', 'add_course')
    list_display_links = ('name', 'email')
    # list_editable = ('active',)
    list_filter = ('active', 'date_joined')
    search_fields = ('name', 'email')
    actions = ['activate_users', 'deactivate_users']
    inlines = [AddresInline, PhoneInline]

    def activate_users(self, request, queryset):
        for q in queryset:
            q.active = True
            q.save()
        messages.success(request, _('Users activated!'))

    def deactivate_users(self, request, queryset):
        for q in queryset:
            q.active = False
            q.save()
        messages.success(request, _('Users deactivated!'))

    def get_img(self, obj):
        if obj.picture:
            return u'<img width="50px" height="50px" src="/media/%s" />' % obj.picture
        else:
            return u'Sem imagem'
    get_img.short_description = _('Image')
    get_img.allow_tags = True

    def add_course(self, obj):
        return u'<a target="_blank" onclick="return showAddAnotherPopup(this);"' \
               u'href="/admin/core/course_student/add/?student_id=%s">Matricular</a>' % obj.id
    add_course.allow_tags = True
    add_course.short_description = _('Add Course')


admin.site.register(Student, StudentAdmin)


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Course, CourseAdmin)


class RegistrationAdmin(admin.ModelAdmin):

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