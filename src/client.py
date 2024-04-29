import requests


class PlateReaderClient:
    def __init__(self, host):
        self.host = host  # Инициализация хоста, к которому будут отправляться запросы

    def read_number(self, image_id):
        # Метод для чтения номера с одного изображения
        print(f'Reading single number for image id: {image_id}')
        # Отправка GET-запроса для чтения номера
        response = requests.get(f'{self.host}/read-number?id={image_id}')
        return response.json()  # Возврат результата в формате JSON

    def read_multiple_numbers(self, image_id_list):
        # Метод для чтения номеров с нескольких изображений
        print("Reading several numbers...")
        # Отправка GET-запроса для чтения номеров
        response = requests.get(f'{self.host}/read-multiple-numbers', params={'id': image_id_list})
        return response.json()  # Возврат результата в формате JSON


if __name__ == "__main__":
    # Создание экземпляра клиента для чтения номеров с использованием локального хоста и порта 8080
    plate_reader_client = PlateReaderClient('http://0.0.0.0:8080')

    print("Testing reading single number:")
    valid_ids = [10022, 9967]
    
    # Тестирование метода для чтения номера с одного изображения
    print(f"Image ID: {valid_ids[0]}, Result: {plate_reader_client.read_number(valid_ids[0])}")

    print("Testing reading multiple numbers:")
    print(f"Image IDs: {valid_ids}, Result: {plate_reader_client.read_multiple_numbers(valid_ids)}")
