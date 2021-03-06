# Generated by Django 4.0.3 on 2022-03-20 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0004_player_player_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_number', models.CharField(max_length=50)),
                ('winner', models.CharField(max_length=50)),
                ('looser', models.CharField(max_length=50)),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matchteam1', to='cricket.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matchteam2', to='cricket.team')),
            ],
        ),
    ]
