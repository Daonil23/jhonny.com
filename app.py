from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave secreta segura

# Configuración para manejar mayúsculas/minúsculas en las rutas
app.url_map.strict_slashes = False

# Lista de páginas disponibles
AVAILABLE_PAGES = {
    'index': 'Index.html',
    'empresa': 'Empresa.html',
    'contacto': 'contacto.html',
    'desarrollador': 'desarrollador.html'
}

# Context processor para añadir variables globales a todos los templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('Index.html')

# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Ruta para servir imágenes
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

# Ruta dinámica para las páginas
@app.route('/<page_name>')
def show_page(page_name):
    # Convertir a minúsculas para hacer la comparación insensible a mayúsculas
    page_name = page_name.lower()
    
    # Si es la página de inicio, redirigir a la raíz
    if page_name in ('index', 'index.html', 'inicio'):
        return redirect(url_for('index'))
    
    # Verificar si la página está en la lista de páginas disponibles
    template_name = None
    for key, value in AVAILABLE_PAGES.items():
        if key in page_name.lower() or page_name.lower() in value.lower():
            template_name = value
            break
    
    if template_name and os.path.exists(os.path.join(app.template_folder, template_name)):
        return render_template(template_name)
    else:
        # Si la página no existe, mostrar error 404
        return render_template('404.html'), 404

# Manejador de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Manejador de errores 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)