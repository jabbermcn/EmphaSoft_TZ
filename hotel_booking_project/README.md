Проект "EmphaSoft_TZ"
Запуск с использованием Docker
Установите Docker Desktop.

Запустите Docker и выполните следующие команды в терминале:

bash
Copy code
docker-compose build
docker-compose up -d
Дождитесь завершения сборки проекта.

Перейдите на следующие страницы:

Swagger API Documentation
ReDoc API Documentation
Запуск локально
Клонируйте репозиторий:

bash
Copy code
git clone https://github.com/jabbermcn/EmphaSoft_TZ.git
Перейдите в корневую директорию проекта (hotel_booking_project).

Установите зависимости:

bash
Copy code
pip install -r requirements.txt
Замените файл с переменными окружения (ENV) на свои данные.

Создайте миграции:

bash
Copy code
python manage.py makemigrations
Примените миграции:

bash
Copy code
python manage.py migrate
Перейдите на следующие страницы:

Swagger API Documentation
ReDoc API Documentation
Примечание: Перед использованием убедитесь, что порт 8000 доступен и не занят другим процессом.