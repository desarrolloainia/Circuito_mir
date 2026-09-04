<script setup lang="ts">
import type { CommandPaletteGroup, CommandPaletteItem, NavigationMenuItem } from '@nuxt/ui'
import {
  closedMirRecords,
  mirCompanies,
  mirDocuments,
  pendingMirCount,
  pendingMirRecords,
  processedPmpRecords,
  unprocessedPmpCount,
  unprocessedPmpRecords
} from '@/pages/admin'

type SearchItem = CommandPaletteItem & { keywords?: string }

const sidebarOpen = ref(false)

const closeSidebar = () => {
  sidebarOpen.value = false
}

const generalLinks = [{
  label: 'Panel principal',
  icon: 'i-lucide-layout-dashboard',
  to: '/admin/dashboard',
  exact: true,
  onSelect: closeSidebar
}, {
  label: 'Nueva MIR',
  icon: 'i-lucide-circle-plus',
  disabled: true
}, {
  label: 'Nueva PMP',
  icon: 'i-lucide-file-plus-2',
  disabled: true
}] satisfies NavigationMenuItem[]

const pmpAlertColor: 'success' | 'warning' | 'error' = unprocessedPmpCount >= 10
  ? 'error'
  : unprocessedPmpCount >= 5 ? 'warning' : 'success'

const pmpLinks = [{
  label: 'Sin procesar',
  icon: 'i-lucide-inbox',
  to: '/admin/pmp/sin-procesar',
  exact: true,
  badge: {
    label: unprocessedPmpCount,
    color: pmpAlertColor,
    variant: 'subtle'
  },
  chip: unprocessedPmpCount > 0
    ? { color: pmpAlertColor, inset: true }
    : false,
  tooltip: { text: `${unprocessedPmpCount} PMP sin procesar` },
  onSelect: closeSidebar
}, {
  label: 'Procesadas',
  icon: 'i-lucide-circle-check-big',
  to: '/admin/pmp/procesadas',
  exact: true,
  onSelect: closeSidebar
}] satisfies NavigationMenuItem[]

const mirLinks = [{
  label: 'Pendientes',
  icon: 'i-lucide-clock-3',
  to: '/admin/mir/pendientes',
  exact: true,
  badge: {
    label: pendingMirCount,
    color: 'warning',
    variant: 'subtle'
  },
  onSelect: closeSidebar
}, {
  label: 'Cerradas',
  icon: 'i-lucide-badge-check',
  to: '/admin/mir/cerradas',
  exact: true,
  onSelect: closeSidebar
}, {
  label: 'Todos los documentos',
  icon: 'i-lucide-files',
  to: '/admin/mir/documentos',
  exact: true,
  onSelect: closeSidebar
}, {
  label: 'Todos por empresa',
  icon: 'i-lucide-building-2',
  to: '/admin/mir/empresas',
  exact: true,
  onSelect: closeSidebar
}] satisfies NavigationMenuItem[]

