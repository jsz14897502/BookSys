# Generated by Django 2.0.2 on 2018-07-23 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LibrarySys', '0004_auto_20180722_0015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='requster',
            new_name='requester',
        ),
        migrations.AlterField(
            model_name='book_list',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.User'),
        ),
        migrations.AlterField(
            model_name='book_short_comment',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.Book_list'),
        ),
        migrations.AlterField(
            model_name='book_short_comment',
            name='commentator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.User'),
        ),
        migrations.AlterField(
            model_name='book_short_comment_like_and_collection_record',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.User'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='book_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.Book_list'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='previous',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.User'),
        ),
        migrations.AlterField(
            model_name='login_record',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.User'),
        ),
        migrations.AlterField(
            model_name='request',
            name='book_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.Book_list'),
        ),
        migrations.AlterField(
            model_name='request',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='LibrarySys.User'),
        ),
    ]
