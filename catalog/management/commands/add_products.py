from django.core.management import BaseCommand, call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Очищает базу данных и загружает данные из фикстуры'

    def handle(self, *args, **options):
        # Удаляем все продукты
        Product.objects.all().delete()
        # Удаляем все категории
        Category.objects.all().delete()

        # Загружаем данные из фикстуры
        try:
            call_command('loaddata', 'catalog_fixture.json')
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены из фикстуры!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {e}'))
