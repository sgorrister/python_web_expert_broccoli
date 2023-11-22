import cgi
import http.cookies

# Вказуємо, що вміст відповіді буде у форматі HTML
print("Content-type: text/html\n")

# Отримуємо дані з форми
form = cgi.FieldStorage()
name = form.getvalue("name")
age = form.getvalue("age")

# Створюємо об'єкт для роботи з cookies
cookie = http.cookies.SimpleCookie()

# Отримуємо значення кукісів, якщо вони існують
if "visit_count" in cookie:
    visit_count = int(cookie["visit_count"].value) + 1
else:
    visit_count = 1

# Встановлюємо нове значення кукісу "visit_count"
cookie["visit_count"] = str(visit_count)

# Встановлюємо тривалість кукісу в секундах (наприклад, 1 година)
cookie["visit_count"]["max-age"] = 3600

# Виводимо заголовки для встановлення кукісів
print(cookie.output())

# Виводимо HTML-сторінку з результатами та кнопкою для видалення кукісів
print('<html><body>')
print('<h1>Результати</h1>')
print(f'<p>Ім\'я: {name}</p>')
print(f'<p>Вік: {age}</p>')
print(f'<p>Кількість відвідувань: {visit_count}</p>')

# Додамо кнопку для видалення кукісів
print('<form action="/cgi-bin/form_handler.py" method="post">')
print('<input type="submit" name="delete_cookies" value="Видалити cookies">')
print('</form>')

print('</body></html>')
