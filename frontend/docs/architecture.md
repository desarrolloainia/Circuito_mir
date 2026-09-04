# Arquitectura y estructura

## Resumen técnico

| Área               | Tecnología o decisión                              |
| ------------------ | -------------------------------------------------- |
| Framework          | Nuxt 4 y Vue 3 con TypeScript.                     |
| Componentes        | Nuxt UI 4 y `@internationalized/date`.             |
| Estilos            | Tailwind CSS 4 y tema global en CSS.               |
| Iconos             | Iconify con las colecciones Lucide y Simple Icons. |
| Fuente             | Public Sans variable.                              |
| Gestor de paquetes | pnpm.                                              |
| Arquitectura       | Feature-Sliced Design (FSD) adaptado a Nuxt.       |
| Datos actuales     | Mocks en memoria y estado Nuxt `useState`.         |

Nuxt usa `src` como directorio raíz. Las rutas no viven en el `pages` convencional: `nuxt.config.ts` configura `src/app/routes` como directorio de rutas y `src/app/layouts` como directorio de layouts.

## Capas FSD

La dirección permitida de dependencias es:

```text
app → pages → entities → shared
```

Una capa solo puede importar desde capas situadas a su derecha. También puede importar dentro de su propio slice, pero dos slices hermanos no deben importarse entre sí.

### `app`

Responsabilidad global de la aplicación:

- Arranque de Nuxt.
- Rutas y layouts.
- Configuración visual global.
- Estilos globales.
- Composición de páginas completas.

Puede importar desde cualquier capa inferior. No debe contener reglas de negocio específicas de una pantalla.

### `pages`

Cada slice representa una pantalla o un grupo de pantallas que ya forman una unidad estable. Contiene composición, estado local, filtros, formularios y comportamiento específico de esa página.

Reglas actuales:

- Cada slice expone su interfaz pública mediante `index.ts`.
- Las rutas importan desde ese `index.ts`, nunca desde `ui/` o `model/` directamente.
- Un slice de página no puede importar otro slice de página.
- La lógica usada solo por una pantalla permanece en esa pantalla.

### `entities`

Contiene modelos de negocio compartidos por varias páginas. Actualmente solo existe la entidad `mir-request`, consumida por el listado, el formulario y el detalle del portal de usuario.

No debe depender de `pages` ni de `app`.

### `shared`

Contiene infraestructura sin reglas de negocio. Actualmente expone el formateador común de fecha y hora.

No debe conocer solicitudes MIR, páginas, layouts ni flujos de usuario.

### Capas no creadas

No existen `features` ni `widgets`. No deben añadirse por anticipado:

- Crea un `feature` cuando una misma interacción de usuario se reutilice realmente en dos o más páginas.
- Mantén las secciones visuales específicas dentro de su página.
- Usa `shared/ui` solo cuando exista un componente visual genérico y reutilizado sin conocimiento del dominio.

## Árbol del proyecto

```text
frontend/
├── docs/                         Documentación para desarrollo
├── public/                       Archivos servidos sin transformación
├── src/
│   ├── app/                      Capa FSD App y convenciones Nuxt
│   │   ├── layouts/              Marcos comunes por grupo de rutas
│   │   ├── routes/               Entradas de routing, sin lógica de negocio
│   │   └── styles/               Estilos y tokens globales
│   ├── entities/                 Modelos de negocio compartidos
│   │   └── mir-request/
│   ├── pages/                    Pantallas completas
│   │   ├── admin/
│   │   ├── create-mir-request/
│   │   ├── mir-request-details/
│   │   └── user-dashboard/
│   ├── shared/                   Infraestructura reutilizable
│   │   └── lib/
│   ├── app.config.ts             Configuración de Nuxt UI
│   └── app.vue                   Entrada visual de la aplicación
├── nuxt.config.ts                Configuración de Nuxt, rutas y prerender
├── package.json                  Dependencias y scripts
├── pnpm-lock.yaml                Versiones exactas de dependencias
├── pnpm-workspace.yaml           Configuración del workspace pnpm
└── tsconfig.json                 Referencias TypeScript generadas por Nuxt
```

No se deben editar manualmente `node_modules`, `.nuxt`, `.output` ni otros artefactos generados.

## Referencia de carpetas y archivos

### Raíz

