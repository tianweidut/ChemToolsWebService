# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Picture'
        db.create_table('fileupload_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('fileupload', ['Picture'])

        # Adding model 'ProcessedFile'
        db.create_table('fileupload_processedfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('file_obj', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('fileupload', ['ProcessedFile'])


    def backwards(self, orm):
        # Deleting model 'Picture'
        db.delete_table('fileupload_picture')

        # Deleting model 'ProcessedFile'
        db.delete_table('fileupload_processedfile')


    models = {
        'fileupload.picture': {
            'Meta': {'object_name': 'Picture'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'fileupload.processedfile': {
            'Meta': {'object_name': 'ProcessedFile'},
            'file_obj': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        }
    }

    complete_apps = ['fileupload']