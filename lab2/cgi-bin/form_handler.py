import cgi

print("Content-type: text/html\n")

form = cgi.FieldStorage()

# Витягуємо дані з форми
name = form.getvalue("name")
age = form.getvalue("age")

# Генеруємо HTML-сторінку з результатами
print(f"<html><body>")
print(f"<h1>Результати</h1>")
print(f"<p>Ім'я: {name}</p>")
print(f"<p>Вік: {age}</p>")
print(f"</body></html>")
