# Funcionamiento y flujos

## Áreas de la aplicación

El frontend presenta dos experiencias independientes:

| Área                 | Prefijo    | Usuario objetivo                                          |
| -------------------- | ---------- | --------------------------------------------------------- |
| Portal de usuario    | `/usuario` | Persona que crea y consulta sus propias solicitudes MIR.  |
| Panel administrativo | `/admin`   | Personal que consulta expedientes MIR y PMP del circuito. |

La separación actual es visual y estructural. No existe autenticación ni autorización real; conocer una URL permite abrirla.

## Mapa de rutas

| URL                          | Layout    | Propósito                                  | Renderizado actual |
| ---------------------------- | --------- | ------------------------------------------ | ------------------ |
| `/usuario`                   | Ninguno   | Redirección al dashboard de usuario.       | Redirect.          |
| `/usuario/dashboard`         | `usuario` | Listado y búsqueda de solicitudes propias. | Prerender.         |
| `/usuario/solicitudes/nueva` | `usuario` | Creación de una solicitud MIR.             | SSR.               |
| `/usuario/solicitudes/:id`   | `usuario` | Detalle y timeline de una solicitud.       | Dinámico.          |
| `/admin/dashboard`           | `default` | Resumen operativo.                         | Prerender.         |
| `/admin/mir/pendientes`      | `default` | MIR que requieren actuación.               | Prerender.         |
| `/admin/mir/cerradas`        | `default` | Histórico de MIR cerradas.                 | Prerender.         |
| `/admin/mir/documentos`      | `default` | Inventario de documentos MIR.              | Prerender.         |
| `/admin/mir/empresas`        | `default` | Expedientes agrupados por empresa.         | Prerender.         |
| `/admin/pmp/sin-procesar`    | `default` | PMP pendientes de revisión.                | Prerender.         |
| `/admin/pmp/procesadas`      | `default` | Histórico de PMP procesadas.               | Prerender.         |

No existen rutas específicas para `/`, `/admin` ni `/usuario/solicitudes`.

## Portal de usuario

### Dashboard

`/usuario/dashboard` muestra:

- Acceso principal a una nueva solicitud.
- Número total de solicitudes cargadas en el estado local.
- Búsqueda por referencia, descripción, empresa o persona detectora.
- Referencia, estado, descripción, empresa y fecha de detección de cada solicitud.
- Acción `Ver seguimiento` para abrir el detalle.

El único estado soportado hoy es `Creada`.

### Crear una solicitud

`/usuario/solicitudes/nueva` solicita:

| Campo                           | Regla actual                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------- |
| Usuario                         | Usuario actual, visible y de solo lectura.                                               |
| Fecha de detección              | Obligatoria, seleccionada con `UCalendar` y no posterior al día actual.                  |
| Persona que ha detectado la MIR | Obligatoria, hasta 120 caracteres.                                                       |
| Descripción                     | Obligatoria, entre 20 y 2000 caracteres. Debe explicar el hecho sin incluir la solución. |
| ¿Está solucionada ya la MIR?    | Obligatorio, con valores `Sí` o `No`.                                                    |
| Adjuntos                        | Opcionales, múltiples, imágenes o PDF en el selector.                                    |
| Empresa                         | Opcional, hasta 160 caracteres.                                                          |
| Persona de contacto             | Opcional, hasta 120 caracteres.                                                          |
| Teléfono                        | Opcional, hasta 30 caracteres.                                                           |
| Correo electrónico              | Opcional y validado por el tipo de input HTML.                                           |
| Código de cliente               | Opcional, hasta 50 caracteres.                                                           |

Al enviar:

1. Se recortan espacios iniciales y finales de los campos de texto editables.
2. Los archivos se reducen a nombre y tamaño.
3. La entidad genera una referencia `MIR-2026-NNNN`.
4. La solicitud se añade al inicio del estado de la sesión.
5. Se muestra una notificación de éxito.
6. La aplicación navega al detalle recién creado.

No se transmite información fuera del navegador.

