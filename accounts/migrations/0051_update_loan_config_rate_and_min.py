from decimal import Decimal
from django.db import migrations, models


def apply_new_config(apps, schema_editor):
    # Client-requested change: loans now start at 100,000 (was 75,000) with
    # a 0.3% monthly rate (was 0.5%). Update the existing singleton row (or
    # create it) so this takes effect immediately without a manual admin
    # edit in production — same approach as 0048_update_loan_config_amounts.
    LoanConfig = apps.get_model("accounts", "LoanConfig")
    cfg = LoanConfig.objects.first()
    if cfg:
        cfg.min_amount = Decimal("100000.00")
        cfg.interest_rate_monthly = Decimal("0.003000")
        cfg.save(update_fields=["min_amount", "interest_rate_monthly"])
    else:
        LoanConfig.objects.create(
            min_amount=Decimal("100000.00"),
            max_amount=Decimal("2000000.00"),
            interest_rate_monthly=Decimal("0.003000"),
        )

    # The "Why Choose Us" About Us copy quoted a loan range (₱80,000 to
    # ₱5,000,000) that never matched the actual enforced min/max — fix it
    # to the real range while we're already updating loan numbers here.
    AboutUsSection = apps.get_model("accounts", "AboutUsSection")
    for s in AboutUsSection.objects.filter(description__icontains='₱80,000 to ₱5,000,000'):
        s.description = s.description.replace('₱80,000 to ₱5,000,000', '₱100,000 to ₱2,000,000')
        s.save(update_fields=['description'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0050_update_aboutus_company_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanconfig',
            name='interest_rate_monthly',
            field=models.DecimalField(decimal_places=6, default=Decimal('0.003000'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='loanconfig',
            name='min_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('100000.00'), max_digits=14),
        ),
        migrations.RunPython(apply_new_config, noop),
    ]
