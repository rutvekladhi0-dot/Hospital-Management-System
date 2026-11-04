from django.core.management.base import BaseCommand
from accounts.models import Role, User


class Command(BaseCommand):
    help = 'Fix duplicate lowercase role entries and reassign users'

    def handle(self, *args, **options):
        duplicates = Role.objects.all()
        roles_list = list(duplicates.values_list('name', flat=True))
        self.stdout.write(f'All roles: {roles_list}')

        canonical_map = {}
        for r in duplicates:
            lower = r.name.lower()
            if lower not in canonical_map:
                canonical_map[lower] = r

        for lower, canonical in canonical_map.items():
            duplicates_with_same_lower = Role.objects.filter(name__iexact=canonical.name)
            for dup in duplicates_with_same_lower:
                if dup.id != canonical.id:
                    for user in dup.users.all():
                        user.roles.remove(dup)
                        user.roles.add(canonical)
                        self.stdout.write(f'  Moved {user.username} from "{dup.name}" to "{canonical.name}"')
                    dup.delete()
                    self.stdout.write(self.style.WARNING(f'  Deleted duplicate role "{dup.name}" (kept "{canonical.name}")'))

        self.stdout.write(self.style.SUCCESS('Done! Roles cleaned up.'))
