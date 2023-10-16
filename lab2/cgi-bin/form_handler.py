import cgi
import html
import http.cookies
import os

def delete_cookies(cookie):
    for key in cookie.keys():
        cookie[key]['expires'] = 0
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
if "counter" in cookie:
    counter = int(cookie["counter"].value)
else:
    counter = 0

form = cgi.FieldStorage()
counter += 1

if "delete_cookies" in form:
    delete_cookies(cookie)
    counter = 0

username = form.getfirst("username", "Ms. Petey Fan")
location = form.getfirst("location", "")
song = form.getvalue("song", "Greatest Hits")
favorites = ["Lyrics", "Concerts", "Interviews", "Merchandise"]
favorites_checkbox = {}
for item in favorites:
    value_choice = form.getvalue(item, "off")
    favorites_checkbox[item] = value_choice

username = html.escape(username)
location = html.escape(location)

print(f"Set-cookie: counter={counter}")

print("Content-type: text/html\r\n\r\n")

escaped_cookie = html.escape(os.environ.get("HTTP_COOKIE", ""))

template_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ms. Petey Fan Page</title>
    
</head>
<body>
    <h1>Welcome to the Ms. Petey Fan Page!</h1>
    <h2>Page number (form number) {counter}</h2>
    <h3>Location: {location}</h3>
    <h3>Favorite Song: {song}</h3>
    <h3>Favorite Features: {favorites_checkbox}</h3>
    <h3>Escaped cookie: {escaped_cookie}</h3>
    <br><br>
    Explore more about Ms. Petey:
    <form action="form_handler.py" method="post">
        Tell us more about you:
        <br>
        Your Name: <input type="text" name="username">
        Your Location: <input type="text" name="location">
        <br>
        Choose your favorite Ms. Petey song:
        <select name="song">
            <option value="Greatest Hits">Greatest Hits</option>
            <option value="All About Love">All About Love</option>
            <option value="Memories">Memories</option>
        </select>
        <br>
        What's your favorite part about Ms. Petey?
        <br>
        <input type="checkbox" name="Lyrics" value="on"> Lyrics
        <input type="checkbox" name="Concerts" value="on"> Concerts
        <input type="checkbox" name="Interviews" value="on"> Interviews
        <input type="checkbox" name="Merchandise" value="on"> Merchandise
        <br>
        <input type="submit" value="Explore">
        <input type="submit" name="delete_cookies" value="Delete Cookies">
    </form>
</body>
</html>
"""

print(template_html)
