from flask import Flask, request, send_file, send_from_directory
import os
import docx

app = Flask(__name__)

# HTML страницы для сайта
index_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Замена транслитеризации</title>
  </head>
  <body>
    <h1>Загрузите файл для замены букв</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".docx">
    <input type="submit" value="Upload">
    </form>
  </body>
</html>
"""

error__html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Error</title>
  </head>
  <body>
    <h1>Error: Файл не загружен</h1>
    <p>Пожалуйста загрузить файл</p>
    <a href="/">На главную страницу</a>
  </body>
</html>
"""

error_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Error</title>
  </head>
  <body>
    <h1>Error: Не верный формат файла</h1>
    <p>Пожалуйста загрузить файл с форматом .docx</p>
    <a href="/">На главную страницу</a>
  </body>
</html>
"""

# Словарь для замен символов
replace_dict = {
    'a': 'ф',
    'b': 'и',
    'c': 'с',
    'd': 'в',
    'e': 'у',
    'f': 'а',
    'g': 'п',
    'h': 'р',
    'i': 'ш',
    'j': 'о',
    'k': 'л',
    'l': 'д',
    'm': 'ь',
    'n': 'т',
    'o': 'щ',
    'p': 'з',
    'q': 'й',
    'r': 'к',
    's': 'ы',
    't': 'е',
    'u': 'г',
    'v': 'м',
    'w': 'ц',
    'x': 'ч',
    'y': 'н',
    'z': 'я',
    '{': 'Х',
    '}': 'Ъ',
    ':': 'Ж',
    '"': 'Э',
    '<': 'Б',
    '>': 'Ю',
    'A': 'Ф',
    'B': 'И',
    'C': 'С',
    'D': 'В',
    'E': 'У',
    'F': 'А',
    'G': 'П',
    'H': 'Р',
    'I': 'Ш',
    'J': 'О',
    'K': 'Л',
    'L': 'Д',
    'M': 'Ь',
    'N': 'Т',
    'O': 'Щ',
    'P': 'З',
    'Q': 'Й',
    'R': 'К',
    'S': 'Ы',
    'T': 'Е',
    'U': 'Г',
    'V': 'М',
    'W': 'Ц',
    'X': 'Ч',
    'Y': 'Н',
    'Z': 'Я',
    '[': 'х',
    ']': 'ъ',
    ';': 'ж',
    "'": 'э',
    ',': 'б',
    '.': 'ю',
    '?': ',',
}


@app.route("/")
def index():
    return index_html


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or file.filename == "":
        return error__html
    if not file.filename.endswith(".docx"):
        return error_html

    # Сохраняем загруженный файл на диске
    file.save(os.path.join(os.getcwd(), file.filename))

    # Открываем файл и заменяем символы
    document = docx.Document(file)
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            text = run.text
            for old, new in replace_dict.items():
                text = text.replace(old, new)
            run.text = text
    converted_filename = f"converted_{file.filename}"
    document.save(converted_filename)

    # Возвращаем пользователю файл
    return send_file(converted_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
