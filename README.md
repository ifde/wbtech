# WB-Tech Shop API

REST API интернет-магазина для тестового задания. Проект реализован на Django REST Framework с JWT, PostgreSQL, автогенерируемой документацией и Docker Compose.

## Возможности
- Регистрация, авторизация, профиль и баланс пользователя
- Каталог товаров (CRUD только для админов)
- Корзина (добавление, удаление, изменение количества)
- Создание заказа из корзины с проверкой баланса и остатков
- Логирование успешного заказа
- Документация OpenAPI через drf-spectacular

## Запуск через Docker Compose
1. Создайте файл .env (уже добавлен в репозиторий) при необходимости обновите значения.
2. Запустите контейнеры:

docker-compose up --build

API будет доступен по адресу http://localhost:8000

## Документация API
- OpenAPI schema: /api/schema/
- Swagger UI: /api/docs/

## Основные эндпоинты
- POST /api/users/register/
- GET /api/users/me/
- POST /api/users/balance/topup/
- POST /api/auth/token/
- POST /api/auth/token/refresh/
- GET /api/products/
- POST /api/cart/add/
- POST /api/cart/remove/
- POST /api/cart/update/
- POST /api/orders/

## Тесты
Запуск тестов внутри контейнера:

docker-compose exec web python manage.py test

## Логирование
Успешные заказы логируются в консоль через логгер orders.