// ponytail: local in-memory indexing is enough for mocks; move this search to the API when records become remote.
const searchGroups: CommandPaletteGroup<SearchItem>[] = [{
  id: 'navigation',
  label: 'Ir a',
  items: [{
    label: 'Panel principal',
    icon: 'i-lucide-layout-dashboard',
    to: '/admin/dashboard'
  }, {
    label: 'PMP sin procesar',
    icon: 'i-lucide-inbox',
    to: '/admin/pmp/sin-procesar'
  }, {
    label: 'PMP procesadas',
    icon: 'i-lucide-circle-check-big',
    to: '/admin/pmp/procesadas'
  }, {
    label: 'MIR pendientes',
    icon: 'i-lucide-clock-3',
    to: '/admin/mir/pendientes'
  }, {
    label: 'MIR cerradas',
    icon: 'i-lucide-badge-check',
    to: '/admin/mir/cerradas'
  }, {
    label: 'Documentos MIR',
    icon: 'i-lucide-files',
    to: '/admin/mir/documentos'
  }, {
    label: 'MIR por empresa',
    icon: 'i-lucide-building-2',
    to: '/admin/mir/empresas'
  }, {
    label: 'Actividad reciente',
    icon: 'i-lucide-history',
    to: '/admin/dashboard#actividad-reciente'
  }, {
    label: 'Pendientes por área',
    icon: 'i-lucide-chart-no-axes-column',
    to: '/admin/dashboard#pendientes-area'
  }]
}, {
  id: 'pending-mir',
  label: 'MIR pendientes',
  items: pendingMirRecords.map(record => ({
    label: record.reference,
    description: `${record.subject} · ${record.company}`,
    suffix: record.status,
    keywords: [record.owner, record.executor, record.department, record.queue, record.priority, record.date].join(' '),
    icon: 'i-lucide-file-warning',
    to: { path: '/admin/mir/pendientes', query: { search: record.reference } }
  }))
}, {
  id: 'closed-mir',
  label: 'MIR cerradas',
  items: closedMirRecords.map(record => ({
    label: record.reference,
    description: `${record.subject} · ${record.company}`,
    suffix: record.status,
    keywords: [record.owner, record.executor, record.department, record.queue, record.priority, record.date].join(' '),
    icon: 'i-lucide-badge-check',
    to: { path: '/admin/mir/cerradas', query: { search: record.reference } }
  }))
}, {
  id: 'unprocessed-pmp',
  label: 'PMP sin procesar',
  items: unprocessedPmpRecords.map(record => ({
    label: record.reference,
    description: `${record.subject} · ${record.company}`,
    suffix: record.status,
    keywords: [record.owner, record.group, record.date].join(' '),
    icon: 'i-lucide-file-clock',
    to: { path: '/admin/pmp/sin-procesar', query: { search: record.reference } }
  }))
}, {
  id: 'processed-pmp',
  label: 'PMP procesadas',
  items: processedPmpRecords.map(record => ({
    label: record.reference,
    description: `${record.subject} · ${record.company}`,
    suffix: record.status,
    keywords: [record.owner, record.group, record.date].join(' '),
    icon: 'i-lucide-file-check-2',
    to: { path: '/admin/pmp/procesadas', query: { search: record.reference } }
  }))
}, {
  id: 'documents',
  label: 'Documentos MIR',
  items: mirDocuments.map(document => ({
    label: document.name,
    description: `${document.reference} · ${document.company}`,
    suffix: document.type,
    keywords: [document.uploadedBy, document.date, document.size].join(' '),
    icon: 'i-lucide-file-text',
    to: { path: '/admin/mir/documentos', query: { search: document.name } }
  }))
}, {
  id: 'companies',
  label: 'Empresas',
  items: mirCompanies.map(company => ({
    label: company.name,
    description: `${company.total} MIR · ${company.pending} pendientes`,
    suffix: `${company.highPriority} prioritarias`,
    icon: 'i-lucide-building-2',
    to: { path: '/admin/mir/empresas', query: { company: company.name } }
  }))
}]

const navigationUi = {
  label: 'px-2 text-[10px] font-bold tracking-[0.14em] text-slate-500 uppercase',
  link: 'text-slate-300 hover:bg-white/6 hover:text-white data-[active]:bg-white/10 data-[active]:text-white',
  linkLeadingIcon: 'text-slate-400 group-data-[active]:text-orange-400'
}
</script>

