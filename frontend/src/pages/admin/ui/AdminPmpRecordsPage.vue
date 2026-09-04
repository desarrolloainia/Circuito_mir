<script setup lang="ts">
import type { TableColumn, TabsItem } from '@nuxt/ui'
import {
  processedPmpGroups,
  processedPmpRecords,
  unprocessedPmpGroups,
  unprocessedPmpRecords
} from '../model/pmp'
import type { PmpGroup, PmpRecord, PmpView } from '../model/pmp'

type PmpGroupFilter = 'all' | PmpGroup

const props = defineProps<{
  view: PmpView
}>()

const route = useRoute()
const search = ref('')
const selectedGroup = ref<PmpGroupFilter>('all')

const columns: TableColumn<PmpRecord>[] = [
  { accessorKey: 'reference', header: 'Referencia', meta: { class: { th: 'w-[30%] md:w-[20%]', td: 'w-[30%] md:w-[20%]' } } },
  { accessorKey: 'subject', header: 'Asunto y empresa', meta: { class: { th: 'w-[45%] md:w-[35%]', td: 'w-[45%] md:w-[35%]' } } },
  { accessorKey: 'owner', header: 'Responsable', meta: { class: { th: 'hidden w-[17%] md:table-cell', td: 'hidden w-[17%] md:table-cell' } } },
  { accessorKey: 'status', header: 'Estado', meta: { class: { th: 'w-[25%] md:w-[13%]', td: 'w-[25%] md:w-[13%]' } } },
  { accessorKey: 'date', header: 'Actualización', meta: { class: { th: 'hidden w-[15%] md:table-cell', td: 'hidden w-[15%] md:table-cell' } } }
]

const pageConfig = computed(() => props.view === 'unprocessed'
  ? {
      title: 'PMP sin procesar',
      description: 'Propuestas pendientes de revisión y clasificación',
      cardTitle: `${unprocessedPmpRecords.length} PMP pendientes`,
      cardDescription: 'Organizadas por tiempo transcurrido desde su recepción',
      records: unprocessedPmpRecords,
      groups: unprocessedPmpGroups
    }
  : {
      title: 'PMP procesadas',
      description: 'Histórico reciente de propuestas revisadas',
      cardTitle: `${processedPmpRecords.length} PMP procesadas`,
      cardDescription: 'Organizadas por fecha de procesamiento',
      records: processedPmpRecords,
      groups: processedPmpGroups
    })

const tabItems = computed<TabsItem[]>(() => [{
  label: 'Todas',
  value: 'all',
  badge: pageConfig.value.records.length
}, ...pageConfig.value.groups.map(group => ({
  label: group.label,
  value: group.label,
  badge: {
    label: pageConfig.value.records.filter(record => record.group === group.label).length,
    color: group.tone,
    variant: 'subtle' as const
  }
}))])

const filteredRecords = computed(() => {
  const query = search.value.trim().toLocaleLowerCase('es')

  return pageConfig.value.records.filter((record) => {
    if (selectedGroup.value !== 'all' && record.group !== selectedGroup.value) {
      return false
    }

    return !query || [record.reference, record.subject, record.company, record.owner]
      .some(value => value.toLocaleLowerCase('es').includes(query))
  })
})

watch([() => props.view, () => route.query.search], ([, query]) => {
  search.value = typeof query === 'string' ? query : ''
  selectedGroup.value = 'all'
}, { immediate: true })
</script>

<template>
  <UDashboardPanel :id="`admin-pmp-${view}`">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">
              {{ pageConfig.title }}
            </h1><p class="mt-0.5 hidden text-xs text-muted sm:block">
              {{ pageConfig.description }}
            </p>
          </div>
        </template><template #right>
          <UDashboardSearchButton
            label="Buscar"
            color="neutral"
            variant="outline"
            :kbds="[]"
            class="hidden sm:inline-flex"
          />
        </template>
      </UDashboardNavbar>
    </template><template #body>
      <main class="mx-auto w-full max-w-6xl p-4 sm:p-6 lg:p-8">
        <UCard
          class="overflow-hidden shadow-sm"
          :ui="{
            header: 'p-4 sm:px-5',
            body: 'p-0 sm:p-0'
          }"
        >
          <template #header>
            <div class="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
              <div class="min-w-0">
                <h2 class="text-base font-bold text-highlighted">
                  {{ pageConfig.cardTitle }}
                </h2>
                <p class="mt-0.5 text-sm text-muted">
                  {{ pageConfig.cardDescription }}
                </p>
              </div>

              <UInput
                v-model="search"
                type="search"
                icon="i-lucide-search"
                placeholder="Buscar PMP..."
                color="neutral"
                size="lg"
                class="w-full sm:w-72"
              />
            </div>
          </template>

          <div class="overflow-x-auto border-b border-default px-3 py-2.5 sm:px-4">
            <UTabs
              v-model="selectedGroup"
              :items="tabItems"
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
            empty="No se encontraron PMP"
            :ui="{
              root: 'overflow-x-auto md:max-h-[560px] md:overflow-auto',
              base: 'w-full table-fixed md:min-w-[900px]',
              th: 'bg-mir-canvas px-2 py-3 text-xs font-semibold text-muted md:px-5',
              td: 'px-2 py-3.5 text-sm text-default md:px-5'
            }"
          >
            <template #reference-cell="{ row }">
              <span class="block truncate text-sm font-bold text-highlighted">
                {{ row.original.reference }}
              </span>
            </template>

            <template #subject-cell="{ row }">
              <div class="w-full min-w-0">
                <p class="whitespace-normal font-semibold leading-5 text-highlighted">
                  {{ row.original.subject }}
                </p>
                <p class="mt-0.5 truncate text-xs text-muted">
                  {{ row.original.company }}
                </p>
              </div>
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
      </main>
    </template>
  </UDashboardPanel>
</template>
