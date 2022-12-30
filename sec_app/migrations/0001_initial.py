# Generated by Django 4.1.3 on 2022-12-17 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('advisoryID', models.IntegerField(default=0)),
                ('severity', models.CharField(max_length=15)),
                ('solution', models.CharField(max_length=1000)),
                ('cvs_tempscore', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='VulnerabilityData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_id', models.IntegerField(default=0)),
                ('vulnerabilityID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sec_app.vulnerability')),
            ],
        ),
    ]
