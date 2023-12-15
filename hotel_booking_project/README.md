Запуск(docker)
Реализовано развертывание приложения с помощью докера, для этого небходимо установить docker desktop и запустить его.
После запуска докера прописать
docker-compose build

Дождаться билда проекта и прописать
docker-compose up -d

Перейти на страницу
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/

Запуск (локально)
Клонировать репозиторий https://github.com/jabbermcn/EmphaSoft_TZ.git
Из корневой директории (hotel_booking_project) установить зависимости
pip install -r requirements.txt

Поменять ENV файл на свои данные

Создать миграции
python manage.py makemigrations

Мигрировать
python manage.py migrate

Перейти на страницу
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/