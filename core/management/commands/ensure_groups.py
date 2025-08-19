from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = """Creates 'Landlord' and 'Renter' groups and
    associates them with base permissions if they do not exist."""

    def handle(self, *args, **options):
        groups_permissions = {
            "Renter": [14, 16, 28],
            "Landlord": [14, 16, 25, 26, 27, 28],
        }

        existing_groups = set(Group.objects.filter(name__in=groups_permissions.keys())
                              .values_list('name', flat=True))

        if existing_groups == set(groups_permissions.keys()):
            self.stdout.write("All groups already exist, the database will not be filled again.")
            return

        for group_name, perm_ids in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Group {group_name} created")
            else:
                self.stdout.write(f"Group {group_name} is already exists")

            permissions = Permission.objects.filter(id__in=perm_ids)
            group.permissions.add(*permissions)
