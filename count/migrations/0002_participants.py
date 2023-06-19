# Generated by Django 4.2.1 on 2023-06-18 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.TextField(default='')),
                ('tricount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='count.counts')),
            ],
        ),
    ]
