import type { components } from "@/types/api";

export type DocumentoDTO = components["schemas"]["DocumentoDTO"];

export const obtenerDocumentos = (): Promise<DocumentoDTO[]> => {
  const {
    public: { apiBase },
  } = useRuntimeConfig();

  return $fetch<DocumentoDTO[]>("/archivos/", { baseURL: apiBase });
};
