# 📚 Proyecto Django - Biblioteca de Libros

Este proyecto es una plataforma web desarrollada con Django y PostgreSQL que permite a los usuarios registrarse, iniciar sesión y gestionar una biblioteca digital. Incluye funcionalidades para subir libros en formato `.epub`, clasificarlos por autor y género, calificarlos y visualizarlos desde una interfaz web y a través de una API REST protegida.

## Características principales:

- 🔐 Registro y autenticación de usuarios (vía sesión y JWT)
- 📖 Subida de libros en formato `.epub`
- 🧑‍💼 Creación dinámica de autores y géneros desde el formulario web
- 🔎 Búsqueda de libros y vista de biblioteca
- 🧩 API REST para integración con frontend y herramientas externas
- 🗂️ Base de datos PostgreSQL

## Estadísticas y análisis

Con `conversor.py` puedes exportar los datos de la base al archivo
`media/db_export.csv` y cargarlos en pandas para análisis.
El sitio incluye una página de **Estadísticas** accesible desde la biblioteca,
que muestra gráficos con la distribución de géneros y la calificación media de
los libros.

## Tecnologías usadas:

- Django 5.2.1
- Django REST Framework
- PostgreSQL
- Bootstrap 5