# Guía de desarrollo

## Requisitos

- Node.js compatible con la versión instalada de Nuxt 4.
- pnpm `11.22.0`, indicado en `package.json`.

No cambies de gestor de paquetes: el lockfile mantenido es `pnpm-lock.yaml`.

## Instalación y ejecución

```bash
pnpm install
pnpm dev
```

Comandos disponibles:

| Comando             | Uso                                                        |
| ------------------- | ---------------------------------------------------------- |
| `pnpm dev`          | Servidor de desarrollo.                                    |
| `pnpm build`        | Build de producción con Nuxt y Nitro.                      |
| `pnpm preview`      | Sirve localmente el último build.                          |
| `pnpm lint`         | Analiza el repositorio con Oxlint.                         |
| `pnpm lint:fix`     | Corrige automáticamente incidencias compatibles de Oxlint. |
| `pnpm format`       | Formatea el repositorio con Oxfmt.                         |
| `pnpm format:check` | Comprueba el formato sin modificar archivos.               |
| `pnpm typecheck`    | Comprueba Vue y TypeScript mediante Nuxt.                  |
| `pnpm check`        | Ejecuta lint, formato y typecheck.                         |

Antes de entregar código:

```bash
pnpm check
pnpm build
```

No existe todavía una suite automatizada de tests.

## Convenciones de código

### TypeScript

- Usa `lang="ts"` en componentes Vue.
- Declara interfaces y uniones de dominio de forma explícita.
- Evita `any` y casts que oculten errores.
- Usa `satisfies` cuando necesites validar una estructura sin perder inferencia.
- Mantén las fechas de dominio en formato ISO y formatéalas al presentar.

### Vue y Nuxt

- Usa Composition API con `<script setup>`.
- Aprovecha autoimports de Nuxt para `ref`, `computed`, `watch`, `useRoute`, `navigateTo` y `useState`.
- Mantén las entradas de ruta delgadas.
- Usa `definePageMeta` para layout y modo de color.
- Evita acceder a APIs del navegador durante SSR sin una guarda de cliente.
- Usa claves globalmente únicas y estables en `useState`.

### UI

- Reutiliza Nuxt UI antes de crear componentes base propios.
- Usa utilidades Tailwind mobile-first.
- Conserva Public Sans, la paleta naranja y el canvas oscuro salvo cambio de diseño global.
- No uses solo color para comunicar un estado; acompáñalo con texto o icono.
- Todo control de icono necesita nombre accesible.
- Todo formulario necesita etiquetas y errores identificables.
- Mantén objetivos táctiles de al menos 24 por 24 píxeles.
- Verifica teclado, foco visible, zoom y móvil.

### Nombres

- Slices y carpetas: kebab-case, por ejemplo `mir-request-details`.
- Componentes Vue: PascalCase, por ejemplo `MirRequestDetailsPage.vue`.
- Archivos de modelo: nombre del dominio, no `types.ts`, `utils.ts` o `helpers.ts` genéricos.
- APIs públicas: `index.ts` en cada slice.

## Reglas FSD obligatorias

```text
app → pages → entities → shared
```

1. No importes una capa superior desde una inferior.
2. No importes entre slices hermanos de `pages`.
3. Importa un slice desde su `index.ts` público.
4. No accedas desde fuera a `ui/` o `model/` internos.
5. Mantén lógica de una sola pantalla dentro de su página.
6. Extrae una entidad solo cuando el modelo se comparta entre varias páginas.
7. Extrae un feature solo cuando la misma interacción se reutilice realmente.
8. No crees carpetas vacías ni abstracciones para necesidades futuras.

Ejemplo correcto:

```ts
import { useMirRequests } from "@/entities/mir-request";
```

Ejemplo incorrecto:

```ts
import { useMirRequests } from "@/entities/mir-request/model/mir-request";
```

## Añadir una página

Para una nueva pantalla independiente:

