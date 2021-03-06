# Generated by Django 2.1.2 on 2019-10-30 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ontology', '0009_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quest', models.TextField()),
                ('Quest_Date', models.DateTimeField()),
                ('Reply', models.TextField(null=True)),
                ('Reply_Dtae', models.DateTimeField(null=True)),
                ('Farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ontology.Farmer')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ontology.Product')),
            ],
        ),
    ]
