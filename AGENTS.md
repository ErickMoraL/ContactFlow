# AGENTS.md

Instrucciones para agentes de Codex que trabajen en este repositorio.

## Proyecto

ContactFlow es un mini CRM hecho con Django. Permite gestionar contactos, empresas, datos de contacto, interacciones y etapas comerciales. La app tiene autenticacion propia, vistas protegidas por usuario y una interfaz HTML con templates Django y Tailwind CSS.

## Stack

- Backend: Python, Django 6.0.3.
- Base de datos: MySQL en Docker para desarrollo. Existe `db.sqlite3` local, pero esta ignorado por git y no debe tratarse como fuente de verdad.
- Frontend: templates Django + Tailwind CSS 4.
- Formato de templates: `djlint` con perfil `django`, indentacion de 2 espacios y `max_line_length = 120`.
- Contenedores: `docker-compose.yml` define servicios `db`, `web` y `node`.

## Filosofia del Proyecto

- Priorizar claridad sobre abstraccion excesiva.
- Preferir convenciones Django antes que patrones personalizados complejos.
- Mantener el proyecto simple y entendible para un desarrollador junior/intermedio.
- Evitar sobreingenieria.

## Nivel del Proyecto

Este proyecto es de aprendizaje. El código debe ser entendible para un desarrollador junior/intermedio. Una solución técnicamente más avanzada no es mejor si reduce la comprensión del usuario.

## Regla de Optimización

Cuando el usuario pida "optimizar", "mejorar" o "limpiar" código:

- No hacer refactors grandes por defecto.
- No cambiar la estructura general del archivo salvo que sea necesario.
- Mantener nombres, flujo y organización actual siempre que sea posible.
- Primero explicar qué problema se detectó.
- Luego proponer el cambio mínimo.
- Si existe una mejora grande, sugerirla como opción separada antes de implementarla.
- Priorizar que el usuario entienda el código sobre hacerlo "más elegante".
- No convertir funciones simples en clases, servicios, helpers o abstracciones nuevas sin pedir permiso.

## Estructura Relevante

- `ContactFLow/`: configuracion principal de Django, urls globales, ASGI/WSGI.
- `accounts/`: registro, login, logout, cambio y recuperacion de password.
- `contacts/`: modelos, formularios, vistas y templates del CRM.
- `templates/`: layouts compartidos.
- `static/src/input.css`: entrada de Tailwind.
- `static/css/output.css`: salida generada de Tailwind, ignorada por git.
- `.env.example`: variables requeridas para desarrollo.
- `.env`: secretos/local config, ignorado por git. No leer ni mostrar salvo que el usuario lo pida explicitamente.

## Comandos Habituales

Instalar dependencias Python:

```bash
pip install -r requirements.txt
```

Instalar dependencias Node:

```bash
npm install
```

Levantar servicios con Docker:

```bash
docker compose up -d
```

Ejecutar servidor Django dentro del entorno disponible:

```bash
python manage.py runserver 0.0.0.0:8000
```

Ejecutar migraciones:

```bash
python manage.py migrate
```

Crear migraciones despues de cambios en modelos:

```bash
python manage.py makemigrations
```

Ejecutar tests:

```bash
python manage.py test
```

Compilar CSS en modo watch:

```bash
npm run dev:css
```

Formatear/revisar templates Django:

```bash
djlint . --profile django --check
djlint . --profile django --reformat
```

## Reglas de Trabajo para Codex

- Responder en espanol por defecto, salvo que el usuario pida otro idioma.
- Antes de editar, revisar los archivos relacionados y seguir los patrones existentes.
- Hacer cambios pequenos y enfocados. Evitar refactors amplios si no son necesarios para la tarea.
- No modificar `.env`, `db.sqlite3`, `node_modules/`, `static/css/output.css`, archivos de cache ni artefactos generados.
- No exponer secretos ni valores reales de variables de entorno.
- Si se toca un modelo, considerar si hace falta migracion y crearla con `makemigrations` cuando corresponda.
- Si se toca autenticacion, permisos o datos del CRM, verificar que cada usuario solo acceda a sus propios objetos.
- Ejecutar pruebas relevantes antes de terminar cuando sea razonable. Si no se pueden ejecutar, explicar por que.
- No revertir cambios ajenos del usuario. Si hay cambios no relacionados en el arbol de git, ignorarlos.
- Para este proyecto, "optimizar" significa hacer el cambio mínimo que mejore claridad, seguridad, rendimiento o mantenibilidad.
- No reestructurar templates, views, forms o modelos completos si el usuario pidió una mejora puntual.
- Si una solución implica cambiar mucho código, detenerse y explicar primero el plan.

## Convenciones Django

- Proteger vistas privadas con `@login_required`.
- Filtrar consultas de contactos y recursos asociados por `user=request.user`.
- Usar `get_object_or_404(..., user=request.user)` para detalles/edicion/eliminacion cuando el modelo tenga usuario.
- Mantener nombres de rutas existentes cuando sea posible:
  - `contact_list`
  - `contact_detail`
  - `contact_create`
  - `contact_edit`
  - `login`
  - `register`
- Usar `reverse_lazy` en vistas basadas en clase cuando el redirect se define como atributo.
- Preferir formularios Django (`forms.ModelForm`) para validacion y renderizado de formularios.
- Mantener textos visibles orientados al usuario final y coherentes con el idioma actual de la interfaz.

## Seguridad y Datos

- La app usa un backend personalizado: `accounts.backends.EmailOrUsernameBackend`.
- El email de recuperacion usa backend de consola en desarrollo.
- `SECRET_KEY`, credenciales MySQL y hosts salen de variables de entorno.
- Cualquier funcionalidad de edicion, borrado o acciones masivas debe validar propiedad por usuario.
- No confiar en IDs enviados por POST/GET sin filtrar por usuario autenticado.

## Frontend y Templates

- Los templates extienden layouts compartidos cuando aplique (`templates/base.html`, `templates/app_layout.html`, `contacts/templates/contacts/layout.html`).
- Conservar bloques Django existentes: `title`, `header`, `content`, `extra_scripts`.
- Usar clases Tailwind de forma consistente con el estilo actual.
- Evitar CSS inline salvo casos puntuales.
- Al cambiar templates, ejecutar `djlint` si esta disponible.
- No editar directamente `static/css/output.css`; modificar `static/src/input.css` o templates y regenerar con Tailwind si hace falta.

## Base de Datos y Docker

- El servicio MySQL se expone en el host por el puerto `3334`, pero dentro de Docker el host esperado es `db` y el puerto `3306`.
- El servicio `web` monta el repo en `/app` y queda con `sleep infinity`; normalmente los comandos Django se ejecutan dentro del contenedor o desde el entorno local configurado.
- El servicio `node` corre `npm install && npm run dev:css`.
- No asumir que Docker esta corriendo; comprobarlo antes de depender de la base de datos.

## Verificacion Recomendada

Para cambios backend:

```bash
python manage.py test
python manage.py check
```

Para cambios en modelos:

```bash
python manage.py makemigrations --check --dry-run
python manage.py test
```

Para cambios en templates:

```bash
djlint . --profile django --check
```

Para cambios frontend/Tailwind:

```bash
npm run dev:css
```

## Al Final de Cada Tarea

Indicar brevemente:

- Que archivos cambiaron.
- Que verificacion se ejecuto.
- Cualquier riesgo o pendiente.
- Siguiente paso sugerido, solo si aporta valor.
