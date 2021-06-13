import datetime
from flask import Flask, request

app = Flask(__name__)

# I would use a db like mongo here instead of a global list in a production environment
LIST_OF_ITEMS = []


class Item:
    def __init__(self, id, file_name, media_type, created_at, updated_at):
        self.id = id
        self.file_name = file_name
        self.media_type = media_type
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return str({
            'id': self.id,
            'file_name': self.file_name,
            'media_type': self.media_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })


@app.route('/items/create', methods=['GET'])
def create_item():
    """
    curl -X GET localhost:5000/items/create -d file_name=hello_world1 -d media_type=python
    :return: Item created.
    {
        'id': 1, 'file_name': 'hello_world1', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 24, 39, 878028), 'updated_at': datetime.datetime(2021, 6, 2, 12, 24, 39, 878037)
    }
    """
    try:
        new_item = Item(
            id=len(LIST_OF_ITEMS) + 1,
            file_name=request.form['file_name'],
            media_type=request.form['media_type'],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
    except KeyError:
        return 'Bad values'
    LIST_OF_ITEMS.append(new_item)
    return f'Item created.\n{LIST_OF_ITEMS[new_item.id-1]}'


@app.route('/items/', methods=['GET'])
def all_items():
    """
     curl http://localhost:5000/items/
    :return:
    [
        {
            'id': 1, 'file_name': 'new_world', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 36, 40, 797705), 'updated_at': datetime.datetime(2021, 6, 2, 12, 37, 57, 265567)
        },
        {
            'id': 2, 'file_name': 'hello_world1', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 36, 48, 47741), 'updated_at': datetime.datetime(2021, 6, 2, 12, 36, 48, 47747)
        },
        {
            'id': 3, 'file_name': 'hello_world2', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 36, 54, 63698), 'updated_at': datetime.datetime(2021, 6, 2, 12, 36, 54, 63705)
        }
    ]
    """
    return str(LIST_OF_ITEMS)


@app.route('/items/<int:id>/', methods=['GET'])
def find_item(id):
    """
    curl http://localhost:5000/items/1/
    :param id: id to find
    :return:
    {
        'id': 1, 'file_name': 'new_world', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 36, 40, 797705), 'updated_at': datetime.datetime(2021, 6, 2, 12, 37, 57, 265567)
    }
    """
    if id < 1:
        return 'Id does not exist.'
    try:
        return str(LIST_OF_ITEMS[id-1])
    except IndexError:
        return 'Id does not exist.'


@app.route('/items/delete/<int:id>/', methods=['GET'])
def delete_item(id):
    """
    curl http://localhost:5000/items/delete/1/
    :param id: id to delete
    :return:
    Item removed from list.
    {
        'id': 1, 'file_name': 'new_world', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 36, 40, 797705), 'updated_at': datetime.datetime(2021, 6, 2, 12, 37, 57, 265567)
    }
    """
    if id < 1:
        return 'Id does not exist.'
    try:
        return f'Item removed from list.\n{LIST_OF_ITEMS.pop(id-1)}'
    except IndexError:
        return 'Id does not exist.'


@app.route('/items/update/<int:id>/', methods=['GET'])
def update_item(id):
    """
    curl -X GET localhost:5000/items/update/1/ -d file_name=new_world
    :param id: id to update
    :return:
    Item updated.
    {
        'id': 1, 'file_name': 'new_world', 'media_type': 'python', 'created_at': datetime.datetime(2021, 6, 2, 12, 36, 40, 797705), 'updated_at': datetime.datetime(2021, 6, 2, 12, 37, 57, 265567)
    }
    """
    if id < 1:
        return 'Id does not exist.'
    try:
        item_to_update = LIST_OF_ITEMS[id-1]
    except IndexError:
        return 'Id does not exist.'
    try:
        item_to_update.file_name = request.form['file_name']
        item_to_update.updated_at = datetime.datetime.now()
        LIST_OF_ITEMS[id-1] = item_to_update
    except KeyError:
        return 'New file name not provided.'
    return f'Item updated.\n{str(LIST_OF_ITEMS[id-1])}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
