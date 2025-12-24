
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import mysql.connector
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '61219257',  
    'database': 'mi_web'
}

class MiServidor(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Maneja peticiones GET: servir archivos HTML/CSS/JS"""
        ruta = self.path
        

        if ruta == '/ver-mensajes':
            contrasena = self.headers.get('X-Password', '')
            if contrasena != 'admin123':
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Contraseña incorrecta'}).encode('utf-8'))
                return
            
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM mensajes_contacto ORDER BY fecha DESC;")
                mensajes = cursor.fetchall()
                cursor.close()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(mensajes, default=str).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return
        

        if ruta == '/':
            ruta = '/index.html'
        
        ruta_archivo = ruta.lstrip('/')
        try:
            with open(ruta_archivo, 'rb') as f:
                contenido = f.read()
            
            self.send_response(200)
            if ruta_archivo.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif ruta_archivo.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif ruta_archivo.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(contenido)
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Archivo no encontrado</h1>')
    
    def do_POST(self):
        """Maneja peticiones POST: guardar formulario en BD"""
        ruta = self.path
        
        if ruta == '/enviar-contacto':
            try:

                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                datos = json.loads(body)
                

                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                query = """
                INSERT INTO mensajes_contacto (nombre, email, asunto, mensaje, fecha)
                VALUES (%s, %s, %s, %s, %s)
                """
                
                valores = (
                    datos.get('nombre'),
                    datos.get('email'),
                    datos.get('asunto'),
                    datos.get('mensaje'),
                    datetime.now()
                )
                
                cursor.execute(query, valores)
                conn.commit()
                cursor.close()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'exito': True, 'mensaje': 'Mensaje guardado'}).encode('utf-8'))
            
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    PUERTO = 8000
    servidor = HTTPServer(('localhost', PUERTO), MiServidor)
    print(f"Servidor corriendo en http://localhost:{PUERTO}")
    print(f"Recuerda cambiar TU_CONTRASEÑA_AQUI en server.py")
    servidor.serve_forever()
