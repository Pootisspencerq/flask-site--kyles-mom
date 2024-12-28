from flask import Flask, render_template, request, flash
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()
from db import DatabaseManager
import os
app = Flask(__name__)  # Створюємо веб–додаток Flask
app.secret_key = os.getenv('SECRET_KEY')
db = DatabaseManager("data.db")

IMG_PATH = os.path.dirname(__file__) +os.sep + "static" +os.sep + "pic"+os.sep

@app.context_processor
def get_categories():
    categories = db.get_all_categories()
    return dict(categories=categories)

@app.route("/")  # Вказуємо url-адресу для виклику функції
def index():
    articles = db.get_all_articles()
    return render_template("index.html", articles=articles)

@app.route("/articles/<int:article_id>")  # Вказуємо url-адресу для виклику функції
def article_page(article_id):
    article = db.get_article(article_id)
    return render_template("article_page.html", article=article)

@app.route("/categories/<int:category_id>")  # Вказуємо url-адресу для виклику функції
def category_page(category_id):
    articles = db.get_category_articles(category_id)
    return render_template("index.html", articles=articles)  # html-сторінка, що повертається у браузер

@app.route("/new/articles>", methods = ['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        if request.form['category'] != 'Виберіть категорію':
            image = request.files['image'] #отримуємо файл картинки
            image.save(IMG_PATH + image.filename)
            db.add_acle(request.form['title'], request.form['content'],
                image.filename, request.form['category'])
        flash("Статтю додано")
    return render_template('new_article.html')
@app.route("/search")  # Вказуємо url-адресу для виклику функції
def search():
    if request.method == "GET":
        query = request.args.get("query")
        articles =db.search_article(query)


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # автоматичне оновлення шаблонів
    app.run(debug=True)  # Запускаємо веб-сервер з цього файлу в режимі налагодження
