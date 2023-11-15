# Django Pokemon

**Pasos para instalación y despliegue**

1. Descarga

Para obtener la aplicación puede descomprimir el archivo adjunto en cualquier ubicación que no requiera permisos de administrado o directamente con git:

|git clone https://www.github.com/PabloOmega/Django-Pokemon|
| :- |

1. Instalación y deploy
- Instalar Python
- En la carpeta Django-Pokemon, encontrará un archivo llamado “setup.bat” puede ejecutarlo directamente dando doble clic (solo Windows). Este archivo comprueba si está instalado Python. Si lo está crea un entorno virtual, instala los requerimientos de la aplicación, realiza las migraciones, ejecuta el servidor y abre automáticamente la página principal en el navegador por defecto. Si desea realizarlo manualmente, ejecute los siguientes comandos en un terminal de Windows:

|cd <ubicación-de-la-carpeta-de-descarga>\Django-Pokemon|
| :- |
|python -m venv env\_django|
|call "env\_django\Scripts\activate"|
|pip install -r requirements.txt|
|python migrate.py makemigrations|
|python migrate.py migrate|
|python migrate.py runserver|

- La primera vez se demorará mientras carga todos los pokemons, por favor espere.

- Si lo realizó manualmente o si no se abrió automáticamente la página, abra una pestaña en su navegador y diríjase a <http://localhost:8000>.

- Si cierra y quiere volver a ejecutar la aplicación puede abrir directamente el archivo “run.bat”

**Pasos para realizar la revisión**

1. Los principales archivos de la aplicación se encuentran en la carpeta Django-Pokemon/pokemon\_api/pokemon\_app. A continuación, se muestra una tabla con la descripción de cada archivo importante:

|Archivo|Ruta|Descripción|Paquetes|
| :- | :- | :- | :- |
|apps.py|/pokemon\_app|Aquí se define la aplicación|Django|
|models.py|/pokemon\_app|Aquí se diseña la base de datos con las principales tablas de los pokemons|Django|
|pokemon\_api.py|/pokemon\_app|Aquí se hace el llamado a la API y se procesan y se cargan los datos|<p>requests: para realizar las solicitudes a la API</p><p>PokeBase: se utiliza únicamente para obtener todos los nombres de los pokemons de la manera sencilla, ya que para demás solicitudes se cuelga.</p>|
|urls.py|/pokemon\_app|Aquí se definen los links de la aplicación. El link principal simplemente es la ruta del local host (“/”) y el link para cada pokemon se establece como (“/pokemon\_id”)|Django|
|views.py|/pokemon\_app|Aquí se procesan las llamadas al servidor y se renderizan las páginas html de la aplicación. Además, actualiza, carga y gestiona la base de datos. Los datos completos se van cargando en función de lo que se muestra para no tardar mucho tiempo al iniciar la aplicación.|Django|
|pokemon\_list.html|/pokemon\_app/templates|Página principal donde se muestran los pokemons paginados con su respectiva información. Además, permite realizar la búsqueda de cada pokemon.|-|
|pokemon\_detail.html|/pokemon\_app/templates|Página individual de cada pokemon, donde se muestra la información más detalla acerca del pokemon.|-|
|pokemon\_detail.css|/pokemon\_app/static/css|Permite definir los estilos de ambas páginas.|-|



