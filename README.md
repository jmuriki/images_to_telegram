# Скачивание фотографий

Данный проект помогает автоматизировать процесс скачивания и публикации фотографий NASA и SpaceX в Telegram.


## Установка

Должен быть установлен python3.
Затем используйте pip (или pip3, если есть конфликт с python2) для установки зависимостей:

`pip install -r requirements.txt`

или

`pip3 install -r requirements.txt`

Рекомендуется использовать virtualenv / venv для изоляции проекта.


## Ключи и параметры

Сохраните ключи/токены/параметры в `.env` файл в директорию проекта в следующем формате:

`NASA_API_KEY=вместо этого текста вставьте ключ`

`TELEGRAM_TOKEN=вместо этого текста вставьте токен`

`CHAT_ID=@вместо этого текста вставьте имя канала`

`PUBLICATION_INTERVAL=вместо этого текста вставьте число`

`IMAGE_PATH=вместо этого текста вставьте путь с именем файла для следующей публикации`

Для получения API ключа NASA зарегистрируйтесь на https://api.nasa.gov .

Для получения токена Telegram, воспользуйтесь telegram ботом `@BotFather`.

В качестве chat_id используйте @имя вашего telegram канала.

Интервал публикаций задаётся в часах. По умолчанию установлен на 4 часа.

Путь с именем файла не является обязательным параметром.


## Запуск

`nasa_spacex_images_bot.py`

Находясь в директории проекта, откройте с помощью python3 файл `nasa_spacex_images_bot.py`


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков https://dvmn.org/.