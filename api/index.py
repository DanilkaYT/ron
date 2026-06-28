import base64
from urllib.request import urlopen
from urllib.error import URLError
from flask import Flask, Response

app = Flask(__name__)

# Заранее заданная ссылка на исходный файл (Base64)
SOURCE_URL = "https://subrostunnel.vercel.app/gen.txt"

@app.route('/', methods=['GET'])
def process_file():
    try:
        # 1. Скачиваем содержимое как байты
        with urlopen(SOURCE_URL) as response:
            raw_data = response.read()
    except URLError as e:
        return f"Ошибка загрузки: {e}", 500
    except Exception as e:
        return f"Неизвестная ошибка: {e}", 500

    # 2. Декодируем Base64
    try:
        decoded_bytes = base64.b64decode(raw_data)
        # Предполагаем UTF-8; при необходимости замените на 'cp1251'
        decoded_text = decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"Ошибка декодирования Base64: {e}", 500

    # 3. Обрабатываем строки
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

    # 4. Возвращаем как текстовый файл для скачивания
    return Response(
        result_text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=result.txt"}
    )

# Для локального тестирования (необязательно)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)