<template>
  <UDashboardGroup
    storage-key="circuito-mir-dashboard"
    unit="rem"
  >
    <UDashboardSidebar
      id="circuito-mir-sidebar"
      v-model:open="sidebarOpen"
      collapsible
      resizable
      :default-size="16.5"
      :min-size="14"
      :max-size="20"
      :collapsed-size="4.5"
      class="border-default bg-mir-sidebar text-white"
      :ui="{
        header: 'border-b border-white/6 px-3',
        body: 'gap-5 px-3 py-4',
        footer: 'border-t border-white/6 px-3 py-3',
        content: 'bg-mir-sidebar text-white'
      }"
    >
      <template #header="{ collapsed }">
        <NuxtLink
          v-if="!collapsed"
          to="/admin/dashboard"
          class="flex min-w-0 items-center gap-3"
          aria-label="Circuito MIR, panel principal"
          @click="closeSidebar"
        >
          <span class="grid size-9 shrink-0 place-items-center rounded-xl bg-linear-to-br from-orange-500 to-orange-400 text-sm font-extrabold text-white shadow-lg shadow-orange-950/25">
            M
          </span>
          <span class="min-w-0">
            <span class="block truncate text-sm font-bold text-white">Circuito MIR</span>
            <span class="block truncate text-[11px] text-slate-400">Incidencias y reclamaciones</span>
          </span>
        </NuxtLink>

        <UDashboardSidebarCollapse
          color="neutral"
          variant="ghost"
          class="text-slate-400 hover:bg-white/8 hover:text-white"
          :class="collapsed ? 'mx-auto' : 'ms-auto'"
        />
      </template>

      <template #default="{ collapsed }">
        <UDashboardSearchButton
          :collapsed="collapsed"
          label="Buscar"
          color="neutral"
          variant="outline"
          class="border-white/10 bg-white/4 text-slate-300 hover:bg-white/8 hover:text-white"
        />

        <div class="space-y-1">
          <p
            v-if="!collapsed"
            class="px-2 pb-1 text-[10px] font-bold tracking-[0.14em] text-slate-500 uppercase"
          >
            General
          </p>
          <UNavigationMenu
            :collapsed="collapsed"
            :items="generalLinks"
            :tooltip="{ delayDuration: 0, content: { side: 'right' } }"
            orientation="vertical"
            color="primary"
            variant="pill"
            :ui="navigationUi"
          />
        </div>

        <div class="space-y-1">
          <p
            v-if="!collapsed"
            class="px-2 pb-1 text-[10px] font-bold tracking-[0.14em] text-slate-500 uppercase"
          >
            PMP
          </p>
          <UNavigationMenu
            :collapsed="collapsed"
            :items="pmpLinks"
            :tooltip="{ delayDuration: 0, content: { side: 'right' } }"
            orientation="vertical"
            color="primary"
            variant="pill"
            :ui="navigationUi"
          />
        </div>

        <div class="space-y-1">
          <p
            v-if="!collapsed"
            class="px-2 pb-1 text-[10px] font-bold tracking-[0.14em] text-slate-500 uppercase"
          >
            MIR
          </p>
          <UNavigationMenu
            :collapsed="collapsed"
            :items="mirLinks"
            :tooltip="{ delayDuration: 0, content: { side: 'right' } }"
            orientation="vertical"
            color="primary"
            variant="pill"
            :ui="navigationUi"
          />
        </div>

        <div class="mt-auto">
          <UTooltip
            text="Manual de usuario MIR"
            :disabled="!collapsed"
          >
            <div
              class="flex items-center gap-3 rounded-xl border border-white/8 bg-white/4 p-2.5 text-slate-300"
              :class="collapsed ? 'justify-center' : ''"
            >
              <UIcon
                name="i-lucide-circle-help"
                class="size-5 shrink-0 text-orange-400"
              />
              <span
                v-if="!collapsed"
                class="min-w-0"
              >
                <span class="block text-xs font-semibold text-white">¿Necesitas ayuda?</span>
                <span class="mt-0.5 block text-[11px] leading-4 text-slate-400">El manual estará disponible próximamente.</span>
              </span>
            </div>
          </UTooltip>
        </div>
      </template>

      <template #footer="{ collapsed }">
        <UTooltip
          text="Usuario MIR"
          :disabled="!collapsed"
        >
          <div
            class="flex min-w-0 items-center gap-3"
            :class="collapsed ? 'justify-center' : ''"
          >
            <UAvatar
              alt="Usuario MIR"
              text="UM"
              size="sm"
              class="shrink-0 bg-orange-500 text-white"
            />
            <span
              v-if="!collapsed"
              class="min-w-0"
            >
              <span class="block truncate text-xs font-semibold text-white">Usuario MIR</span>
              <span class="block truncate text-[11px] text-slate-400">Gestión operativa</span>
            </span>
          </div>
        </UTooltip>
      </template>
    </UDashboardSidebar>

    <UDashboardSearch
      :groups="searchGroups"
      placeholder="Buscar expedientes o secciones..."
      :color-mode="false"
      :fuse="{
        fuseOptions: {
          ignoreDiacritics: true,
          keys: ['label', 'description', 'suffix', 'keywords']
        }
      }"
    />

    <slot />
  </UDashboardGroup>
</template>
