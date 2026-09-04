export type MirRequestStatus = "Creada";

export interface MirRequestAttachment {
  name: string;
  size: number;
}

export interface MirRequest {
  id: string;
  reference: string;
  createdBy: string;
  detectionDate: string;
  detectedBy: string;
  description: string;
  resolved: boolean;
  company: string;
  contactPerson: string;
  phone: string;
  email: string;
  customerCode: string;
  status: MirRequestStatus;
  createdAt: string;
  attachments: MirRequestAttachment[];
}

export interface CreateMirRequestInput {
  createdBy: string;
  detectionDate: string;
  detectedBy: string;
  description: string;
  resolved: boolean;
  company: string;
  contactPerson: string;
  phone: string;
  email: string;
  customerCode: string;
  attachments: MirRequestAttachment[];
}

const initialMirRequests: MirRequest[] = [
  {
    id: "mir-2026-1842",
    reference: "MIR-2026-1842",
    createdBy: "PABLO SANTIAGO/AINIALAN",
    detectionDate: "2026-08-21",
    detectedBy: "PABLO SANTIAGO/AINIALAN",
    description:
      "Se ha detectado una diferencia entre la versión aprobada del procedimiento y la copia disponible en el puesto de trabajo.",
    resolved: false,
    company: "Euromed, S.A.",
    contactPerson: "María García",
    phone: "963 000 001",
    email: "maria.garcia@euromed.es",
    customerCode: "EU-1042",
    status: "Creada",
    createdAt: "2026-08-21T08:35:00.000Z",
    attachments: [{ name: "evidencia-documental.pdf", size: 1843200 }],
  },
  {
    id: "mir-2026-1838",
    reference: "MIR-2026-1838",
    createdBy: "PABLO SANTIAGO/AINIALAN",
    detectionDate: "2026-08-18",
    detectedBy: "PABLO SANTIAGO/AINIALAN",
    description:
      "El informe final no se ha recibido en la fecha acordada y necesitamos confirmar la nueva previsión de entrega.",
    resolved: false,
    company: "Laboratorios Uno",
    contactPerson: "Juan Pérez",
    phone: "961 000 210",
    email: "juan.perez@laboratoriosuno.es",
    customerCode: "LU-2081",
    status: "Creada",
    createdAt: "2026-08-18T14:10:00.000Z",
    attachments: [],
  },
  {
    id: "mir-2026-1827",
    reference: "MIR-2026-1827",
    createdBy: "PABLO SANTIAGO/AINIALAN",
    detectionDate: "2026-08-12",
    detectedBy: "PABLO SANTIAGO/AINIALAN",
    description:
      "Las etiquetas internas no incluyen la referencia de recepción y dificultan el seguimiento completo de cada muestra.",
    resolved: true,
    company: "BioMed Iberia",
    contactPerson: "Laura Martínez",
    phone: "960 000 403",
    email: "laura.martinez@biomediberia.es",
    customerCode: "BI-3094",
    status: "Creada",
    createdAt: "2026-08-12T09:20:00.000Z",
    attachments: [{ name: "propuesta-etiquetado.pdf", size: 638976 }],
  },
];

export const useMirRequests = () => {
  const requests = useState<MirRequest[]>("user-mir-requests", () =>
    structuredClone(initialMirRequests),
  );
  const sequence = useState<number>("user-mir-request-sequence", () => 1842);

  const createMirRequest = (input: CreateMirRequestInput): MirRequest => {
    const reference = `MIR-2026-${++sequence.value}`;
    const request: MirRequest = {
      ...input,
      id: reference.toLocaleLowerCase("es"),
      reference,
      status: "Creada",
      createdAt: new Date().toISOString(),
    };

    requests.value.unshift(request);
    return request;
  };

  const getMirRequestById = (id: string): MirRequest | undefined =>
    requests.value.find((request) => request.id === id);

  return {
    requests: readonly(requests),
    createMirRequest,
    getMirRequestById,
  };
};
