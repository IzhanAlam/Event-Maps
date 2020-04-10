# Generated by Django 3.0.5 on 2020-04-10 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='geo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson_object', models.TextField()),
                ('feature', models.TextField(null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('recent', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='geo2hrs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson_object', models.TextField()),
                ('feature', models.TextField(null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('recent', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='geo30min',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson_object', models.TextField()),
                ('feature', models.TextField(null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('recent', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='geo6hrs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson_object', models.TextField()),
                ('feature', models.TextField(null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('recent', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='privateComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(null=True)),
                ('pub_date', models.DateTimeField(null=True, verbose_name='date published')),
                ('instance', models.IntegerField()),
                ('author', models.CharField(max_length=280, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='userEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=30)),
                ('longitude', models.CharField(max_length=30)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('title', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=280)),
                ('time', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='geoprivate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson_object', models.TextField()),
                ('feature', models.TextField(null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('recent', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='eventInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('event_comments', models.TextField(null=True)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('time', models.IntegerField(default=0)),
                ('popup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='default.userEvent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]