# Generated by Django 4.0.3 on 2022-05-29 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_rename_phone_deletedcontacts_phone1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='user',
        ),
        migrations.DeleteModel(
            name='DeletedContacts',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
