# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_aboutussection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('processing', 'Processing'),
                    ('waiting', 'Waiting for approval'),
                    ('reviewed', 'Reviewed'),
                    ('paid', 'Payment sent'),
                    ('rejected', 'Rejected'),
                    ('withdrawal_fail', 'Withdrawal Fail'),
                ],
                default='processing',
                max_length=20,
            ),
        ),
    ]
