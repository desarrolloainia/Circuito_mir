import { unprocessedPmpCount } from './pmp'
import { pendingMirCount } from './mir'

export type DashboardStatusTone = 'success' | 'warning' | 'error'

export interface DashboardMetric {
  label: string
  value: string
  note: string
  icon: string
}

export interface DashboardActivity {
  reference: string
  type: 'MIR' | 'PMP'
  subject: string
  owner: string
  status: string
  tone: DashboardStatusTone
  updated: string
}

export interface DashboardQuickAction {
  title: string
  description: string
  icon: string
}

export interface DashboardPendingArea {
  area: string
  count: number
  percentage: number
}

export const dashboardMetrics: DashboardMetric[] = [
  { label: 'PMP sin procesar', value: String(unprocessedPmpCount), note: '4 asignadas a tu usuario', icon: 'i-lucide-inbox' },
  { label: 'MIR pendientes', value: String(pendingMirCount), note: '3 con prioridad alta', icon: 'i-lucide-clock-3' },
  { label: 'Cerradas este mes', value: '47', note: '+18% frente al mes anterior', icon: 'i-lucide-circle-check-big' },
  { label: 'Tiempo medio', value: '3,4 d', note: 'Hasta resolución', icon: 'i-lucide-timer' }
]

export const dashboardActivities: DashboardActivity[] = [
  { reference: 'MIR-2026-1842', type: 'MIR', subject: 'Desviación documental', owner: 'Marta López', status: 'Pendiente', tone: 'warning', updated: 'Hace 18 min' },
  { reference: 'PMP-2026-0921', type: 'PMP', subject: 'Mejora trazabilidad', owner: 'Carlos Ruiz', status: 'Procesada', tone: 'success', updated: 'Hace 43 min' },
  { reference: 'MIR-2026-1839', type: 'MIR', subject: 'Incidencia proveedor', owner: 'Ana Torres', status: 'Alta prioridad', tone: 'error', updated: 'Hace 1 h' },
  { reference: 'MIR-2026-1835', type: 'MIR', subject: 'Revisión plan de acción', owner: 'David Pérez', status: 'Cerrada', tone: 'success', updated: 'Ayer' }
]

export const dashboardQuickActions: DashboardQuickAction[] = [
  { title: 'Nueva MIR', description: 'Registrar una incidencia, mejora o reclamación.', icon: 'i-lucide-circle-plus' },
  { title: 'Nueva PMP', description: 'Crear una propuesta de mejora preventiva.', icon: 'i-lucide-file-plus-2' },
  { title: 'Buscar expediente', description: 'Localizar documentos por usuario o empresa.', icon: 'i-lucide-search' }
]

export const dashboardPendingAreas: DashboardPendingArea[] = [
  { area: 'Usuario', count: 9, percentage: 32 },
  { area: 'CAL', count: 7, percentage: 25 },
  { area: 'Responsable', count: 6, percentage: 21 },
  { area: 'Ejecutor', count: 4, percentage: 14 },
  { area: '+7 días', count: 2, percentage: 8 }
]
