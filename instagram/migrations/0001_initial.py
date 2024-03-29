# Generated by Django 2.2.3 on 2019-08-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('dob', models.DateField()),
                ('password', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_image')),
            ],
        ),
    ]