| Ruta                  | Responsabilidad                                                                  |
| --------------------- | -------------------------------------------------------------------------------- |
| `README.md`           | Presentación breve, puesta en marcha y enlaces a esta documentación.             |
| `docs/`               | Documentación mantenida para futuros desarrolladores.                            |
| `public/`             | Recursos públicos copiados directamente al resultado final. Contiene el favicon. |
| `nuxt.config.ts`      | Módulos, directorios Nuxt, hoja global, reglas de renderizado y compatibilidad.  |
| `package.json`        | Dependencias y comandos de desarrollo, calidad y build.                          |
| `pnpm-lock.yaml`      | Resolución reproducible de dependencias. Debe actualizarse con pnpm.             |
| `pnpm-workspace.yaml` | Declara el workspace de pnpm.                                                    |
| `tsconfig.json`       | Enlaza los proyectos TypeScript generados por Nuxt.                              |
| `Agents.md`           | Instrucciones locales para herramientas y asistentes de desarrollo.              |

### Entrada y configuración visual

| Ruta                      | Responsabilidad                                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `src/app.vue`             | Envuelve todas las rutas con `UApp`, `NuxtLayout` y `NuxtPage`.                                            |
| `src/app.config.ts`       | Configura naranja como color primario y slate como color neutral de Nuxt UI.                               |
| `src/app/styles/main.css` | Importa Tailwind, Nuxt UI y Public Sans; define paletas, canvas, sidebar, selección y movimiento reducido. |

### Layouts

| Ruta                          | Responsabilidad                                                                                             |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `src/app/layouts/default.vue` | Layout administrativo: sidebar, navegación MIR/PMP, contadores y buscador global local.                     |
| `src/app/layouts/usuario.vue` | Layout del solicitante: navegación reducida, identidad de usuario, ayuda y enlace para saltar al contenido. |

Cada layout usa un `storage-key` de Nuxt UI diferente. Ese almacenamiento conserva preferencias visuales del dashboard, no datos MIR.

### Rutas

Las entradas de `src/app/routes` son adaptadores delgados. Seleccionan layout y modo de color, importan una página mediante su API pública y la renderizan.

| Ruta de archivo                                | Página importada                                             |
| ---------------------------------------------- | ------------------------------------------------------------ |
| `src/app/routes/usuario/dashboard.vue`         | `UserDashboardPage` desde `@/pages/user-dashboard`.          |
| `src/app/routes/usuario/solicitudes/nueva.vue` | `CreateMirRequestPage` desde `@/pages/create-mir-request`.   |
| `src/app/routes/usuario/solicitudes/[id].vue`  | `MirRequestDetailsPage` desde `@/pages/mir-request-details`. |
| `src/app/routes/admin/dashboard.vue`           | `AdminDashboardPage` desde `@/pages/admin`.                  |
| `src/app/routes/admin/mir/pendientes.vue`      | `AdminMirRecordsPage` con vista `pending`.                   |
| `src/app/routes/admin/mir/cerradas.vue`        | `AdminMirRecordsPage` con vista `closed`.                    |
| `src/app/routes/admin/mir/documentos.vue`      | `AdminMirDocumentsPage`.                                     |
| `src/app/routes/admin/mir/empresas.vue`        | `AdminMirCompaniesPage`.                                     |
| `src/app/routes/admin/pmp/sin-procesar.vue`    | `AdminPmpRecordsPage` con vista `unprocessed`.               |
| `src/app/routes/admin/pmp/procesadas.vue`      | `AdminPmpRecordsPage` con vista `processed`.                 |

Una entrada de ruta no debe obtener datos ni implementar filtros, formularios o reglas de negocio.

### Entidad `mir-request`

| Ruta                                            | Responsabilidad                                                             |
| ----------------------------------------------- | --------------------------------------------------------------------------- |
| `src/entities/mir-request/index.ts`             | API pública de la entidad.                                                  |
| `src/entities/mir-request/model/mir-request.ts` | Tipos, solicitudes iniciales, secuencia mock y composable `useMirRequests`. |

La entidad expone:

```text
useMirRequests
CreateMirRequestInput
MirRequest
MirRequestAttachment
MirRequestStatus
```

`useMirRequests` gestiona dos estados Nuxt:

```text
user-mir-requests
user-mir-request-sequence
```

Sus operaciones actuales son leer todas las solicitudes, crear una y localizar una por ID.

### Página `user-dashboard`

| Ruta                                                | Responsabilidad                                                       |
| --------------------------------------------------- | --------------------------------------------------------------------- |
| `src/pages/user-dashboard/index.ts`                 | API pública de la página.                                             |
| `src/pages/user-dashboard/ui/UserDashboardPage.vue` | CTA de creación, búsqueda local y listado de solicitudes del usuario. |

Consume `useMirRequests` y `formatDate` mediante sus respectivas APIs públicas.

### Página `create-mir-request`

| Ruta                                                       | Responsabilidad                                                                                       |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `src/pages/create-mir-request/index.ts`                    | API pública de la página.                                                                             |
| `src/pages/create-mir-request/ui/CreateMirRequestPage.vue` | Formulario oficial de datos MIR, preparación del input, creación mock, toast y navegación al detalle. |

