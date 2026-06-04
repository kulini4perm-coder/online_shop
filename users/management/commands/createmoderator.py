from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from catalog.models import Product


class Command(BaseCommand):
    ''' Создание группы Модератор продуктов '''

    def handle(self, *args, **options):
        moderator, created = Group.objects.get_or_create(name='Модератор продуктов')
        content_type = ContentType.objects.get_for_model(Product)

        try:
            unpublish_perm = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
            delete_perm = Permission.objects.get(codename='delete_product', content_type=content_type)

            moderator.permissions.set([unpublish_perm, delete_perm])

            if created:
                self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана и настроена!'))
            else:
                self.stdout.write(self.style.SUCCESS('Права группы "Модератор продуктов" успешно обновлены!'))

        except ObjectDoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: Сначала примените миграции! Право не найдено. {e}'))
