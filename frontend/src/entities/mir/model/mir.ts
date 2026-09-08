import type { components } from "@/types/api";

export type TipoDocumento = components["schemas"]["TipoDocumento"];
export type MirDTO = components["schemas"]["MirDTO"];
export type Prioridad = components["schemas"]["Prioridad"];

export type CrearMirInput = Omit<components["schemas"]["CrearMirDTO"], "tipos_documento">;

const EXTENSION_TIPOS: Record<string, TipoDocumento> = {
  pdf: "pdf",
  doc: "word",
  docx: "word",
  xls: "excel",
  xlsx: "excel",
  png: "imagen",
  jpg: "imagen",
  jpeg: "imagen",
  gif: "imagen",
  webp: "imagen",
};

export const inferirTipoDocumento = (nombreArchivo: string): TipoDocumento => {
  const extension = nombreArchivo.split(".").pop()?.toLowerCase() ?? "";
  return EXTENSION_TIPOS[extension] ?? "otro";
};

export const crearMir = (datos: CrearMirInput, archivos: File[] = []): Promise<MirDTO> => {
  const {
    public: { apiBase },
  } = useRuntimeConfig();
  const body = new FormData();
  const tiposDocumento = archivos.map(({ name }) => inferirTipoDocumento(name));

  body.append("datos", JSON.stringify({ ...datos, tipos_documento: tiposDocumento }));
  for (const archivo of archivos) {
    body.append("archivos", archivo);
  }

  return $fetch<MirDTO>("/mir", { baseURL: apiBase, method: "POST", body });
};

export const listarMir = (): Promise<MirDTO[]> => {
  const {
    public: { apiBase },
  } = useRuntimeConfig();

  return $fetch<MirDTO[]>("/mir", { baseURL: apiBase });
};
