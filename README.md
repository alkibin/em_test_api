Описание задачи:
Необходимо разработать REST API с использованием FastAPI для управления библиотечным каталогом. API должно позволять работать с книгами, авторами и выдачей книг читателям.

Основные требования:
Создание структуры базы данных:

Использовать SQLAlchemy (2 версии) для взаимодействия с базой данных.
Спроектировать таблицы для следующих сущностей:
Author (Автор): id, имя, фамилия, дата рождения.
Book (Книга): id, название, описание, id автора, количество доступных экземпляров.
Borrow (Выдача): id, id книги, имя читателя, дата выдачи, дата возврата.
Реализация REST API:

Эндпоинты для авторов:
Создание автора (POST /authors).
Получение списка авторов (GET /authors).
Получение информации об авторе по id (GET /authors/{id}).
Обновление информации об авторе (PUT /authors/{id}).
Удаление автора (DELETE /authors/{id}).
Эндпоинты для книг:
Добавление книги (POST /books).
Получение списка книг (GET /books).
Получение информации о книге по id (GET /books/{id}).
Обновление информации о книге (PUT /books/{id}).
Удаление книги (DELETE /books/{id}).
Эндпоинты для выдач:
Создание записи о выдаче книги (POST /borrows).
Получение списка всех выдач (GET /borrows).
Получение информации о выдаче по id (GET /borrows/{id}).
Завершение выдачи (PATCH /borrows/{id}/return) с указанием даты возврата.
Бизнес-логика:

Проверять наличие доступных экземпляров книги при создании записи о выдаче.
Уменьшать количество доступных экземпляров книги при выдаче и увеличивать при возврате.
При попытке выдать недоступную книгу возвращать соответствующую ошибку.


Документация:
Использовать встроенную документацию FastAPI (Swagger/OpenAPI).
Дополнительные требования:

Тестирование:
Написать несколько тестов с использованием pytest для проверки работы основных функций API.


Docker:
Создать Dockerfile и docker-compose файл для запуска проекта вместе с базой данных (например, PostgreSQL).


Оценка:
Корректность структуры базы данных и её проектирование.
Чистота и логичность кода.
Уровень работы с FastAPI и SQLAlchemy.
Наличие и качество тестов (если реализовано).
Docker-конфигурация (если реализовано).
Структура проекта (использование паттернов проектирования).


Запустить проект через docker-compose.yml
- docker compose up -d
Запустить миграции 
- alembic upgrade head
Документация Сваггер доступна по адресу localhost:8000/api/openapi

Тесты запускаются из консолипри запущенной бд.
в паке tests/init_db.py нужно запустить скрипт для создания бд и запонения таблиц тестовыми данными.
