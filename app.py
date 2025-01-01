from flask import Flask, render_template, request, flash, url_for
from dotenv import load_dotenv
from db import DatabaseManager
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
db = DatabaseManager("data.db")

IMG_PATH = os.path.join(os.path.dirname(__file__), "static", "pic")

@app.context_processor
def get_categories():
    categories = db.get_all_categories()
    return dict(categories=categories)

@app.route("/")
def index():
    articles = db.get_all_articles()
    return render_template("index.html", articles=articles)

@app.route("/articles/<int:article_id>")
def article_page(article_id):
    article = db.get_article(article_id)
    return render_template("article_page.html", article=article)

@app.route("/categories/<int:category_id>")
def category_page(category_id):
    articles = db.get_category_articles(category_id)
    return render_template("index.html", articles=articles)

@app.route("/new/articles", methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        if request.form['category'] != 'Виберіть категорію':
            image = request.files['image']
            image.save(os.path.join(IMG_PATH, image.filename))
            db.add_article(
                request.form['title'],
                request.form['content'],
                image.filename,
                1,  # Assuming a user ID of 1 for simplicity
                request.form['category']
            )
            flash("Статтю додано", "success")
        else:
            flash("Виберіть категорію", "warning")
    return render_template("new_article.html")

@app.route("/search")
def search():
    query = request.args.get("query", "")
    articles = db.search_article(query)
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
