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
`media/db_export.csv` y cargarlos en pandas para análisis. Asegúrate de tener
la biblioteca **pandas** instalada para poder generar las gráficas.
El sitio incluye una página de **Estadísticas** accesible desde la biblioteca,
que muestra gráficos con la distribución de géneros y la calificación media de
los libros.

## Tecnologías usadas:

- Django 5.2.1
- Django REST Framework
- PostgreSQL
- Bootstrap 5

## Colecciones Postman

Se incluyen archivos de colección para probar la API con Postman. El archivo `FullAPI.postman_collection.json` reúne todas las peticiones disponibles. También puedes consultar la tabla `POSTMAN_TABLE.md` para ver un resumen de cada endpoint.

## Versiones utilizadas

- **Python** 3.12.10
- **Django** 5.2.1
- **Django REST Framework** 3.16
- **PostgreSQL** 14+
- **pip** 25.1.1

## Instalación rápida

1. Instala Python 3.12 y `pip`.
2. Crea un entorno virtual con `python -m venv venv` y actívalo.
3. Ejecuta `pip install -r requirements.txt` para instalar las dependencias.
4. Configura tu base de datos PostgreSQL en `miApp/settings.py`.
5. Realiza las migraciones con `python manage.py migrate`.
6. Crea un superusuario con `python manage.py createsuperuser` y ejecuta el servidor con `python manage.py runserver`.

## Fundamentación

El proyecto surge como una biblioteca digital donde cualquier usuario registrado puede subir y calificar libros en formato `.epub`.  Cuenta con un panel web para gestionar autores y géneros y una API REST que permite integrar la información con otras herramientas (por ejemplo aplicaciones móviles o Postman).  Con `conversor.py` exportamos los registros a CSV y mediante **pandas** se generan estadísticas básicas.

## Registro de un libro

Para crear un libro mediante la API se envía una petición `POST` a `/api/libros/libros/` con los datos del libro. A modo de referencia:

```json
{
  "nombre": "Mi libro",
  "autor": 1,
  "fecha_lanzamiento": "2024-01-01",
  "generos": [1],
  "archivo": "(archivo .epub)"
}
```

![Captura registro](ruta/a/captura_registro.png)

## Listado de libros

La ruta `GET /api/libros/libros/` devuelve todos los libros registrados. El siguiente ejemplo muestra la respuesta obtenida en Postman.

![Captura listado](ruta/a/captura_listado.png)

## Uso de pandas

El script `conversor.py` facilita la exportación de registros.  Los pasos principales son:

1. `db_to_csv()` recorre los modelos de libros y genera `media/db_export.csv`.
2. `reviews_to_csv()` produce `media/reviews.csv` con la cantidad de reseñas por usuario.
3. `csv_to_dataframe()` y `reviews_dataframe()` leen dichos archivos para manipularlos con pandas.

```python
from conversor import db_to_csv, csv_to_dataframe

path = db_to_csv()
df = csv_to_dataframe(path)
print(df.head())
```

## Estadísticas

La vista `estadisticas_view` lee los CSV y responde a preguntas comunes:

- **¿Cuál fue el género más guardado?**
- **¿Cuál fue el género con menos libros?**
- **¿Libro con mejor calificación?**
- **¿Libro con peor calificación?**
- **Usuarios con más reseñas.**

Además se generan tres gráficas que se muestran en la interfaz:

1. **Libros por género.**
2. **Calificación media por libro.**
3. **Reseñas por usuario.**

![Gráfico género](ruta/a/grafico_genero.png)
![Gráfico calificación](ruta/a/grafico_calificacion.png)
![Gráfico reseñas](ruta/a/grafico_reseñas.png)

## Próximamente

- Sugerencias de libros por género seleccionado.

## Licencia

Este proyecto se distribuye bajo los términos de la [Licencia MIT](LICENSE).