# Generated by Django 2.1.2 on 2019-10-29 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontology', '0007_dealernotification_knowledgecenternotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeCenterService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Service', models.TextField()),
            ],
        ),
    ]
