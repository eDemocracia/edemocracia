# Generated by Django 2.2.10 on 2021-04-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewUsersReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('new_users', models.IntegerField(blank=True, default=0, null=True, verbose_name='new users')),
            ],
            options={
                'verbose_name': 'new user',
                'verbose_name_plural': 'new users',
                'unique_together': {('start_date', 'period')},
            },
        ),
    ]
