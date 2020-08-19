# Generated by Django 2.2.9 on 2020-08-17 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create_profile', '0001_initial'),
        ('photo', '0004_auto_20200818_0250'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo.Photo')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_profile.Profile')),
            ],
            options={
                'ordering': ['updated'],
            },
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
