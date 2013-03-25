# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActiveKeyInfo'
        db.create_table('gui_activekeyinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyValue', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('totalCount', self.gf('django.db.models.fields.IntegerField')()),
            ('leftCount', self.gf('django.db.models.fields.IntegerField')()),
            ('isAlreadLocated', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('gui', ['ActiveKeyInfo'])

        # Adding model 'LanguageEnum'
        db.create_table('gui_languageenum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('languageStr', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('gui', ['LanguageEnum'])

        # Adding model 'ActiveHistory'
        db.create_table('gui_activehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('activeIP', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('activeTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('antActiveIP', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('antActiveTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('activekey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gui.ActiveKeyInfo'])),
        ))
        db.send_create_signal('gui', ['ActiveHistory'])

        # Adding model 'ModelInfo'
        db.create_table('gui_modelinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modelName', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('gui', ['ModelInfo'])

        # Adding model 'CompoundInfo'
        db.create_table('gui_compoundinfo', (
            ('smilesInfo', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
            ('casInfo', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gui', ['CompoundInfo'])

        # Adding model 'CompoundName'
        db.create_table('gui_compoundname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('simlesInfo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gui.CompoundInfo'])),
            ('nameStr', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('languageID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gui.LanguageEnum'])),
            ('isDefault', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gui', ['CompoundName'])

        # Adding model 'CalculateHistory'
        db.create_table('gui_calculatehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('calculateStartTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('calculateEndTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('paramInfo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('result', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('isFinished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modelInfo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gui.ModelInfo'])),
            ('smilesInfo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gui.CompoundInfo'])),
        ))
        db.send_create_signal('gui', ['CalculateHistory'])


    def backwards(self, orm):
        # Deleting model 'ActiveKeyInfo'
        db.delete_table('gui_activekeyinfo')

        # Deleting model 'LanguageEnum'
        db.delete_table('gui_languageenum')

        # Deleting model 'ActiveHistory'
        db.delete_table('gui_activehistory')

        # Deleting model 'ModelInfo'
        db.delete_table('gui_modelinfo')

        # Deleting model 'CompoundInfo'
        db.delete_table('gui_compoundinfo')

        # Deleting model 'CompoundName'
        db.delete_table('gui_compoundname')

        # Deleting model 'CalculateHistory'
        db.delete_table('gui_calculatehistory')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gui.activehistory': {
            'Meta': {'object_name': 'ActiveHistory'},
            'activeIP': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'activeTime': ('django.db.models.fields.DateTimeField', [], {}),
            'activekey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gui.ActiveKeyInfo']"}),
            'antActiveIP': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'antActiveTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"})
        },
        'gui.activekeyinfo': {
            'Meta': {'object_name': 'ActiveKeyInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isAlreadLocated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keyValue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'leftCount': ('django.db.models.fields.IntegerField', [], {}),
            'totalCount': ('django.db.models.fields.IntegerField', [], {})
        },
        'gui.calculatehistory': {
            'Meta': {'object_name': 'CalculateHistory'},
            'calculateEndTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'calculateStartTime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isFinished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modelInfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gui.ModelInfo']"}),
            'paramInfo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'smilesInfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gui.CompoundInfo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"})
        },
        'gui.compoundinfo': {
            'Meta': {'object_name': 'CompoundInfo'},
            'casInfo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'smilesInfo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'})
        },
        'gui.compoundname': {
            'Meta': {'object_name': 'CompoundName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isDefault': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languageID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gui.LanguageEnum']"}),
            'nameStr': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'simlesInfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gui.CompoundInfo']"})
        },
        'gui.languageenum': {
            'Meta': {'object_name': 'LanguageEnum'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languageStr': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gui.modelinfo': {
            'Meta': {'object_name': 'ModelInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modelName': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'agentID': ('django.db.models.fields.CharField', [], {'default': "UUID('2a3249cb-24bc-4ead-9af6-356cccd1e9e0')", 'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machinecode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'workunit': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'})
        }
    }

    complete_apps = ['gui']