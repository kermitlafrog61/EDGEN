# Generated by Django 4.2 on 2023-04-27 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('approved', models.BooleanField(default=False)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Универ',
                'verbose_name_plural': 'Универы',
            },
        ),
    ]