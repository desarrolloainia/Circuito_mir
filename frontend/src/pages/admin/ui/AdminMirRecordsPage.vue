<script setup lang="ts">
import type { TableColumn, TabsItem } from '@nuxt/ui'
import { closedMirRecords, pendingMirRecords } from '../model/mir'
import type { MirQueue, MirRecord, MirView } from '../model/mir'

type PendingFilter = 'all' | 'overdue' | MirQueue

const props = defineProps<{
  view: MirView
}>()

const route = useRoute()
const search = ref<string>('')
const selectedFilter = ref<PendingFilter>('all')
const selectedCompany = ref<string>('Todas las empresas')

const columns: TableColumn<MirRecord>[] = [
  { accessorKey: 'reference', header: 'Nº MIR', meta: { class: { th: 'w-[30%] md:w-[12%]', td: 'w-[30%] md:w-[12%]' } } },
  { accessorKey: 'subject', header: 'Incidencia y empresa', meta: { class: { th: 'w-[45%] md:w-[26%]', td: 'w-[45%] md:w-[26%]' } } },
  { accessorKey: 'queue', header: 'Pendiente de', meta: { class: { th: 'hidden w-[12%] md:table-cell', td: 'hidden w-[12%] md:table-cell' } } },
  { accessorKey: 'owner', header: 'Responsable', meta: { class: { th: 'hidden w-[14%] md:table-cell', td: 'hidden w-[14%] md:table-cell' } } },
  { accessorKey: 'executor', header: 'Ejecutor', meta: { class: { th: 'hidden w-[14%] md:table-cell', td: 'hidden w-[14%] md:table-cell' } } },
  { accessorKey: 'priority', header: 'Prioridad', meta: { class: { th: 'w-[25%] md:w-[10%]', td: 'w-[25%] md:w-[10%]' } } },
  { accessorKey: 'date', header: 'Fecha', meta: { class: { th: 'hidden w-[12%] md:table-cell', td: 'hidden w-[12%] md:table-cell' } } }
]

const pageConfig = computed(() => props.view === 'pending'
  ? {
      title: 'MIR pendientes',
      description: 'Incidencias que requieren seguimiento o actuación',
      cardTitle: `${pendingMirRecords.length} MIR pendientes`,
      cardDescription: 'Filtra por el punto del circuito en el que están pendientes',
      records: pendingMirRecords
    }
  : {
      title: 'MIR cerradas',
      description: 'Histórico de incidencias y reclamaciones resueltas',
      cardTitle: `${closedMirRecords.length} MIR cerradas`,
      cardDescription: 'Consulta las resoluciones recientes por empresa o responsable',
      records: closedMirRecords
    })

const companies = computed<string[]>(() => [
  'Todas las empresas',
  ...new Set(pageConfig.value.records.map(record => record.company))
])

const pendingTabs = computed<TabsItem[]>(() => {
  const filters: Array<{ label: string, value: PendingFilter }> = [
    { label: 'Todas', value: 'all' },
    { label: 'Del usuario', value: 'Usuario' },
    { label: 'CAL', value: 'CAL' },
    { label: 'Responsable', value: 'Responsable' },
    { label: 'Ejecutor', value: 'Ejecutor' },
    { label: '+7 días', value: 'overdue' },
    { label: 'CAL C.E.', value: 'CAL C.E.' }
  ]

  return filters.map(filter => ({
    label: filter.label,
    value: filter.value,
    badge: filter.value === 'all'
      ? pendingMirRecords.length
      : pendingMirRecords.filter(record => filter.value === 'overdue'
        ? record.daysOpen > 7
        : record.queue === filter.value).length
  }))
})

const filteredRecords = computed<MirRecord[]>(() => {
  const query: string = search.value.trim().toLocaleLowerCase('es')

  return pageConfig.value.records.filter((record) => {
    if (selectedCompany.value !== 'Todas las empresas' && record.company !== selectedCompany.value) {
      return false
    }

    if (props.view === 'pending' && selectedFilter.value !== 'all') {
      const matchesFilter: boolean = selectedFilter.value === 'overdue'
        ? record.daysOpen > 7
        : record.queue === selectedFilter.value

      if (!matchesFilter) {
        return false
      }
    }

    return !query || [record.reference, record.subject, record.company, record.owner, record.executor, record.department]
      .some(value => value.toLocaleLowerCase('es').includes(query))
  })
})

