from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        "author": "JI",
        "title" : "Blog Post 1",
        "content" : "First Post Content",
        "date_posted": "August 26, 2019"
    },
    {
        "author": "JI",
        "title" : "Blog Post 2",
        "content" : "Second Post Content",
        "date_posted": "August 26, 2019"
    },
]


@app.route("/home")
def home():
    """
    posts의 데이터를 home.html에 전달해 렌더링
    """
    return render_template("home.html", posts=posts)


@app.route('/about')
def about():
    """
    about.html에 title을 건네줌
    """
    return render_template("about.html", title="about")