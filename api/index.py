import base64
from urllib.request import urlopen
from urllib.error import URLError
from flask import Flask, Response

app = Flask(__name__)

# Ссылка на ваш исходный файл (с Base64)
SOURCE_URL = "https://subrostunnel.vercel.app/gen.txt"

def process_data():
    """
    Загружает, декодирует Base64, фильтрует строки с LTE,
    заменяет wlrus, нумерует, добавляет флаг и бота.
    Возвращает (текст_результата, сообщение_об_ошибке, статус_код)
    """
    try:
        with urlopen(SOURCE_URL) as response:
            raw_data = response.read()
    except URLError as e:
        return None, f"Ошибка загрузки: {e}", 500
    except Exception as e:
        return None, f"Неизвестная ошибка: {e}", 500

    try:
        decoded_bytes = base64.b64decode(raw_data)
        # Если нужна другая кодировка, замените 'utf-8' на 'cp1251' и т.п.
        decoded_text = decoded_bytes.decode('utf-8')
    except Exception as e:
        return None, f"Ошибка декодирования Base64: {e}", 500

    lines = decoded_text.splitlines()
    result_lines = []
    counter = 1

    for line in lines:
        if "LTE" in line.upper():
            new_line = line.replace("wlrus", "fastflash-test")
            # Удаляем всё, что после '#'
            if '#' in new_line:
                new_line = new_line.split('#', 1)[0].rstrip()
            new_line += f" #🇩🇪{counter} @fastflashvpnbot"
            result_lines.append(new_line)
            counter += 1

    result_text = "\n".join(result_lines)
    return result_text, None, 200

# Главный маршрут – отображает результат как обычный текст
@app.route('/', methods=['GET'])
def index():
    result, error, status = process_data()
    if error:
        return error, status
    return Response(result, mimetype="text/plain")

# Дополнительный маршрут /result.txt – тоже отображает текст
@app.route('/result.txt', methods=['GET'])
def result_txt():
    return index()  # просто вызываем ту же логику

# Для локального тестирования (не обязательно)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
