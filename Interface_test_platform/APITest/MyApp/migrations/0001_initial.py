# Generated by Django 4.0.3 on 2022-04-07 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DB_tucao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30, null=True)),
                ('text', models.CharField(max_length=1000, null=True)),
                ('ctime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
