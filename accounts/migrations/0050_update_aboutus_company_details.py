from django.db import migrations


def update_company_details(apps, schema_editor):
    """Rebrand: ASIASOURCE FINANCIAL INC. -> FILIPINO FUND, INC. (name, SEC
    number, founding date, and head office address). Matched by old content
    rather than fixed PKs, since these rows are seeded per-environment."""
    AboutUsSection = apps.get_model('accounts', 'AboutUsSection')

    for s in AboutUsSection.objects.filter(subtitle__icontains='ASIASOURCE'):
        s.subtitle = 'FILIPINO FUND, INC.'
        s.description = (
            'FILIPINO FUND, INC. (SEC No. 0000190385) is a reputable financial services '
            'provider that has been offering low-interest online loans since May 9, 1991. '
            'We provide comprehensive financial solutions for both individuals and '
            'businesses, with a strong emphasis on convenience and exceptional customer '
            'service.'
        )
        s.save(update_fields=['subtitle', 'description'])

    for s in AboutUsSection.objects.filter(description__icontains='IBP Tower'):
        s.subtitle = '12th Floor, PSE Tower, Fort Bonifacio'
        s.description = (
            'Visit us at our head office located at Units 1210-1212, 12th Floor, PSE '
            'Tower, 5th Avenue corner 28th Street, Fort Bonifacio, Taguig City, Fourth '
            'District, National Capital Region (NCR), 1630. Our team is ready to assist '
            'you.'
        )
        s.save(update_fields=['subtitle', 'description'])

    for s in AboutUsSection.objects.filter(subtitle__icontains='Since 2014'):
        s.subtitle = 'Trusted Since 1991'
        s.description = (
            'With over 30 years of experience, 50,000+ satisfied clients, and SEC '
            'registration, we are one of the most trusted online lending platforms in '
            'the Philippines. We offer loans from ₱80,000 to ₱5,000,000 with '
            'competitive low-interest rates and flexible repayment terms.'
        )
        s.save(update_fields=['subtitle', 'description'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_paymentmethod_account_name'),
    ]

    operations = [
        migrations.RunPython(update_company_details, migrations.RunPython.noop),
    ]
