# Generated by Django 3.2.16 on 2023-02-01 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('follow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='accounts.user'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='accounts.user'),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_from_user', to='accounts.user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_to_user', to='accounts.user')),
            ],
            options={
                'db_table': 'block',
            },
        ),
    ]