La selección de archivos se convierte en metadatos `{ name, size }`. El contenido real del archivo no se almacena.

### Página `mir-request-details`

| Ruta                                                         | Responsabilidad                                               |
| ------------------------------------------------------------ | ------------------------------------------------------------- |
| `src/pages/mir-request-details/index.ts`                     | API pública de la página.                                     |
| `src/pages/mir-request-details/ui/MirRequestDetailsPage.vue` | Búsqueda por parámetro de ruta, resumen, adjuntos y timeline. |

El timeline solo contiene el evento `Solicitud creada`. Un ID desconocido muestra una alerta.

### Página `admin`

`admin` es un slice existente que agrupa varias vistas operativas estrechamente relacionadas.

| Ruta                                           | Responsabilidad                                                |
| ---------------------------------------------- | -------------------------------------------------------------- |
| `src/pages/admin/index.ts`                     | API pública para rutas y layout administrativo.                |
| `src/pages/admin/model/dashboard.ts`           | Métricas, actividad, acciones rápidas y distribución por área. |
| `src/pages/admin/model/mir.ts`                 | Tipos y mocks de MIR, documentos y agregados por empresa.      |
| `src/pages/admin/model/pmp.ts`                 | Tipos, grupos y mocks de PMP procesadas y sin procesar.        |
| `src/pages/admin/ui/AdminDashboardPage.vue`    | Resumen administrativo, actividad y pendientes por área.       |
| `src/pages/admin/ui/AdminMirRecordsPage.vue`   | Tabla reutilizada para MIR pendientes y cerradas.              |
| `src/pages/admin/ui/AdminMirDocumentsPage.vue` | Inventario filtrable de documentos.                            |
| `src/pages/admin/ui/AdminMirCompaniesPage.vue` | Ranking y consulta de MIR por empresa.                         |
| `src/pages/admin/ui/AdminPmpRecordsPage.vue`   | Tabla reutilizada para PMP procesadas y sin procesar.          |

Los imports relativos entre `model` y `ui` son internos al mismo slice. Los consumidores externos deben usar `src/pages/admin/index.ts`.

### Shared

| Ruta                      | Responsabilidad                                            |
| ------------------------- | ---------------------------------------------------------- |
| `src/shared/lib/index.ts` | API pública del segmento `shared/lib`.                     |
| `src/shared/lib/date.ts`  | Formatea fecha y hora en español con zona `Europe/Madrid`. |

## Flujo de datos del portal de usuario

```text
Route adapter
  ↓
Page slice
  ↓
useMirRequests()
  ↓
Nuxt useState en memoria
```

Al crear una solicitud:

```text
CreateMirRequestPage
  → valida el formulario con atributos HTML
  → transforma File[] en metadatos
  → createMirRequest(input)
  → añade el registro al inicio del estado
  → muestra un toast
  → navega a /usuario/solicitudes/:id
```

El estado sobrevive a la navegación del cliente. Una recarga reconstruye los mocks iniciales y elimina los registros creados durante la sesión.

## Datos administrativos

Los datos administrativos son arrays estáticos dentro de `src/pages/admin/model`. Los filtros son `computed` locales y recorren esos arrays en memoria.

El modelo administrativo `MirRecord` y la entidad de usuario `MirRequest` son modelos distintos. Actualmente no deben tratarse como una única fuente de verdad:

- Una solicitud creada en `/usuario` no aparece en `/admin`.
- Los mocks pueden compartir referencias con información diferente.
- No existe sincronización entre ambos contextos.

Cuando se incorpore una API, deberá definirse un contrato único y eliminar progresivamente esta duplicidad.

## Rendering

`nuxt.config.ts` prerenderiza las páginas estáticas de administración y el dashboard de usuario. `/usuario` redirige a `/usuario/dashboard`.

El formulario se renderiza en cada petición para que la fecha de detección inicial corresponda al día actual y no a la fecha del último build.

La ruta dinámica `/usuario/solicitudes/:id` se resuelve en tiempo de ejecución. No puede prerenderizar solicitudes creadas solo en memoria.

## Tema y accesibilidad

La aplicación usa un tema oscuro con naranja como color de acción. Los componentes proceden prioritariamente de Nuxt UI y se adaptan con utilidades Tailwind.

Convenciones existentes:

- Diseño mobile-first.
- Controles nativos o Nuxt UI antes que componentes personalizados.
- Etiquetas accesibles para campos e iconos interactivos.
- Captions en tablas.
- Enlace para saltar navegación en el layout de usuario.
- Respeto de `prefers-reduced-motion` en estilos globales.
