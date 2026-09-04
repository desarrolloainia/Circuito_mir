export type PmpView = 'unprocessed' | 'processed'
export type PmpTone = 'neutral' | 'success' | 'warning' | 'error'
export type PmpGroup = 'Vencidas' | 'Próximas' | 'Recientes' | 'Hoy' | 'Esta semana' | 'Anteriores'

export interface PmpRecord {
  reference: string
  subject: string
  company: string
  owner: string
  date: string
  group: PmpGroup
  status: string
  tone: PmpTone
}

export interface PmpGroupDefinition {
  label: PmpGroup
  description: string
  icon: string
  tone: PmpTone
}

export const unprocessedPmpGroups: PmpGroupDefinition[] = [
  { label: 'Vencidas', description: 'Más de 7 días sin procesar', icon: 'i-lucide-triangle-alert', tone: 'error' },
  { label: 'Próximas', description: 'Entre 3 y 7 días en espera', icon: 'i-lucide-clock-3', tone: 'warning' },
  { label: 'Recientes', description: 'Recibidas durante los últimos 3 días', icon: 'i-lucide-sparkles', tone: 'neutral' }
]

export const processedPmpGroups: PmpGroupDefinition[] = [
  { label: 'Hoy', description: 'Procesadas durante la jornada', icon: 'i-lucide-calendar-check-2', tone: 'success' },
  { label: 'Esta semana', description: 'Procesadas en los últimos 7 días', icon: 'i-lucide-calendar-days', tone: 'neutral' },
  { label: 'Anteriores', description: 'Procesadas antes de esta semana', icon: 'i-lucide-archive', tone: 'neutral' }
]

export const unprocessedPmpRecords: PmpRecord[] = [
  { reference: 'PMP-2026-1048', subject: 'Actualización del protocolo de recepción', company: 'Logística Norte', owner: 'Marta López', date: 'Hace 12 días', group: 'Vencidas', status: 'Vencida', tone: 'error' },
  { reference: 'PMP-2026-1045', subject: 'Control de temperatura en almacén', company: 'FarmaSur', owner: 'Ana Torres', date: 'Hace 10 días', group: 'Vencidas', status: 'Vencida', tone: 'error' },
  { reference: 'PMP-2026-1042', subject: 'Revisión de homologación de proveedores', company: 'TecnoCalidad', owner: 'Usuario MIR', date: 'Hace 8 días', group: 'Vencidas', status: 'Vencida', tone: 'error' },
  { reference: 'PMP-2026-1055', subject: 'Trazabilidad de lotes devueltos', company: 'Alimentaria Centro', owner: 'Carlos Ruiz', date: 'Hace 6 días', group: 'Próximas', status: 'Próxima', tone: 'warning' },
  { reference: 'PMP-2026-1053', subject: 'Digitalización del registro de mantenimiento', company: 'Envases Levante', owner: 'Usuario MIR', date: 'Hace 5 días', group: 'Próximas', status: 'Próxima', tone: 'warning' },
  { reference: 'PMP-2026-1051', subject: 'Validación de documentación externa', company: 'BioMed Iberia', owner: 'David Pérez', date: 'Hace 4 días', group: 'Próximas', status: 'Próxima', tone: 'warning' },
  { reference: 'PMP-2026-1049', subject: 'Mejora del control de no conformidades', company: 'Metalúrgica Sur', owner: 'Usuario MIR', date: 'Hace 3 días', group: 'Próximas', status: 'Próxima', tone: 'warning' },
  { reference: 'PMP-2026-1061', subject: 'Automatización de avisos de caducidad', company: 'Química Delta', owner: 'Marta López', date: 'Hace 2 días', group: 'Recientes', status: 'En plazo', tone: 'neutral' },
  { reference: 'PMP-2026-1060', subject: 'Nuevo checklist de expediciones', company: 'Distribuciones Vega', owner: 'Usuario MIR', date: 'Ayer', group: 'Recientes', status: 'En plazo', tone: 'neutral' },
  { reference: 'PMP-2026-1058', subject: 'Optimización de auditorías internas', company: 'Calidad Global', owner: 'Ana Torres', date: 'Hoy, 08:45', group: 'Recientes', status: 'En plazo', tone: 'neutral' }
]

export const processedPmpRecords: PmpRecord[] = [
  { reference: 'PMP-2026-1057', subject: 'Mejora del etiquetado de muestras', company: 'Laboratorios Uno', owner: 'Carlos Ruiz', date: 'Hoy, 11:32', group: 'Hoy', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1056', subject: 'Actualización de instrucciones de limpieza', company: 'Higiene Técnica', owner: 'Marta López', date: 'Hoy, 10:14', group: 'Hoy', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1054', subject: 'Control visual de embalajes', company: 'Pack Solutions', owner: 'Ana Torres', date: 'Hoy, 09:18', group: 'Hoy', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1052', subject: 'Registro digital de calibraciones', company: 'Metrología Centro', owner: 'David Pérez', date: 'Ayer, 16:40', group: 'Esta semana', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1050', subject: 'Revisión del circuito de devoluciones', company: 'Comercial Este', owner: 'Carlos Ruiz', date: 'Hace 2 días', group: 'Esta semana', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1047', subject: 'Mejora del archivo de certificados', company: 'Certifica SL', owner: 'Usuario MIR', date: 'Hace 4 días', group: 'Esta semana', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1046', subject: 'Estandarización del parte de incidencias', company: 'Servicios Atlas', owner: 'Marta López', date: 'Hace 6 días', group: 'Esta semana', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1041', subject: 'Seguimiento de acciones correctivas', company: 'Industria Nova', owner: 'Ana Torres', date: '12 ago 2026', group: 'Anteriores', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1038', subject: 'Revisión del plan de formación anual', company: 'Formación Integral', owner: 'David Pérez', date: '8 ago 2026', group: 'Anteriores', status: 'Procesada', tone: 'success' },
  { reference: 'PMP-2026-1034', subject: 'Simplificación del control documental', company: 'Gestión Clara', owner: 'Usuario MIR', date: '4 ago 2026', group: 'Anteriores', status: 'Procesada', tone: 'success' }
]

export const unprocessedPmpCount = unprocessedPmpRecords.length
