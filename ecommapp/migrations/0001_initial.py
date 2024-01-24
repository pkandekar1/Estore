# Generated by Django 5.0 on 2024-01-16 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('pdetails', models.CharField(max_length=50)),
                ('cat', models.IntegerField()),
                ('is_activate', models.BooleanField(default=True)),
            ],
        ),
    ]
