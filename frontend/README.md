# Circuito MIR Frontend

Aplicación Nuxt para consultar y gestionar el circuito de mejoras, incidencias, reclamaciones (MIR) y propuestas de mejora preventiva (PMP).

Actualmente incluye dos áreas:

- Portal de usuario en `/usuario`, para crear solicitudes MIR y consultar su seguimiento.
- Panel administrativo en `/admin`, para consultar MIR, PMP, documentos y empresas.

La aplicación es un prototipo frontend: usa datos mock y no dispone todavía de autenticación, API ni persistencia real.

## Inicio rápido

```bash
pnpm install
pnpm dev
```

El servidor de desarrollo estará disponible en `http://localhost:3000`.

## Documentación

- [Índice de documentación](./docs/README.md)
- [Arquitectura y estructura](./docs/architecture.md)
- [Funcionamiento y flujos](./docs/application-flows.md)
- [Guía de desarrollo](./docs/development.md)

## Comprobaciones

```bash
pnpm check
pnpm build
```
