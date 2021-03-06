# Generated by Django 2.0.7 on 2018-08-24 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rh', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atualizacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PREENCHENDO', 'PREENCHENDO'), ('AGUARDANDO_VALIDACAO', 'AGUARDANDO VALIDAÇÃO'), ('RECUSADO', 'RECUSADO'), ('ACEITO', 'ACEITO')], max_length=50)),
                ('criacao_data', models.DateTimeField(auto_now_add=True)),
                ('envio_data', models.DateTimeField(auto_now_add=True)),
                ('pessoa_fisica', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rh.PessoaFisica')),
            ],
        ),
        migrations.CreateModel(
            name='Comprovante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.SmallIntegerField(choices=[(1, 'TÍTULO DE ELEITOR'), (2, 'CNH'), (3, 'CTPS'), (4, 'PIS/PASEP'), (5, 'NIS'), (7, 'IPSEP'), (8, 'INSS'), (9, 'RESERVISTA'), (10, 'CONSELHO PROFISSIONAL')], null=True)),
            ],
        ),
    ]
