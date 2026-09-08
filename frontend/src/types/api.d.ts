export interface paths {
    "/mir": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Listar */
        get: operations["listar_mir_get"];
        put?: never;
        /** Crear */
        post: operations["crear_mir_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/mir/{mir_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Obtener */
        get: operations["obtener_mir__mir_id__get"];
        /** Actualizar */
        put: operations["actualizar_mir__mir_id__put"];
        post?: never;
        /** Eliminar */
        delete: operations["eliminar_mir__mir_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/archivos/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Listar Archivos */
        get: operations["listar_archivos_archivos__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/archivos/{documento_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /** Eliminar Archivo */
        delete: operations["eliminar_archivo_archivos__documento_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** ActualizarMirDTO */
        ActualizarMirDTO: {
            /** Descripcion */
            descripcion: string;
            solucionado: components["schemas"]["Solucionado"];
            /** Nombre Empresa */
            nombre_empresa: string;
            prioridad: components["schemas"]["Prioridad"];
            /** Nombre Persona Empresa */
            nombre_persona_empresa: string;
            /** Telefono Empresa */
            telefono_empresa: number;
            /** Codigo Cliente */
            codigo_cliente: string;
            /** Correo Cliente */
            correo_cliente: string;
            /**
             * Fecha Deteccion
             * Format: date
             */
            fecha_deteccion: string;
            /** Documento Ids */
            documento_ids?: string[];
        };
        /** Body_crear_mir_post */
        Body_crear_mir_post: {
            /** Datos */
            datos: string;
            /** Archivos */
            archivos?: string[] | null;
        };
        /** CrearMirDTO */
        CrearMirDTO: {
            /** Descripcion */
            descripcion: string;
            solucionado: components["schemas"]["Solucionado"];
            /** Nombre Empresa */
            nombre_empresa: string;
            prioridad: components["schemas"]["Prioridad"];
            /** Nombre Persona Empresa */
            nombre_persona_empresa: string;
            /** Telefono Empresa */
            telefono_empresa: number;
            /** Codigo Cliente */
            codigo_cliente: string;
            /** Correo Cliente */
            correo_cliente: string;
            /**
             * Fecha Deteccion
             * Format: date
             */
            fecha_deteccion: string;
            /** Tipos Documento */
            tipos_documento?: components["schemas"]["TipoDocumento"][];
        };
        /** DocumentoDTO */
        DocumentoDTO: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Nombre */
            nombre: string;
            tipo: components["schemas"]["TipoDocumento"];
            /** Storage Id */
            storage_id: string;
            /**
             * Creado Por
             * Format: uuid
             */
            creado_por: string;
            /**
             * Creado En
             * Format: date-time
             */
            creado_en: string;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** MirDTO */
        MirDTO: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Descripcion */
            descripcion: string;
            solucionado: components["schemas"]["Solucionado"];
            /** Archivos Adjuntos */
            archivos_adjuntos: components["schemas"]["DocumentoDTO"][];
            /** Nombre Empresa */
            nombre_empresa: string;
            prioridad: components["schemas"]["Prioridad"];
            /** Nombre Persona Empresa */
            nombre_persona_empresa: string;
            /** Telefono Empresa */
            telefono_empresa: number;
            /** Codigo Cliente */
            codigo_cliente: string;
            /** Correo Cliente */
            correo_cliente: string;
            /**
             * Fecha Deteccion
             * Format: date
             */
            fecha_deteccion: string;
        };
        /**
         * Prioridad
         * @enum {string}
         */
        Prioridad: "alta" | "media" | "baja";
        /**
         * Solucionado
         * @enum {string}
         */
        Solucionado: "si" | "no";
        /**
         * TipoDocumento
         * @enum {string}
         */
        TipoDocumento: "pdf" | "word" | "excel" | "imagen" | "otro";
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
            /** Input */
            input?: unknown;
            /** Context */
            ctx?: Record<string, never>;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    listar_mir_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MirDTO"][];
                };
            };
        };
    };
    crear_mir_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "multipart/form-data": components["schemas"]["Body_crear_mir_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MirDTO"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    obtener_mir__mir_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                mir_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MirDTO"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    actualizar_mir__mir_id__put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                mir_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActualizarMirDTO"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MirDTO"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    eliminar_mir__mir_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                mir_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    listar_archivos_archivos__get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentoDTO"][];
                };
            };
        };
    };
    eliminar_archivo_archivos__documento_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                documento_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
