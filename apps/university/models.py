# -*- coding: utf-8 -*-

from django.db import models


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

    name = models.CharField('Nome', max_length=30)
    email = models.EmailField()
    picture = models.ImageField('Imagem', upload_to='uploads/', blank=True)
    active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Membro desde', auto_now_add=True)
    department = models.ForeignKey('Department', verbose_name='Departamento')
    bio = models.TextField('Biografia', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'


class Department(models.Model):
    """
    A Departament inside the university
    """

    name = models.CharField('Nome', max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class Course(models.Model):
    """
    Model to represent a Course that belongs to a Departament
    """

    name = models.CharField('Nome', max_length=30)
    slug = models.SlugField(blank=True)
    department = models.ForeignKey(Department, verbose_name='Departamento')
    student = models.ManyToManyField(Student, blank=True)
    semester = models.CharField('Semestre', max_length=10, choices=SEMESTER_CHOICES)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.department.name)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Address(models.Model):
    """
    A model to represent a Student address
    """

    student = models.ForeignKey(Student)
    street = models.CharField('Rua', max_length=50)
    number = models.IntegerField('Número', max_length=10)
    neighborhood = models.CharField('Bairro', max_length=30)
    city = models.CharField('Cidade', max_length=30)

    def __unicode__(self):
        return u'%s, %s - %s', self.street, self.number, self.neighborhood

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


class Phone(models.Model):
    """
    A Model to represent the telephone number of the Student
    """

    student = models.ForeignKey(Student)
    number = models.CharField('Número', max_length=15)

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'