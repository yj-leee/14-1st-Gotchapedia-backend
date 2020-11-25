# Generated by Django 3.1.3 on 2020-11-25 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('main_image', models.URLField(max_length=1000)),
                ('description', models.TextField(null=True)),
                ('opening_at', models.DateField()),
                ('show_time', models.IntegerField()),
            ],
            options={
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='MovieStaffPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
            options={
                'db_table': 'movie_staff_positions',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('proflie_image', models.URLField(max_length=1000)),
                ('movie', models.ManyToManyField(through='movie.MovieStaffPosition', to='movie.Movie')),
            ],
            options={
                'db_table': 'staff',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=1000)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
            options={
                'db_table': 'pictures',
            },
        ),
        migrations.AddField(
            model_name='moviestaffposition',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.position'),
        ),
        migrations.AddField(
            model_name='moviestaffposition',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.staff'),
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
            options={
                'db_table': 'movie_genre',
            },
        ),
        migrations.AddField(
            model_name='genre',
            name='movie',
            field=models.ManyToManyField(through='movie.MovieGenre', to='movie.Movie'),
        ),
    ]
