# Mi Página Personal

Mi Página Personal es un sitio web desarrollado como trabajo final de Introducción al Desarrollo Web. Incluye secciones sobre mí (inicio, hobbies, música, cosas que leí con reseñas detalladas) y página de contacto con formulario funcional que guarda datos en MySQL.

## Tecnologías utilizadas

- HTML5 – Estructura de las páginas
- CSS3 – Estilos y diseño responsivo
- JavaScript – Validaciones y lógica interactiva
- Python – Servidor backend para formularios
- SQL/MySQL – Base de datos para mensajes de contacto

## Instrucciones de instalación y ejecución

### 1. Clonar el proyecto
git clone https://github.com/tu-usuario/mi-pagina-personal.git
cd mi-pagina-personal


### 2. Configurar base de datos
python crear_bd.py

### 3. Iniciar servidor backend
python server.py

### 4. Abrir en navegador
http://localhost:8000

## Estructura del proyecto

### Frontend
- index.html: Página principal
- hobbies.html: Mis hobbies
- musica.html: Gustos musicales
- cosas-que-lei.html: Reseñas de libros y fanfics (La Dependienta, Jung, Kawakami, Tapiz Amarillo, AO3)**
- contacto.html: Formulario funcional
- styles.css`: Estilos globales

### JavaScript
- contacto.js: Validación y envío AJAX


### Backend
- server.py: Procesador de formularios
- crear_bd.py: Configuración MySQL
