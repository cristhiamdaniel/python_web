"""
Hola Mundo con Flask
"""

from flask import Flask

app = Flask(__name__) # __name__ es el nombre del módulo
@app.route('/') # Ruta principal
def index():
    """
    Ruta principal
    :return: str
    """
    return 'Hola Mundo'

if __name__ == '__main__':
    app.run(debug=True, port=8000) # Se ejecuta la aplicación