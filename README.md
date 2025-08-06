# 📝 Gestión de Actas y Compromisos – Prueba Técnica

Este proyecto es un módulo independiente para gestionar **actas, compromisos y gestiones**, con autenticación basada en roles, protección de archivos adjuntos, validaciones y consumo desde una API propia.

---

## ⚙️ Tecnologías utilizadas

- **Backend**: Django + Django REST Framework
- **Frontend**: React + Vite
- **Base de datos**: SQLite (local)

---

## 👤 Roles implementados

| Rol           | Permisos principales |
|---------------|----------------------|
| **Administrador** | Accede a todas las actas, compromisos y gestiones |
| **Usuario**       | Solo puede ver actas donde participa (como creador o responsable) |

---

## 🔐 Credenciales para pruebas

| Rol           | Correo                     | Contraseña    |
|---------------|----------------------------|---------------|
| Admin         | `admin@correo.com`         | `admin123`    |
| Usuario Base  | `usuario@correo.com`       | `usuario123`  |

---


## Instrucciones para correr el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/usuario/repo-actas.git
cd repo-actas
```

---

### 2. Configura el backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata users.json  # precarga usuarios y ejemplos
python manage.py runserver
```

El backend se ejecuta en: `http://127.0.0.1:8000/`

---

### 3. Configura el frontend (React)

```bash
cd frontend
npm install
npm run dev
```

El frontend se ejecuta en: `http://127.0.0.1:5173/`

---

## Estructura principal

```
backend/
├── actas_app/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── db.sqlite3 

frontend/
├── src/
│   ├── components/
│   ├── api/
│   └── App.jsx
└── index.html
```

---

## 🛡️ Protección de archivos

Todos los archivos PDF y adjuntos se sirven bajo `/media/<archivo>` y están protegidos mediante autenticación por token. Solo usuarios autenticados pueden acceder.

---

## 🧠 Lógica de visibilidad de “Agregar gestión”

El botón “Agregar gestión” solo se muestra si:

- El usuario es **Administrador**, o  
- El usuario es responsable de un compromiso dentro del acta

---

## 📩 Contacto

**Desarrollador:** [Tu nombre]  
**Correo:** tuemail@correo.com

---