# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CommonUser'
        db.delete_table(u'core_commonuser')

        # Deleting model 'SuperUser'
        db.delete_table(u'core_superuser')

        # Adding model 'Department'
        db.create_table(u'core_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'core', ['Department'])

        # Adding model 'Student'
        db.create_table(u'core_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Student'])

        # Adding model 'Course'
        db.create_table(u'core_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Department'])),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'core', ['Course'])

        # Adding M2M table for field student on 'Course'
        m2m_table_name = db.shorten_name(u'core_course_student')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'core.course'], null=False)),
            ('student', models.ForeignKey(orm[u'core.student'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'student_id'])

        # Deleting field 'Phone.user'
        db.delete_column(u'core_phone', 'user_id')

        # Adding field 'Phone.student'
        db.add_column(u'core_phone', 'student',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.Student']),
                      keep_default=False)

        # Deleting field 'Address.user'
        db.delete_column(u'core_address', 'user_id')

        # Adding field 'Address.student'
        db.add_column(u'core_address', 'student',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.Student']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'CommonUser'
        db.create_table(u'core_commonuser', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['CommonUser'])

        # Adding model 'SuperUser'
        db.create_table(u'core_superuser', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['SuperUser'])

        # Deleting model 'Department'
        db.delete_table(u'core_department')

        # Deleting model 'Student'
        db.delete_table(u'core_student')

        # Deleting model 'Course'
        db.delete_table(u'core_course')

        # Removing M2M table for field student on 'Course'
        db.delete_table(db.shorten_name(u'core_course_student'))

        # Adding field 'Phone.user'
        db.add_column(u'core_phone', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Phone.student'
        db.delete_column(u'core_phone', 'student_id')

        # Adding field 'Address.user'
        db.add_column(u'core_address', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Address.student'
        db.delete_column(u'core_address', 'student_id')


    models = {
        u'core.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Student']"})
        },
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Department']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Student']", 'symmetrical': 'False'})
        },
        u'core.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.phone': {
            'Meta': {'object_name': 'Phone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Student']"})
        },
        u'core.student': {
            'Meta': {'object_name': 'Student'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['core']