1. Crea `src/pages/<slice>/ui/<PageName>.vue`.
2. Mantén ahí su comportamiento local.
3. Crea `src/pages/<slice>/index.ts` y exporta el componente.
4. Crea una entrada delgada en `src/app/routes`.
5. Importa la página desde `@/pages/<slice>`.
6. Selecciona `default` o `usuario` mediante `definePageMeta`.
7. Añade una regla de prerender solo si la ruta es determinista durante build.

Ejemplo de entrada de ruta:

```vue
<script setup lang="ts">
import { ExamplePage } from "@/pages/example";

definePageMeta({
  layout: "usuario",
  colorMode: "dark",
});
</script>

<template>
  <ExamplePage />
</template>
```

## Añadir o ampliar una entidad

Usa `entities` cuando varias páginas necesiten el mismo modelo estable.

1. Crea `src/entities/<entity>/model/<entity>.ts`.
2. Coloca tipos y reglas del dominio en ese modelo.
3. Expón únicamente lo necesario desde `src/entities/<entity>/index.ts`.
4. Importa siempre desde la API pública.
5. No incluyas componentes de una página dentro de la entidad.

Si solo una página necesita el dato o la operación, mantenlo en la página.

## Añadir infraestructura compartida

Usa `shared` para código sin reglas del dominio:

| Tipo                                           | Ubicación recomendada |
| ---------------------------------------------- | --------------------- |
| Componentes visuales genéricos reutilizados    | `src/shared/ui/`      |
| Formateadores y funciones técnicas             | `src/shared/lib/`     |
| Cliente HTTP y contratos básicos de transporte | `src/shared/api/`     |
| Configuración y constantes globales            | `src/shared/config/`  |
| Sesión y tokens de autenticación               | `src/shared/auth/`    |

Cada segmento de `shared` debe exponer su propia API pública. No crees un `src/shared/index.ts` global.

## Sustituir mocks por una API

La migración debería realizarse sin hacer que las páginas conozcan detalles de transporte:

1. Define el cliente HTTP en `shared/api`.
2. Define el contrato real de MIR y resuelve la diferencia entre `MirRequest` y `MirRecord`.
3. Sustituye los arrays administrativos por consultas.
4. Sustituye `useState` como fuente de verdad del usuario por datos remotos.
5. Mantén estados de carga, vacío y error en las páginas consumidoras.
6. Implementa la subida real con validación de tipo, tamaño y permisos en servidor.
7. Añade autorización en servidor; ocultar enlaces no es una medida de seguridad.
8. Elimina los mocks cuando ya no tengan consumidores.

No mantengas indefinidamente dos caminos, mock y real, salvo que exista una necesidad concreta de demo o desarrollo aislado.

## Seguridad pendiente

Antes de considerar la aplicación productiva se necesita:

- Autenticación.
- Roles para usuario y administración.
- Autorización de cada solicitud en servidor.
- Validación de todos los inputs en el límite de confianza.
- Validación y almacenamiento seguro de archivos.
- Control de referencias generado por backend o base de datos.
- Registro de eventos del timeline en una fuente durable.

El mensaje actual de solicitud no encontrada no demuestra propiedad. La comprobación real debe realizarse en servidor usando la identidad autenticada.

## Tests recomendados al incorporar backend

No añadas una suite grande antes de necesitarla. Los primeros tests con valor deberían cubrir:

- Un usuario no puede leer solicitudes de otro usuario.
- La creación rechaza inputs inválidos.
- La referencia no se duplica con concurrencia.
- Un archivo inválido no se almacena.
- Los eventos de timeline conservan orden y autor.
- Los filtros principales presentan los registros correctos.

## Limitaciones conocidas

- Datos de usuario y administración separados y potencialmente inconsistentes.
- Estado del usuario perdido al recargar.
- Año y secuencia de referencias hardcodeados en el mock.
- Validación del formulario basada en atributos HTML, sin esquema compartido.
- Sin límite de cantidad o tamaño de adjuntos.
- Un único estado y evento de timeline para el usuario.
- Sin API, autenticación, permisos ni persistencia.
- Botones administrativos todavía decorativos.
- Sin tests automatizados.
- Sin títulos y metadatos específicos por ruta.
