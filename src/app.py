import logging
from flask import Flask, request
from models.plate_reader import PlateReader
from io import BytesIO
import requests
from PIL import Image, UnidentifiedImageError


def read_number_by_id(model, image_id):
    try:
        # Формирование URL для получения изображения по его ID
        image_url = f"http://51.250.83.169:7878/images/{image_id}"
        # Запрос на получение изображения по URL
        response = requests.get(image_url)
    except ConnectionError:
        # Обработка ошибки, если не удалось подключиться к серверу с изображениями
        return {'error': 'failed to fetch image'}, 500

    try:
        # Получение данных изображения и открытие его с использованием библиотеки PIL
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        # Извлечение текста с изображения с помощью модели PlateReader
        gov_number = model.read_text(image)
    except UnidentifiedImageError:
        # Обработка ошибки, если формат изображения неподдерживаемый
        return {'error': 'invalid image format'}, 400

    return {image_id: gov_number}, 200


app = Flask(__name__)  # Создание объекта приложения Flask


# Настройка Flask для корректного отображения не ASCII символов в JSON
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    # Обработчик маршрута для корневого URL, который возвращает приветственное сообщение
    return '<h1><center>Hello!</center></h1>'


@app.route('/read-number')
def read_number():
    # Обработчик маршрута для чтения номера с одного изображения
    image_id = request.args.get('id')  # Получение ID изображения из запроса
    result = read_number_by_id(reader, image_id)  # Вызов функции для чтения номера
    return result  # Возврат результата


@app.route('/read-multiple-numbers')
def read_multiple_numbers():
    # Обработчик маршрута для чтения номеров с нескольких изображений
    image_id_list = request.args.getlist('id')  # Получение списка ID изображений из запроса
    response = {}
    for image_id in image_id_list:
        # Цикл для обработки каждого ID изображения
        model_response, status_code = read_number_by_id(reader, image_id)
        if status_code != 200:
            return model_response  # В случае ошибки возвращается сообщение об ошибке
        response[image_id] = model_response[image_id]  # Добавление результата в ответ
    return response  # Возврат ответа с результатами для всех изображений


if __name__ == '__main__':
    # Настройка журналирования
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    # Создание экземпляра модели PlateReader и загрузка весов из файла
    reader = PlateReader().load_from_file(
        "./model_weights/plate_reader_model.pth")

    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=8080, debug=True)
