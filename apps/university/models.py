from django.db import models
from django.utils.translation import ugettext_lazy as _


SEMESTER_CHOICES = (
    ('0', '2013.1'),
    ('1', '2013.2'),
    ('2', '2014.1'),
    ('3', '2014.2'),
)


class Student(models.Model):
    """
    Model to represent a Student in a University
    """

    name = models.CharField(_('Name'), max_length=30)
    email = models.EmailField()
    picture = models.ImageField(upload_to='uploads/', blank=True)
    active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Member Since'), auto_now_add=True)
    department = models.ForeignKey('Department')

    def __unicode__(self):
        return self.name


class Department(models.Model):
    """
    Departament
    """

    name = models.CharField(_('Name'), max_length=30)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    """
    Course
    """

    name = models.CharField(_('Name'), max_length=30)
    slug = models.SlugField()
    department = models.ForeignKey(Department)
    student = models.ManyToManyField(Student, blank=True)
    semester = models.CharField(_('Semester'), max_length=10, choices=SEMESTER_CHOICES)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.department.name)


class Address(models.Model):
    """
    A model to represent a user address
    """

    student = models.ForeignKey(Student)
    street = models.CharField(_('Street'), max_length=50)
    number = models.IntegerField(_('Number'), max_length=10)
    neighborhood = models.CharField(_('Neighborhood'), max_length=30)
    city = models.CharField(_('City'), max_length=30)

    def __unicode__(self):
        return u'%s, %s - %s', self.street, self.number, self.neighborhood

    class Meta:
        verbose_name_plural = _('Adresses')


class Phone(models.Model):
    """
    A Model to represent the telephone number of the user
    """

    student = models.ForeignKey(Student)
    number = models.CharField(_('Number'), max_length=15)