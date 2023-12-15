# EmphaSoft_TZ Application

## Запуск с использованием Docker

Развертывание приложения с использованием Docker обеспечивает простоту и портативность. Следуйте шагам ниже:

1. Установите [Docker Desktop](https://www.docker.com/products/docker-desktop).

2. Запустите Docker и выполните следующие команды в терминале:

    ```bash
    docker-compose build
    docker-compose up -d
    ```

3. Дождитесь успешного завершения сборки проекта.

![Пример успешного запуска контейнеров](https://i.postimg.cc/Njx1Cc10/2023-12-14-21-24-45.png)
[![2023-12-14-21-24-45.png](https://i.postimg.cc/Njx1Cc10/2023-12-14-21-24-45.png)](https://postimg.cc/zyVb342m)

4. Перейдите по следующим ссылкам:
    - [Swagger API Documentation](http://127.0.0.1:8000/swagger/)
    - [ReDoc API Documentation](http://127.0.0.1:8000/redoc/)

## Запуск локально

Для запуска приложения локально, выполните следующие шаги:

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/jabbermcn/EmphaSoft_TZ.git
    ```

2. Перейдите в корневую директорию проекта (`hotel_booking_project`).

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Замените файл с переменными окружения (ENV) на свои данные.

5. Создайте миграции:

    ```bash
    python manage.py makemigrations
    ```

6. Примените миграции:

    ```bash
    python manage.py migrate
    ```

7. Посетите следующие страницы:
    - [Swagger API Documentation](http://127.0.0.1:8000/swagger/)
    - [ReDoc API Documentation](http://127.0.0.1:8000/redoc/)

**Примечание:** Перед использованием убедитесь, что порт 8000 доступен и не занят другим процессом.