watch([() => props.view, () => route.query.search], ([, query]) => {
  search.value = typeof query === 'string' ? query : ''
  selectedFilter.value = 'all'
  selectedCompany.value = 'Todas las empresas'
}, { immediate: true })
</script>

<template>
  <UDashboardPanel :id="`admin-mir-${view}`">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">
              {{ pageConfig.title }}
            </h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              {{ pageConfig.description }}
            </p>
          </div>
        </template>
        <template #right>
          <UDashboardSearchButton
            label="Buscar"
            color="neutral"
            variant="outline"
            :kbds="[]"
            class="hidden sm:inline-flex"
          />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <main class="mx-auto w-full max-w-[1500px] p-4 sm:p-6 lg:p-8">
        <UCard
          class="overflow-hidden shadow-sm"
          :ui="{ header: 'p-4 sm:px-5', body: 'p-0 sm:p-0' }"
        >
          <template #header>
            <div class="flex flex-col justify-between gap-4 xl:flex-row xl:items-center">
              <div class="min-w-0">
                <h2 class="text-base font-bold text-highlighted">
                  {{ pageConfig.cardTitle }}
                </h2>
                <p class="mt-0.5 text-sm text-muted">
                  {{ pageConfig.cardDescription }}
                </p>
              </div>

              <div class="flex w-full flex-col gap-2 sm:flex-row xl:w-auto">
                <UInput
                  v-model="search"
                  type="search"
                  icon="i-lucide-search"
                  placeholder="Buscar MIR..."
                  color="neutral"
                  size="lg"
                  class="w-full sm:w-72"
                />
                <USelect
                  v-model="selectedCompany"
                  :items="companies"
                  icon="i-lucide-building-2"
                  color="neutral"
                  size="lg"
                  class="w-full sm:w-56"
                  aria-label="Filtrar por empresa"
                />
              </div>
            </div>
          </template>

          <div
            v-if="view === 'pending'"
            class="overflow-x-auto border-b border-default px-3 py-2.5 sm:px-4"
          >
            <UTabs
              v-model="selectedFilter"
              :items="pendingTabs"
              :content="false"
              color="primary"
              variant="pill"
              size="lg"
              class="min-w-max"
            />
          </div>

          <UTable
            :data="filteredRecords"
            :columns="columns"
            :caption="pageConfig.cardTitle"
            sticky="header"
            empty="No se encontraron MIR"
            :ui="{
              root: 'overflow-x-auto md:max-h-[620px] md:overflow-auto',
              base: 'w-full table-fixed md:min-w-[1120px]',
              th: 'bg-mir-canvas px-2 py-3 text-xs font-semibold text-muted md:px-4',
              td: 'px-2 py-3.5 text-sm text-default md:px-4'
            }"
          >
            <template #reference-cell="{ row }">
              <span class="block truncate font-bold text-highlighted">
                {{ row.original.reference }}
              </span>
            </template>

            <template #subject-cell="{ row }">
              <div class="min-w-0">
                <p class="whitespace-normal font-semibold leading-5 text-highlighted">
                  {{ row.original.subject }}
                </p>
                <p class="mt-0.5 truncate text-xs text-muted">
                  {{ row.original.company }} · {{ row.original.department }}
                </p>
              </div>
            </template>

            <template #queue-cell="{ row }">
              <UBadge
                :label="row.original.queue"
                color="neutral"
                variant="subtle"
                size="sm"
              />
            </template>

            <template #priority-cell="{ row }">
              <UBadge
                :label="row.original.priority"
                :color="row.original.priorityTone"
                variant="subtle"
                size="sm"
              />
            </template>
          </UTable>
        </UCard>
      </main>
    </template>
  </UDashboardPanel>
</template>
