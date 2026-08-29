# Generated manually (interactive makemigrations prompt can't run
# non-interactively) — adds period_month/period_year to
# FastestGrowingMarket, mirroring Agent's existing period fields, and
# swaps the global unique=True on rank for a per-period
# unique_together, matching Agent's constraint.
#
# Existing rows get backfilled with period_month=6, period_year=2026
# to match the Agent fixture rows' period, so the demo dataset stays
# internally consistent ("this month's" data).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_agent_source_name_agent_source_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fastestgrowingmarket',
            name='period_month',
            field=models.PositiveSmallIntegerField(default=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fastestgrowingmarket',
            name='period_year',
            field=models.PositiveSmallIntegerField(default=2026),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fastestgrowingmarket',
            name='rank',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='fastestgrowingmarket',
            unique_together={('rank', 'period_month', 'period_year')},
        ),
    ]
