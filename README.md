# Online Shop Project

Веб-приложение на Django для демонстрации работы интернет-магазина.

## Технологии
- **Python 3.14+**
- **Django 6.0**
- **Poetry** (управление зависимостями)
- **Bootstrap 5** (верстка)

## Как запустить проект локально

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com
   cd online-shop

2. **Установите зависимости через Poetry:**
   ```bash
   poetry install

3. **Активируйте окружение:**
   ```bash
   poetry env activate

4. **Запустите сервер:**
   ```bash
   python manage.py runserver

### Структура приложения

* **config/** — основные настройки проекта.
* **catalog/** — приложение с контроллерами страниц:
    * — Главная страница (`home`).
    * — Страница обратной связи (`contacts`).
* **static/** — CSS стили (Bootstrap) и скрипты JavaScripts.
* **templates/** — HTML-шаблоны страниц.
