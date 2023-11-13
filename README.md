# Foodgram

**Foodgram** - это веб-приложение для любителей еды, которое позволяет создавать, делиться и открывать свои любимые рецепты. С Foodgram вы можете зарегистрироваться, создавать и публиковать свои собственные рецепты, а также находить и добавлять рецепты других пользователей в закладки. Вы также можете подписываться на авторов рецептов, чтобы быть в курсе их новых кулинарных шедевров.


## Описание проекта  
 - Бекенд приложения написан на языке [Django](https://www.djangoproject.com).
 - API реализована с использованием [Django REST Framework](https://www.django-rest-framework.org).
 - Для основных действий по аутентификации используется библиотека [djoser](https://github.com/sunscrapers/djoser).

 - Фронтенд - одностраничное приложение на языке JavaScript с использованием библиотеки [React](https://ru.reactjs.org/), которое взаимодействует с API через удобный пользовательский интерфейс.


## Технологии и инструменты:

- Django
- Django REST framework
- PostgreSQL
- Docker
- Gunicorn
- Nginx
- Git и GitHub
- React


## Основные функции:

### 1. Регистрация и аутентификация

- Пользователи могут зарегистрироваться, создав учетную запись с уникальным именем пользователя и адресом электронной почты.

### 2. Создание и публикация рецептов

- Пользователи могут создавать и редактировать свои собственные рецепты, включая заголовок, описание, изображение, список ингредиентов и  тегов.

### 3. Поиск рецептов

- Все пользователи могут просматривать рецепты, созданные другими пользователями.

### 4. Избранное

- Пользователи могут добавлять рецепты в свой список избранных, чтобы сохранить свои любимые рецепты для будущего доступа.

### 5. Подписки

- Пользователи могут подписываться на авторов рецептов.

### 6. Корзина покупок

- Пользователи могут добавлять рецепты в свою корзину покупок и могут скачивать список покупок с суммированным количеством ингредиентов для всех рецептов в корзине.

Foodgram создан для обмена кулинарными идеями и вдохновением среди любителей еды. Мы надеемся, что вы найдете здесь много вкусных рецептов и интересных блюд!


## Запуск проекта

Клонировать репозиторий и перейти в директорию `infra/`:
```bash
git git@github.com:JacobKleim/foodgram-project-react.git
```
```bash
cd foodgram-project-react/infra
```

Создайте в директории infra .env файл с параметрами:
```
    DB_ENGINE=django.db.backends.postgresql  # указываем, что работаем с postgresql 
    DB_NAME=postgres  # имя базы данных 
    POSTGRES_USER=postgres  # логин для подключения к базе данных 
    POSTGRES_PASSWORD=postgres  # пароль для подключения к БД (установите свой)
    DB_HOST=db  # название сервиса (контейнера) 
    DB_PORT=5432  # порт для подключения к БД
    
    ALLOWED_HOSTS=localhost #Ваши хосты
    SECRET_KEY=KEY # ваш ключ
```

Установите и настройте [Doсker](https://www.docker.com/products/docker-desktop/), если у вас его нет.

◾ Запустите docker-compose:
```
docker-compose up -d --build
```
В соберите файлы статики, и запустите миграции командами:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

◾ Создать суперпользователя можно командой:
```
docker-compose exec web python manage.py createsuperuser
```
◾ Остановить:
```
docker-compose down -v
```

## Автор

Автор: Клейменов Яков

Электронная почта: yakovkleimenov@yandex.ru

GitHub: https://github.com/JacobKleim


