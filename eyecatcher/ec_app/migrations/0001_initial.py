# Generated by Django 4.2.3 on 2023-07-10 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('properties', models.JSONField()),
                ('secret', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('click_data', models.JSONField()),
                ('image', models.FileField(upload_to='')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reports', to='ec_app.system')),
            ],
        ),
    ]
