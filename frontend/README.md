## Build a Chat (Frontend)

Vue 3 + Vite project scaffold for login and registration views. Backend (Flask) integration will be added later.

### Requisitos
- Node.js 18+

### Instalación
```bash
npm install
```

### Desarrollo
```bash
npm run dev
```
Abre `http://localhost:5173`.

Opcional: configura la URL del backend (por defecto `http://localhost:5000`). Crea un archivo `.env` en la raíz con:
```bash
VITE_API_BASE_URL=http://localhost:5000
```

### Scripts
- `npm run dev`: servidor de desarrollo
- `npm run build`: build de producción
- `npm run preview`: previo local del build

### Estructura
- `src/views/LoginView.vue`: formulario de inicio de sesión
- `src/views/RegisterView.vue`: formulario de registro
- `src/router/index.ts`: rutas (`/login`, `/register`)
- `src/services/api.ts`: cliente para `/login` y `/signup`

Cuando el backend esté listo, conectaremos las acciones de los formularios a los endpoints de Flask.

Nota backend: habilita CORS en Flask para `http://localhost:5173`.


