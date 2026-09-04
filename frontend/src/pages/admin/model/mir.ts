export type MirView = 'pending' | 'closed'
export type MirTone = 'neutral' | 'success' | 'warning' | 'error'
export type MirPriority = 'Alta' | 'Media' | 'Normal'
export type MirQueue = 'Usuario' | 'CAL' | 'Responsable' | 'Ejecutor' | 'CAL C.E.'

export interface MirRecord {
  reference: string
  subject: string
  company: string
  owner: string
  executor: string
  queue: MirQueue
  department: string
  date: string
  daysOpen: number
  status: string
  tone: MirTone
  priority: MirPriority
  priorityTone: MirTone
}

export interface MirDocument {
  name: string
  reference: string
  company: string
  type: 'Informe' | 'Evidencia' | 'Acta' | 'Respuesta'
  size: string
  uploadedBy: string
  date: string
}

export interface MirCompany {
  name: string
  pending: number
  highPriority: number
  closed: number
  total: number
}

export const pendingMirRecords: MirRecord[] = [
  { reference: 'MIR-2026-1842', subject: 'Desviación en el control documental', company: 'Euromed, S.A.', owner: 'Amparo Úbeda', executor: 'Vicente Carbonell', queue: 'Usuario', department: 'Línea laboratorio', date: '4 may 2026', daysOpen: 12, status: 'En resolución', tone: 'warning', priority: 'Alta', priorityTone: 'error' },
  { reference: 'MIR-2026-1839', subject: 'Incidencia con proveedor de reactivos', company: 'Martínez y Canto SL', owner: 'Alicia Trigueros', executor: 'Alicia Trigueros', queue: 'CAL', department: 'Calidad', date: '29 abr 2026', daysOpen: 10, status: 'Revisión CAL', tone: 'warning', priority: 'Alta', priorityTone: 'error' },
  { reference: 'MIR-2026-1837', subject: 'Resultado fuera de especificación', company: 'Laboratorios Uno', owner: 'Carme Porcar', executor: 'Ester Gallego', queue: 'Responsable', department: 'Microbiología', date: '27 abr 2026', daysOpen: 9, status: 'Técnico asignado', tone: 'neutral', priority: 'Alta', priorityTone: 'error' },
  { reference: 'MIR-2026-1834', subject: 'Error de trazabilidad de una muestra', company: 'BioMed Iberia', owner: 'Amparo Úbeda', executor: 'Carme Porcar', queue: 'Ejecutor', department: 'Línea laboratorio', date: '25 abr 2026', daysOpen: 8, status: 'En resolución', tone: 'warning', priority: 'Media', priorityTone: 'warning' },
  { reference: 'MIR-2026-1831', subject: 'Reclamación por retraso de entrega', company: 'Eurogrup', owner: 'Sonia Marco', executor: 'Sonia Marco', queue: 'CAL C.E.', department: 'Atención al cliente', date: '24 abr 2026', daysOpen: 7, status: 'Revisión CAL', tone: 'warning', priority: 'Media', priorityTone: 'warning' },
  { reference: 'MIR-2026-1829', subject: 'Temperatura incorrecta en recepción', company: 'Euromed, S.A.', owner: 'Rosa Sanjuan', executor: 'Rosa Sanjuan', queue: 'Usuario', department: 'Recepción', date: '22 abr 2026', daysOpen: 6, status: 'En resolución', tone: 'warning', priority: 'Media', priorityTone: 'warning' },
  { reference: 'MIR-2026-1826', subject: 'Documentación incompleta del lote', company: 'TecnoCalidad', owner: 'María Frontera', executor: 'Manuela Sabao', queue: 'CAL', department: 'Calidad', date: '20 abr 2026', daysOpen: 5, status: 'Revisión CAL', tone: 'warning', priority: 'Normal', priorityTone: 'neutral' },
  { reference: 'MIR-2026-1824', subject: 'Fallo puntual en equipo de medida', company: 'FarmaSur', owner: 'Cecilia Medina', executor: 'Cecilia Medina', queue: 'Ejecutor', department: 'Instrumentación', date: '18 abr 2026', daysOpen: 4, status: 'Técnico asignado', tone: 'neutral', priority: 'Media', priorityTone: 'warning' },
  { reference: 'MIR-2026-1821', subject: 'Diferencia en el etiquetado final', company: 'Euromed, S.A.', owner: 'Irene Llorca', executor: 'Irene Llorca', queue: 'Responsable', department: 'Producción', date: '17 abr 2026', daysOpen: 3, status: 'En resolución', tone: 'warning', priority: 'Normal', priorityTone: 'neutral' },
  { reference: 'MIR-2026-1818', subject: 'Registro de limpieza sin firma', company: 'Laboratorios Uno', owner: 'Carme Porcar', executor: 'Carme Porcar', queue: 'CAL C.E.', department: 'Calidad', date: '15 abr 2026', daysOpen: 2, status: 'Revisión CAL', tone: 'warning', priority: 'Normal', priorityTone: 'neutral' }
]

