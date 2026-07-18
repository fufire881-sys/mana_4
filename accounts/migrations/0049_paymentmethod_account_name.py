from django.db import migrations, models


def move_old_bank_name_to_account_name(apps, schema_editor):
    """Old frontend saved the account holder's name into bank_name (it was
    mislabeled "Account Name" in the UI). Move that value into the new
    account_name field so existing data lands under the right label, and
    clear bank_name so it can hold a real bank name going forward."""
    PaymentMethod = apps.get_model('accounts', 'PaymentMethod')
    for pm in PaymentMethod.objects.exclude(bank_name=""):
        pm.account_name = pm.bank_name
        pm.bank_name = ""
        pm.save(update_fields=["account_name", "bank_name"])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0048_update_loan_config_amounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='account_name',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.RunPython(move_old_bank_name_to_account_name, migrations.RunPython.noop),
    ]
