from django.db import migrations


def remove_years_claim(apps, schema_editor):
    """The company was SEC-registered on November 11, 2021, so the old
    "over 30 years of experience" claim no longer holds."""
    AboutUsSection = apps.get_model('accounts', 'AboutUsSection')

    for s in AboutUsSection.objects.filter(description__icontains='30 years of experience'):
        s.description = s.description.replace(
            'With over 30 years of experience, 50,000+ satisfied clients, and SEC registration,',
            'With 50,000+ satisfied clients and SEC registration,',
        )
        s.save(update_fields=['description'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0053_update_aboutus_365_ampersand'),
    ]

    operations = [
        migrations.RunPython(remove_years_claim, migrations.RunPython.noop),
    ]