### Seguimiento

`/usuario/solicitudes/:id` busca el ID en el estado de solicitudes y presenta:

- Referencia y estado.
- Usuario, fecha de detección, persona detectora, descripción y estado de resolución inicial.
- Empresa, persona, teléfono, correo electrónico y código de cliente.
- Metadatos de los adjuntos.
- Timeline con el evento `Solicitud creada`.

Si el ID no existe, aparece `Solicitud no encontrada`.

Una solicitud creada durante la sesión deja de existir al recargar. Por ello, recargar su URL de detalle puede mostrar el estado de no encontrado.

## Panel administrativo

### Layout y búsqueda global

El layout `default` incluye:

- Navegación por dashboard, MIR y PMP.
- Contadores de MIR pendientes y PMP sin procesar.
- Buscador global mediante `UDashboardSearch`.
- Resultados para navegación, MIR, PMP, documentos y empresas.

La búsqueda global indexa los mocks en memoria. Al seleccionar un registro navega a su listado con un parámetro de consulta, por ejemplo `?search=MIR-2026-1842`.

### Dashboard administrativo

`/admin/dashboard` muestra cuatro bloques:

- Métricas generales.
- Acciones rápidas.
- Actividad reciente.
- Pendientes por área.

Las cifras y actividades son estáticas. Las acciones rápidas y algunos botones todavía no ejecutan operaciones.

### MIR pendientes y cerradas

`AdminMirRecordsPage` sirve dos rutas mediante la propiedad `view`.

La vista pendiente permite:

- Buscar por referencia, asunto, empresa, responsable, ejecutor o departamento.
- Filtrar por empresa.
- Filtrar por cola: Usuario, CAL, Responsable, Ejecutor o CAL C.E.
- Mostrar expedientes con más de siete días abiertos.

La vista cerrada permite búsqueda y filtro por empresa. Ninguna de las dos modifica expedientes.

### Documentos MIR

`/admin/mir/documentos` permite:

- Buscar por nombre, referencia, empresa o autor de subida.
- Filtrar por empresa.
- Filtrar por tipo de documento.

Los archivos son metadatos mock; no pueden abrirse ni descargarse.

### MIR por empresa

`/admin/mir/empresas` deriva empresas a partir de MIR pendientes y cerradas. Las ordena por número de pendientes y después por prioridad alta.

Las cuatro primeras empresas aparecen como accesos rápidos. La tabla inferior combina expedientes pendientes y cerrados y permite buscar o seleccionar una empresa.

### PMP

`AdminPmpRecordsPage` sirve dos rutas mediante la propiedad `view`.

PMP sin procesar se agrupa en:

- Vencidas.
- Próximas.
- Recientes.

PMP procesadas se agrupa en:

- Hoy.
- Esta semana.
- Anteriores.

Ambas vistas permiten filtrar por grupo y buscar por referencia, asunto, empresa o responsable. No existe una operación para procesar o revertir una PMP.

## Estado y persistencia

| Dato                      | Ubicación                             | Persistencia                  |
| ------------------------- | ------------------------------------- | ----------------------------- |
| Solicitudes del usuario   | Entidad `mir-request` con `useState`. | Solo navegación de la sesión. |
| Secuencia de referencias  | `useState` separado.                  | Solo navegación de la sesión. |
| MIR y PMP administrativas | Arrays en el slice `admin`.           | Estáticos en el bundle.       |
| Preferencias del sidebar  | `UDashboardGroup` con `storage-key`.  | Gestionada por Nuxt UI.       |
| Contenido de adjuntos     | No se almacena.                       | Ninguna.                      |

## Límites funcionales actuales

- No existe inicio de sesión ni control de roles.
- No existe backend ni API.
- No existe base de datos.
- No existe subida real de archivos.
- No existe un timeline posterior a la creación.
- No existe comunicación entre portal de usuario y administración.
- No existe paginación, orden remoto ni búsqueda remota.
- Las vistas administrativas son principalmente de consulta.
