from flask import Flask, render_template, request, jsonify
import uuid
import os

app = Flask(__name__)

class MagicalInventory:
    def __init__(self):
        self.items = []

    def add_item(self, description):
        item = {
            'id': str(uuid.uuid4()),
            'description': description
        }
        self.items.append(item)
        return "Item adicionado com sucesso."

    def remove_item(self, item_id):
        for item in self.items:
            if item['id'] == item_id:
                self.items.remove(item)
                return "Item removido com sucesso."
        return "Item não encontrado no inventário."

    def list_items(self):
        if not self.items:
            return "Inventário vazio."
        return self.items

inventory = MagicalInventory()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def list_items():
    return jsonify(inventory.list_items())

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    description = data.get('description')
    result = inventory.add_item(description)
    return jsonify({"message": result})

@app.route('/api/items/<item_id>', methods=['DELETE'])
def remove_item(item_id):
    result = inventory.remove_item(item_id)
    return jsonify({"message": result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)