# Frontend Unitech

Aplicación React con Vite que consulta `GET /students` y muestra estados de carga, error y lista vacía.

## Ejecutar localmente

Requisitos: Node.js 24 y npm. Desde este directorio:

```bash
npm ci
cp .env.example .env
npm run dev
```

Configura `VITE_API_URL` en `.env` con la URL base del backend, por ejemplo `http://127.0.0.1:8000`. No agregues `/students` ni credenciales. Reinicia Vite después de cambiarla.

## Validar y compilar

```bash
npm run lint
npm run build
```

La compilación comprueba que `VITE_API_URL` exista y sea una URL HTTP o HTTPS válida. Genera los archivos de producción en `dist`.

Consulta el [README principal](../README.md) para configurar la base de datos, ejecutar las migraciones y desplegar el proyecto.
