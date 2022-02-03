# Generated by Django 2.1.2 on 2019-10-29 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ontology', '0008_knowledgecenterservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Query', models.TextField()),
                ('Query_Date', models.DateField()),
                ('Reply', models.TextField(null=True)),
                ('Reply_Date', models.DateField(null=True)),
                ('Farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ontology.Farmer')),
            ],
        ),
    ]
