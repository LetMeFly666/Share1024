# Generated by Django 3.2 on 2022-10-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('cardID', models.IntegerField(default=1, primary_key=True, serialize=False, verbose_name='卡牌ID')),
                ('shareBy', models.CharField(max_length=20, verbose_name='被谁分享')),
                ('cardIs', models.CharField(max_length=4, verbose_name='卡牌是什么')),
                ('get1', models.IntegerField(default=0, verbose_name='第一次领取')),
                ('get2', models.IntegerField(default=0, verbose_name='第二次领取')),
                ('get3', models.IntegerField(default=0, verbose_name='第三次领取')),
                ('gotTimes', models.IntegerField(default=0, verbose_name='被领取了几次')),
                ('leetcodeURL', models.CharField(max_length=100, verbose_name='卡牌分享链接')),
            ],
        ),
        migrations.CreateModel(
            name='Got',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gotCardID', models.IntegerField(verbose_name='被领取卡牌ID')),
                ('gotBy', models.CharField(max_length=20, verbose_name='被谁领取')),
                ('shareCardID', models.IntegerField(default=0, verbose_name='传递的卡牌ID')),
                ('state', models.IntegerField(default=0, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='力扣id')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='邮箱')),
                ('shareNum', models.IntegerField(default=0, verbose_name='一共分享了多少卡牌')),
                ('cannotUseTimes', models.IntegerField(default=0, verbose_name='被反馈链接不能使用的次数')),
                ('lastGot', models.IntegerField(default=0, verbose_name='上次领取的卡牌ID')),
            ],
        ),
    ]
