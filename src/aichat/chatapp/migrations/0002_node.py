# Generated by Django 2.0.5 on 2018-05-25 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('x_loc', models.IntegerField(default=0)),
                ('y_loc', models.IntegerField(default=0)),
            ],
        ),
    ]
