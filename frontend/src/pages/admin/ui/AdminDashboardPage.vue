<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import {
  dashboardActivities,
  dashboardMetrics,
  dashboardPendingAreas,
  dashboardQuickActions
} from '../model/dashboard'
import type { DashboardActivity } from '../model/dashboard'

const activityColumns: TableColumn<DashboardActivity>[] = [
  { accessorKey: 'reference', header: 'Referencia', meta: { class: { th: 'w-[28%] md:w-auto', td: 'w-[28%] md:w-auto' } } },
  { accessorKey: 'type', header: 'Tipo', meta: { class: { th: 'hidden md:table-cell', td: 'hidden md:table-cell' } } },
  { accessorKey: 'subject', header: 'Asunto', meta: { class: { th: 'w-[47%] md:w-auto', td: 'w-[47%] md:w-auto' } } },
  { accessorKey: 'owner', header: 'Responsable', meta: { class: { th: 'hidden md:table-cell', td: 'hidden md:table-cell' } } },
  { accessorKey: 'status', header: 'Estado', meta: { class: { th: 'w-[25%] md:w-auto', td: 'w-[25%] md:w-auto' } } },
  { accessorKey: 'updated', header: 'Actualización', meta: { class: { th: 'hidden md:table-cell', td: 'hidden md:table-cell' } } }
]
</script>

<template>
  <UDashboardPanel id="admin-dashboard">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">
              Panel principal
            </h1><p class="mt-0.5 hidden text-xs text-muted sm:block">
              Seguimiento operativo de mejoras, incidencias y reclamaciones
            </p>
          </div>
        </template><template #right>
          <UDashboardSearchButton
            label="Buscar"
            color="neutral"
            variant="outline"
            :kbds="[]"
            class="hidden sm:inline-flex"
          /><UButton
            icon="i-lucide-plus"
            aria-label="Nueva MIR"
          >
            <span class="hidden sm:inline">Nueva MIR</span>
          </UButton>
        </template>
      </UDashboardNavbar>
    </template><template #body>
      <main class="mx-auto w-full max-w-[1500px] p-4 sm:p-6 lg:p-8">
        <section
          aria-label="Resumen operativo"
          class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"
        >
          <UCard
            v-for="metric in dashboardMetrics"
            :key="metric.label"
            as="article"
            class="shadow-sm"
            :ui="{ body: 'p-5 sm:p-5' }"
          >
            <div class="flex justify-between gap-4">
              <p class="text-xs font-semibold text-muted">
                {{ metric.label }}
              </p><UIcon
                :name="metric.icon"
                class="size-5 text-orange-500"
              />
            </div><p class="mt-3 text-3xl font-extrabold text-highlighted">
              {{ metric.value }}
            </p><p class="mt-1 text-xs text-muted">
              {{ metric.note }}
            </p>
          </UCard>
        </section>

        <section
          class="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1.6fr)_minmax(18rem,.9fr)]"
        >
          <div class="space-y-6">
            <UCard
              title="Acciones rápidas"
              class="shadow-sm"
              :ui="{
                header: 'px-5 pt-5 pb-4',
                body: 'px-5 pb-5'
              }"
            >
              <div class="grid gap-3 sm:grid-cols-3">
                <UButton
                  v-for="action in dashboardQuickActions"
                  :key="action.title"
                  :icon="action.icon"
                  color="neutral"
                  variant="outline"
                  class="h-auto items-start justify-start p-4 text-left"
                >
                  <span>
                    <span
                      class="block text-sm font-bold text-highlighted"
                    >
                      {{ action.title }}
                    </span>

                    <span
                      class="mt-1 block text-xs text-muted"
                    >
                      {{ action.description }}
                    </span>
                  </span>
                </UButton>
              </div>
            </UCard>

            <UCard
              id="actividad-reciente"
              class="scroll-mt-6 overflow-hidden shadow-sm"
              :ui="{
                header: 'p-5',
                body: 'p-0'
              }"
            >
              <template #header>
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <h2 class="font-bold text-highlighted">
                      Actividad reciente
                    </h2>

                    <p class="mt-1 text-xs text-muted">
                      Últimos movimientos del circuito
                    </p>
                  </div>

                  <UButton
                    label="Ver todo"
                    color="neutral"
                    variant="outline"
                    size="sm"
                  />
                </div>
              </template>

              <UTable
                :data="dashboardActivities"
                :columns="activityColumns"
                caption="Actividad reciente del circuito MIR"
                :ui="{
                  root: 'overflow-x-auto',
                  base: 'w-full table-fixed md:min-w-[680px]',
                  th: 'bg-mir-canvas px-2 py-3 text-xs font-semibold text-muted md:px-5',
                  td: 'px-2 py-3.5 text-xs text-default md:px-5'
                }"
              >
                <template #reference-cell="{ row }">
                  <span class="block truncate font-bold">
                    {{ row.original.reference }}
                  </span>
                </template>

                <template #status-cell="{ row }">
                  <UBadge
                    :label="row.original.status"
                    :color="row.original.tone"
                    variant="subtle"
                    size="sm"
                  />
                </template>
              </UTable>
            </UCard>
          </div>

          <UCard
            id="pendientes-area"
            title="Pendientes por área"
            description="Distribución actual"
            class="scroll-mt-6 self-start shadow-sm"
            :ui="{
              header: 'px-5 pt-5 pb-4',
              body: 'px-5 pb-5'
            }"
          >
            <ul class="space-y-5">
              <li
                v-for="item in dashboardPendingAreas"
                :key="item.area"
                class="grid grid-cols-[1fr_auto] items-end gap-4"
              >
                <div>
                  <div class="mb-2 flex items-center justify-between gap-4 text-xs">
                    <span class="font-semibold text-highlighted">
                      {{ item.area }}
                    </span>

                    <span class="text-muted">
                      {{ item.percentage }}%
                    </span>
                  </div>

                  <UProgress
                    :model-value="item.percentage"
                    :max="100"
                    size="sm"
                    :get-value-text="
                      () => `${item.percentage}% de pendientes en ${item.area}`
                    "
                  />
                </div>

                <span class="text-sm font-extrabold text-highlighted">
                  {{ item.count }}
                </span>
              </li>
            </ul>
          </UCard>
        </section>
      </main>
    </template>
  </UDashboardPanel>
</template>
