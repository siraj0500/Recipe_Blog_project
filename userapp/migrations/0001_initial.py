# Generated by Django 4.0.4 on 2022-05-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=50)),
                ('sender_email', models.EmailField(max_length=70)),
                ('sender_message', models.TextField(max_length=500)),
            ],
        ),
    ]