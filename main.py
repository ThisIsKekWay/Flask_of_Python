from flask import Flask, render_template

app = Flask(__name__)

cats = [
    {"title": "Одежда", "func_name": 'clothes'},
    {"title": "Шляпки", "func_name": 'hats'},
    {"title": "Обувь", "func_name": 'shoes'},
]


@app.route('/')
@app.route('/index/')
def index ():
    return render_template('store_index.html', category=cats)


@app.route('/info/')
def info ():
    return render_template('store_info.html')


@app.route('/contacts/')
def contacts ():
    return render_template('store_contacts.html')


@app.route('/clothes/')
def clothes ():
    return render_template('store_clothes.html')


@app.route('/shoes/')
def shoes ():
    return render_template('store_shoes.html')


@app.route('/hats/')
def hats ():
    return render_template('store_hats.html')


if __name__ == "__main__":
    app.run(debug=True)
