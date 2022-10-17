# Generated by Django 4.1.2 on 2022-10-17 23:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=200)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawn',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref_id', models.UUIDField(unique=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('withdrawn_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('SUCC', 'success'), ('FAIL', 'fail')], default='FAIL', max_length=4)),
                ('widthdrawn_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.user')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ENA', 'enabled'), ('DIS', 'disabled')], default='ENA', max_length=3)),
                ('enabled_at', models.DateTimeField(null=True)),
                ('disabled_at', models.DateTimeField(null=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.user')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref_id', models.UUIDField(unique=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('deposit_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('SUCC', 'success'), ('FAIL', 'fail')], default='FAIL', max_length=4)),
                ('deposit_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.user')),
            ],
        ),
    ]