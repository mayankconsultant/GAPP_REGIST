# Generated by Django 3.1.6 on 2021-02-11 18:28

import REGISTER.models
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='county',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='states',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='payam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='REGISTER.county')),
            ],
        ),
        migrations.CreateModel(
            name='CUSTOMER',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MOBILE_NUMBER', models.CharField(max_length=12)),
                ('FIRST_NAME', models.CharField(max_length=30)),
                ('SECOND_NAME', models.CharField(blank=True, max_length=30, null=True)),
                ('THIRD_NAME', models.CharField(blank=True, max_length=30, null=True)),
                ('LAST_NAME', models.CharField(max_length=30)),
                ('ID_TYPE', models.CharField(
                    choices=[('1', 'Work ID'), ('2', 'Student ID'), ('3', 'UN ID'), ('4', 'Military,Polica,SPLM'),
                             ('5', 'Tribal Chiefs Cert.'), ('6', 'National ID'), ('7', 'Passport'),
                             ('8', 'Voting Card'), ('9', 'Driving License')], max_length=30)),
                ('ID_NUMBER', models.CharField(max_length=15)),
                ('gender',
                 models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], default='MALE', max_length=10)),
                ('DOB', models.DateField(blank=True, null=True, verbose_name='Date Of Birth')),
                ('COUNTRY', django_countries.fields.CountryField(max_length=2)),
                ('ADDRESS', models.CharField(blank=True, max_length=50, null=True)),
                ('CITY', models.CharField(max_length=100)),
                ('BOMA', models.CharField(blank=True, max_length=50, null=True)),
                ('ID_PROOF',
                 models.ImageField(upload_to=REGISTER.models.customer_directory_path, verbose_name='ID PROOF FILE')),
                ('CREATED_DATE', models.DateField(auto_now_add=True)),
                ('COUNTY', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='REGISTER.county')),
                ('PAYAM', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='REGISTER.payam')),
                ('STATE', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='REGISTER.states')),
            ],
            options={
                'verbose_name': 'CUSTOMER',
                'verbose_name_plural': 'CUSTOMERS',
            },
        ),
        migrations.AddField(
            model_name='county',
            name='states',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='REGISTER.states'),
        ),
    ]
