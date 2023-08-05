# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestLog'
        db.create_table(u'aio_client_requestlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('error', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('timestamp_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('request_type', self.gf('django.db.models.fields.CharField')(default=u'get/api/v0/as-provider/request', max_length=100)),
            ('sender_url', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('http_header', self.gf('django.db.models.fields.TextField')(default='{"Content-Type": "application/json;charset=utf-8"}')),
            ('http_body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'aio_client', ['RequestLog'])

        # Adding model 'PostConsumerRequest'
        db.create_table(u'aio_client_postconsumerrequest', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state',
             self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('request_id',
             self.gf('django.db.models.fields.related.ForeignKey')(
                 to=orm['aio_client.RequestLog'])),
            ('message_type',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('origin_message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('attachments',
             self.gf('django.db.models.fields.CharField')(default=u'[]',
                                                          max_length=500,
                                                          blank=True)),
            ('is_test_message',
             self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aio_client', ['PostConsumerRequest'])

        # Adding model 'GetConsumerResponse'
        db.create_table(u'aio_client_getconsumerresponse', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state',
             self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('request_id',
             self.gf('django.db.models.fields.related.ForeignKey')(
                 to=orm['aio_client.RequestLog'])),
            ('message_type',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('origin_message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('attachments',
             self.gf('django.db.models.fields.CharField')(default=u'[]',
                                                          max_length=500,
                                                          blank=True)),
        ))
        db.send_create_signal(u'aio_client', ['GetConsumerResponse'])

        # Adding model 'GetConsumerReceipt'
        db.create_table(u'aio_client_getconsumerreceipt', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state',
             self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('request_id',
             self.gf('django.db.models.fields.related.ForeignKey')(
                 to=orm['aio_client.RequestLog'])),
            ('message_type',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('origin_message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('error',
             self.gf('django.db.models.fields.TextField')(default=u'')),
            ('fault',
             self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aio_client', ['GetConsumerReceipt'])

        # Adding model 'GetProviderRequest'
        db.create_table(u'aio_client_getproviderrequest', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state',
             self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('request_id',
             self.gf('django.db.models.fields.related.ForeignKey')(
                 to=orm['aio_client.RequestLog'])),
            ('message_type',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('origin_message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('attachments',
             self.gf('django.db.models.fields.CharField')(default=u'[]',
                                                          max_length=500,
                                                          blank=True)),
            ('is_test_message',
             self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('replay_to',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'aio_client', ['GetProviderRequest'])

        # Adding model 'PostProviderRequest'
        db.create_table(u'aio_client_postproviderrequest', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state',
             self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('request_id',
             self.gf('django.db.models.fields.related.ForeignKey')(
                 to=orm['aio_client.RequestLog'])),
            ('message_type',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('origin_message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('attachments',
             self.gf('django.db.models.fields.CharField')(default=u'[]',
                                                          max_length=500,
                                                          blank=True)),
            ('replay_to',
             self.gf('django.db.models.fields.CharField')(max_length=4000)),
            ('content_failure_code',
             self.gf('django.db.models.fields.CharField')(max_length=50,
                                                          null=True,
                                                          blank=True)),
            ('content_failure_comment',
             self.gf('django.db.models.fields.TextField')(default=u'',
                                                          blank=True)),
            ('is_test_message',
             self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aio_client', ['PostProviderRequest'])

        # Adding model 'GetProviderReceipt'
        db.create_table(u'aio_client_getproviderreceipt', (
            ('id',
             self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state',
             self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('request_id',
             self.gf('django.db.models.fields.related.ForeignKey')(
                 to=orm['aio_client.RequestLog'])),
            ('message_type',
             self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('origin_message_id',
             self.gf('django.db.models.fields.CharField')(max_length=100,
                                                          null=True)),
            ('error',
             self.gf('django.db.models.fields.TextField')(default=u'')),
            ('fault',
             self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aio_client', ['GetProviderReceipt'])

    def backwards(self, orm):
        # Deleting model 'RequestLog'
        db.delete_table(u'aio_client_requestlog')

        # Deleting model 'PostConsumerRequest'
        db.delete_table(u'aio_client_postconsumerrequest')

        # Deleting model 'GetConsumerResponse'
        db.delete_table(u'aio_client_getconsumerresponse')

        # Deleting model 'GetConsumerReceipt'
        db.delete_table(u'aio_client_getconsumerreceipt')

        # Deleting model 'GetProviderRequest'
        db.delete_table(u'aio_client_getproviderrequest')

        # Deleting model 'PostProviderRequest'
        db.delete_table(u'aio_client_postproviderrequest')

        # Deleting model 'GetProviderReceipt'
        db.delete_table(u'aio_client_getproviderreceipt')

    models = {
        u'aio_client.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            'error': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'http_body': ('django.db.models.fields.TextField', [], {}),
            'http_header': ('django.db.models.fields.TextField', [], {'default': '\'{"Content-Type": "application/json;charset=utf-8"}\''}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_type': ('django.db.models.fields.CharField', [], {'default': "u'get/api/v0/as-provider/request'", 'max_length': '100'}),
            'sender_url': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'aio_client.getconsumerreceipt': {
            'Meta': {'object_name': 'GetConsumerReceipt'},
            'error': (
            'django.db.models.fields.TextField', [], {'default': "u''"}),
            'fault': (
            'django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [],
                           {'max_length': '100', 'null': 'True'}),
            'message_type': (
            'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_message_id': ('django.db.models.fields.CharField', [],
                                  {'max_length': '100', 'null': 'True'}),
            'request_id': ('django.db.models.fields.related.ForeignKey', [],
                           {'to': u"orm['aio_client.RequestLog']"}),
            'state': (
            'django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'aio_client.getconsumerresponse': {
            'Meta': {'object_name': 'GetConsumerResponse'},
            'attachments': ('django.db.models.fields.CharField', [],
                            {'default': "u'[]'", 'max_length': '500',
                             'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [],
                           {'max_length': '100', 'null': 'True'}),
            'message_type': (
            'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_message_id': ('django.db.models.fields.CharField', [],
                                  {'max_length': '100', 'null': 'True'}),
            'request_id': ('django.db.models.fields.related.ForeignKey', [],
                           {'to': u"orm['aio_client.RequestLog']"}),
            'state': (
            'django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'aio_client.postconsumerrequest': {
            'Meta': {'object_name': 'PostConsumerRequest'},
            'attachments': ('django.db.models.fields.CharField', [],
                            {'default': "u'[]'", 'max_length': '500',
                             'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': (
            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_test_message': (
            'django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message_id': ('django.db.models.fields.CharField', [],
                           {'max_length': '100', 'null': 'True'}),
            'message_type': (
            'django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_message_id': ('django.db.models.fields.CharField', [],
                                  {'max_length': '100', 'null': 'True'}),
            'request_id': ('django.db.models.fields.related.ForeignKey', [],
                           {'to': u"orm['aio_client.RequestLog']"}),
            'state': (
            'django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'aio_client.getproviderreceipt': {
            'Meta': {'object_name': 'GetProviderReceipt'},
            'error': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'fault': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_message_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'request_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aio_client.RequestLog']"}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'aio_client.getproviderrequest': {
            'Meta': {'object_name': 'GetProviderRequest'},
            'attachments': ('django.db.models.fields.CharField', [], {'default': "u'[]'", 'max_length': '500', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_test_message': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_message_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'replay_to': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'request_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aio_client.RequestLog']"}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'aio_client.postproviderrequest': {
            'Meta': {'object_name': 'PostProviderRequest'},
            'attachments': ('django.db.models.fields.CharField', [], {'default': "u'[]'", 'max_length': '500', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'content_failure_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content_failure_comment': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_test_message': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_message_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'replay_to': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'request_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aio_client.RequestLog']"}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['aio_client']
