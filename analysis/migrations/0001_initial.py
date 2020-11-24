<<<<<<< HEAD
# Generated by Django 3.1.3 on 2020-11-23 15:04
=======
# Generated by Django 3.1.3 on 2020-11-23 14:40
>>>>>>> main

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('movie', '0001_initial'),
        ('users', '__first__'),
=======
        ('users', '0003_auto_20201117_0725'),
        ('movie', '0005_auto_20201119_0608'),
>>>>>>> main
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='Star',
=======
            name='UserLog',
>>>>>>> main
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.DecimalField(decimal_places=1, max_digits=2)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
<<<<<<< HEAD
                'db_table': 'stars',
=======
                'db_table': 'user_logs',
>>>>>>> main
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('status', models.CharField(max_length=200)),
=======
                ('point', models.DecimalField(decimal_places=1, max_digits=2)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
>>>>>>> main
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'interests',
            },
        ),
    ]
