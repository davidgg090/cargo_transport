[![Python application](https://github.com/davidgg090/cargo_transport/actions/workflows/python-app.yml/badge.svg)](https://github.com/davidgg090/cargo_transport/actions/workflows/python-app.yml)

# Cargo Transport API

## Descripción

Esta es una API para una compañía aérea que se dedica al transporte de cargas aéreas entre diferentes orígenes y destinos. La API permite gestionar paquetes de clientes, incluyendo la creación de usuarios y autenticación, adición de paquetes, y generación de reportes diarios.

## Tecnologías Utilizadas

- **FastAPI**: Framework web para construir APIs rápidas y eficientes.
- **SQLAlchemy**: ORM para interactuar con la base de datos SQLite.
- **Pydantic**: Para validación de datos y creación de modelos.
- **JWT**: Para autenticación y manejo de tokens.
- **python-dotenv**: Para cargar variables de entorno desde un archivo `.env`.
- **pytest**: Framework para escribir y ejecutar pruebas.
- **Docker**: Para contenerizar la aplicación y facilitar su despliegue.

## Requisitos Previos

- Python 3.12+
- pip
- Docker (opcional, para contenerización)

## Instalación

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/davidgg090/cargo_transport.git
    cd cargo_transport
    ```

2. Crear y activar un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
    ```

3. Instalar las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

    ```plaintext
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    SQLALCHEMY_DATABASE_URL=sqlite:///./test.db
    ```

## Uso

1. Iniciar el servidor:

    ```bash
    uvicorn app.main:app --reload
    ```

2. La API estará disponible en `http://127.0.0.1:8000`.

## Endpoints

### Raíz

- **GET** `/`: Devuelve un mensaje de bienvenida.
    - Response: `{ "message": "Welcome to the Cargo Transport API" }`

### Health Check

- **GET** `/health`: Devuelve el estado de la aplicación.
    - Response: `{ "status": "healthy" }`
### Autenticación

- **POST** `/auth/register/`: Registrar un nuevo usuario.
    - Request Body: `{ "username": "string", "password": "string" }`
    - Response: `{ "username": "string" }`

- **POST** `/auth/token/`: Obtener un token de acceso.
    - Request Body: `{"username": "string", "password": "string"}`
    - Response: `{ "access_token": "string", "token_type": "bearer" }`

### Paquetes

- **POST** `/cargo/packages/`: Añadir un nuevo paquete (requiere autenticación).
    - Request Body: `{ "client": "string", "weight": "float", "origin": "string", "destination": "string", "date": "date" }`
    - Response: `{ "id": "int", "client": "string", "weight": "float", "origin": "string", "destination": "string", "date": "date" }`

- **GET** `/cargo/report/`: Obtener un reporte diario (requiere autenticación).
    - Query Parameters: `report_date=YYYY-MM-DD`
    - Response: `{ "total_packages": "int", "total_revenue": "float" }`

## Ejecución de Pruebas

Para ejecutar las pruebas, usa el siguiente comando:

```bash
pytest
```

Esto ejecutará todas las pruebas definidas en la carpeta tests.


# Contenerización con Docker

### Requisitos Previos

- Docker instalado en tu máquina.

### Construir y Ejecutar la Imagen Docker

1. **Construir la imagen Docker**:

    ```bash
    docker build -t cargo-transport-api .
    ```

2. **Ejecutar el contenedor**:

    ```bash
    docker run -d -p 8000:8000 --name cargo-transport-api-container cargo-transport-api
    ```

    La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. 