export const closedMirRecords: MirRecord[] = [
  { reference: 'MIR-2026-1815', subject: 'Daño en embalaje durante transporte', company: 'Euromed, S.A.', owner: 'Amparo Úbeda', executor: 'Vicente Carbonell', queue: 'Responsable', department: 'Logística', date: 'Cerrada hoy', daysOpen: 6, status: 'Cerrada', tone: 'success', priority: 'Media', priorityTone: 'warning' },
  { reference: 'MIR-2026-1812', subject: 'Certificado de análisis incorrecto', company: 'BioMed Iberia', owner: 'Alicia Trigueros', executor: 'Alicia Trigueros', queue: 'CAL', department: 'Calidad', date: 'Cerrada ayer', daysOpen: 5, status: 'Cerrada', tone: 'success', priority: 'Alta', priorityTone: 'error' },
  { reference: 'MIR-2026-1808', subject: 'Incidencia en la toma de muestra', company: 'Laboratorios Uno', owner: 'Carme Porcar', executor: 'Ester Gallego', queue: 'Ejecutor', department: 'Microbiología', date: '12 ago 2026', daysOpen: 4, status: 'Cerrada', tone: 'success', priority: 'Normal', priorityTone: 'neutral' },
  { reference: 'MIR-2026-1803', subject: 'Entrega de documentación duplicada', company: 'Eurogrup', owner: 'Sonia Marco', executor: 'Sonia Marco', queue: 'Usuario', department: 'Administración', date: '9 ago 2026', daysOpen: 8, status: 'Cerrada', tone: 'success', priority: 'Normal', priorityTone: 'neutral' },
  { reference: 'MIR-2026-1797', subject: 'Valor incorrecto en informe final', company: 'Euromed, S.A.', owner: 'Rosa Sanjuan', executor: 'Rosa Sanjuan', queue: 'CAL C.E.', department: 'Calidad', date: '5 ago 2026', daysOpen: 7, status: 'Cerrada', tone: 'success', priority: 'Media', priorityTone: 'warning' },
  { reference: 'MIR-2026-1791', subject: 'Retraso en validación de resultados', company: 'FarmaSur', owner: 'Cecilia Medina', executor: 'Cecilia Medina', queue: 'Responsable', department: 'Instrumentación', date: '1 ago 2026', daysOpen: 9, status: 'Cerrada', tone: 'success', priority: 'Alta', priorityTone: 'error' }
]

export const mirDocuments: MirDocument[] = [
  { name: 'informe-desviacion-documental.pdf', reference: 'MIR-2026-1842', company: 'Euromed, S.A.', type: 'Informe', size: '1,8 MB', uploadedBy: 'Amparo Úbeda', date: '4 may 2026' },
  { name: 'evidencia-reactivos-recepcion.jpg', reference: 'MIR-2026-1839', company: 'Martínez y Canto SL', type: 'Evidencia', size: '846 KB', uploadedBy: 'Alicia Trigueros', date: '29 abr 2026' },
  { name: 'acta-revision-cal.pdf', reference: 'MIR-2026-1839', company: 'Martínez y Canto SL', type: 'Acta', size: '522 KB', uploadedBy: 'Alicia Trigueros', date: '28 abr 2026' },
  { name: 'resultados-microbiologia.xlsx', reference: 'MIR-2026-1837', company: 'Laboratorios Uno', type: 'Evidencia', size: '138 KB', uploadedBy: 'Carme Porcar', date: '27 abr 2026' },
  { name: 'respuesta-proveedor.pdf', reference: 'MIR-2026-1831', company: 'Eurogrup', type: 'Respuesta', size: '734 KB', uploadedBy: 'Sonia Marco', date: '25 abr 2026' },
  { name: 'registro-temperatura.pdf', reference: 'MIR-2026-1829', company: 'Euromed, S.A.', type: 'Evidencia', size: '312 KB', uploadedBy: 'Rosa Sanjuan', date: '22 abr 2026' },
  { name: 'informe-cierre-1815.pdf', reference: 'MIR-2026-1815', company: 'Euromed, S.A.', type: 'Informe', size: '1,2 MB', uploadedBy: 'Vicente Carbonell', date: '20 abr 2026' },
  { name: 'acta-validacion-resultados.pdf', reference: 'MIR-2026-1791', company: 'FarmaSur', type: 'Acta', size: '688 KB', uploadedBy: 'Cecilia Medina', date: '1 ago 2026' }
]

export const pendingMirCount = pendingMirRecords.length

const allMirRecords: MirRecord[] = [...pendingMirRecords, ...closedMirRecords]

export const mirCompanies: MirCompany[] = [...new Set(allMirRecords.map(record => record.company))]
  .map((name) => {
    const pending: MirRecord[] = pendingMirRecords.filter(record => record.company === name)
    const closed: number = closedMirRecords.filter(record => record.company === name).length

    return {
      name,
      pending: pending.length,
      highPriority: pending.filter(record => record.priority === 'Alta').length,
      closed,
      total: pending.length + closed
    }
  })
  .sort((companyA, companyB) => companyB.pending - companyA.pending || companyB.highPriority - companyA.highPriority)
