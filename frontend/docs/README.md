# Documentación de Circuito MIR

Esta documentación describe el estado actual del frontend para que una persona nueva pueda entenderlo, ejecutarlo y ampliarlo sin romper sus límites arquitectónicos.

## Documentos

| Documento                                         | Contenido                                                                                                |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [Arquitectura y estructura](./architecture.md)    | Capas FSD, dependencias, árbol de carpetas, responsabilidad de cada archivo y flujo de datos.            |
| [Funcionamiento y flujos](./application-flows.md) | Rutas, pantallas, navegación, filtros y comportamiento del portal de usuario y del panel administrativo. |
| [Guía de desarrollo](./development.md)            | Instalación, comandos, convenciones, recetas para añadir código y limitaciones conocidas.                |

## Lectura recomendada

1. Lee [Arquitectura y estructura](./architecture.md) antes de mover o crear archivos.
2. Consulta [Funcionamiento y flujos](./application-flows.md) para conocer el comportamiento visible.
3. Sigue [Guía de desarrollo](./development.md) antes de abrir una entrega.

## Estado del producto

El repositorio contiene una interfaz funcional construida con datos mock. No existe todavía backend, autenticación, autorización, almacenamiento de archivos ni persistencia de solicitudes.

Esto implica que:

- Las URLs de usuario y administración no están protegidas.
- Las solicitudes creadas se pierden al recargar la aplicación.
- Los datos del portal de usuario y del panel administrativo no se sincronizan.
- Los botones sin manejador son demostraciones visuales, no operaciones reales.

Estas restricciones deben conservarse visibles en la documentación hasta que una implementación real las sustituya.
