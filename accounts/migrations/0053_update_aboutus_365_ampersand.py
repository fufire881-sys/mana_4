from django.db import migrations


def update_company_details(apps, schema_editor):
    """Rebrand: FILIPINO FUND, INC. -> 365 AMPERSAND CONNECT CORPORATION (name,
    SEC number, registration date, and head office address). Matched by old
    content rather than fixed PKs, since these rows are seeded per-environment."""
    AboutUsSection = apps.get_model('accounts', 'AboutUsSection')

    for s in AboutUsSection.objects.filter(subtitle__icontains='FILIPINO FUND'):
        s.subtitle = '365 AMPERSAND CONNECT CORPORATION'
        s.description = (
            '365 AMPERSAND CONNECT CORPORATION (SEC Reg. No. 2021110032200-04) is a '
            'registered financial services provider, registered with the SEC on '
            'November 11, 2021, offering low-interest online loans. We provide '
            'comprehensive financial solutions for both individuals and businesses, '
            'with a strong emphasis on convenience and exceptional customer service.'
        )
        s.save(update_fields=['subtitle', 'description'])

    for s in AboutUsSection.objects.filter(description__icontains='PSE Tower'):
        s.subtitle = 'Tabing Ilog, Marilao, Bulacan'
        s.description = (
            'Visit us at our head office located at Unit 3 No. 22, Cristobal Apartment '
            'Villarica, Tabing Ilog, Marilao, Bulacan, Region III (Central Luzon), 3019. '
            'Our team is ready to assist you.'
        )
        s.save(update_fields=['subtitle', 'description'])

    for s in AboutUsSection.objects.filter(subtitle__icontains='Since 1991'):
        s.subtitle = 'SEC Registered Since 2021'
        s.save(update_fields=['subtitle'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_update_loan_config_max_amount'),
    ]

    operations = [
        migrations.RunPython(update_company_details, migrations.RunPython.noop),
    ]
