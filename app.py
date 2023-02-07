from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


def get_item(item_id):
    connection = get_db_connection()
    current_item = connection.execute('select * from items where id = ?', (item_id,)).fetchone()
    connection.close()

    if current_item is None:
        abort(404)
    return current_item


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'


@app.route('/')
def index():
    connection = get_db_connection()
    items = connection.execute('select * from items').fetchall()
    connection.close()
    return render_template("index.html", items=items)


@app.route('/<int:item_id>')
def item(item_id):
    current_item = get_item(item_id)
    return render_template('item.html', item=current_item)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('insert into items (title, description) values (?, ?)', (title, description))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:item_id>/edit', methods=('GET', 'POST'))
def edit(item_id):
    current_item = get_item(item_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('update items set title = ?, description = ? where id = ?',
                               (title, description, item_id))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('edit.html', item=current_item)


@app.route('/<int:item_id>/delete', methods=('POST',))
def delete(item_id):
    current_item = get_item(item_id)
    connection = get_db_connection()
    connection.execute('delete from items where id = ?', (item_id,))
    connection.commit()
    connection.close()
    flash(f"{current_item['title']} was successfully deleted!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()



