# 📌 Proyecto

Guía para configurar y ejecutar la aplicación en diferentes entornos.

---

## 🚀 Instalación y Ejecución

### 🔹 Linux (Sin Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Crear un archivo `.env` en la carpeta principal y agregar las siguientes variables de entorno:

```env
DATABASE_URL=postgresql://emprinet:49ainmKy0TxgOFW@206.189.182.199:5432/clinia
JWT_KEY=MIHcAgEBBEIAhFuGMfb4ucwO9Mdi80UuVUxBAWpyJ2NiHViEI2aSwtMEoGBQXXh1JOjVl
SECRET_KEY=b4e8f1d2c7a94e3f9d6b2a1f8c5e0d3a7e9b4c2d1f6a8e5c0d7b9f3a2e1c4d8
```

2. Ejecutar la aplicación:

```bash
python3 app.py
```

---

### 🐳 Linux (Con Docker)

```bash
sudo docker compose up
```

⚠️ **Nota:** Si ya existe un contenedor con el mismo nombre, eliminarlo o cambiar la propiedad `container_name` en el archivo `docker-compose.yml`.

📌 **Importante:** Las variables de entorno están definidas en `docker-compose.yml`. Aunque no es la mejor práctica, se dejó así para facilitar el despliegue.

---

### 🔹 Windows (Sin Docker)

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

1. Crear un archivo `.env` en la carpeta principal y agregar las siguientes variables de entorno:

```env
DATABASE_URL=postgresql://emprinet:49ainmKy0TxgOFW@206.189.182.199:5432/clinia
JWT_KEY=MIHcAgEBBEIAhFuGMfb4ucwO9Mdi80UuVUxBAWpyJ2NiHViEI2aSwtMEoGBQXXh1JOjVl
SECRET_KEY=b4e8f1d2c7a94e3f9d6b2a1f8c5e0d3a7e9b4c2d1f6a8e5c0d7b9f3a2e1c4d8
```

2. Ejecutar la aplicación:

```powershell
python app.py
```

💡 **Tip:** Si `python` no funciona, probar con `python3`.

---

### 🐳 Windows (Con Docker)

```powershell
docker-compose up
```

⚠️ **Nota:** Si ya existe un contenedor con el mismo nombre, eliminarlo o cambiar la propiedad `container_name` en el archivo `docker-compose.yml`.

📌 **Importante:** Las variables de entorno están definidas en `docker-compose.yml`. Aunque no es la mejor práctica, se dejó así para facilitar el despliegue.

---

## 📡 API Endpoints

### 🏥 Pacientes (`/patients`)
- **POST** `/patients` → Crear un paciente.
- **GET** `/patients` → Obtener la lista de pacientes.
- **GET** `/patients/<id>` → Obtener un paciente por su ID.
- **PUT** `/patients/<id>` → Actualizar un paciente.
- **DELETE** `/patients/<id>` → Eliminar un paciente.

### 📅 Turnos (`/appointments`)
- **POST** `/appointments` → Crear un turno (asociado a un paciente).
- **GET** `/appointments` → Obtener la lista de turnos.
- **GET** `/appointments/<id>` → Obtener un turno por su ID.
- **PUT** `/appointments/<id>` → Actualizar un turno.
- **DELETE** `/appointments/<id>` → Eliminar un turno.

### 👤 Usuarios (`/user`)
- **GET** `/user` → Obtener todos los usuarios.
- **POST** `/user` → Crear un usuario.
  - **Formato requerido:** `{ "username": "nombre", "password_hash": "contraseña" }`
  - Este usuario es necesario para obtener el token y acceder a la ruta protegida.

### 🔐 Autenticación JWT (`/auth`)
- **POST** `/auth` → Iniciar sesión y obtener un token.
  - **Ejemplo de credenciales:** `{ "username": "santi", "password_hash": "prueba123" }`

### 🔒 Ruta Protegida (`/`)
- **GET** `/` → Acceso solo con token JWT (para probar la autenticación).

---

✅ **Listo! Tu aplicación debería estar corriendo correctamente.** 🚀




