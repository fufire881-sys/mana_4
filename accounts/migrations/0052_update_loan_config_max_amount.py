from decimal import Decimal
from django.db import migrations, models


def apply_new_max(apps, schema_editor):
    # Client-requested change: raise the maximum loan amount from
    # 2,000,000 to 5,000,000 (min stays 100,000). Same approach as
    # 0048/0051 — update the existing singleton row (or create it) so it
    # takes effect on deploy without a manual admin edit.
    LoanConfig = apps.get_model("accounts", "LoanConfig")
    cfg = LoanConfig.objects.first()
    if cfg:
        cfg.max_amount = Decimal("5000000.00")
        cfg.save(update_fields=["max_amount"])
    else:
        LoanConfig.objects.create(
            min_amount=Decimal("100000.00"),
            max_amount=Decimal("5000000.00"),
            interest_rate_monthly=Decimal("0.003000"),
        )

    # The "Why Choose Us" About Us copy quotes the loan range too — keep
    # it in sync with the real enforced limits.
    AboutUsSection = apps.get_model("accounts", "AboutUsSection")
    for s in AboutUsSection.objects.filter(description__icontains='₱100,000 to ₱2,000,000'):
        s.description = s.description.replace('₱100,000 to ₱2,000,000', '₱100,000 to ₱5,000,000')
        s.save(update_fields=['description'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0051_update_loan_config_rate_and_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanconfig',
            name='max_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('5000000.00'), max_digits=14),
        ),
        migrations.RunPython(apply_new_max, noop),
    ]
