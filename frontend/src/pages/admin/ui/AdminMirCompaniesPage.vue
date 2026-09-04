<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { closedMirRecords, mirCompanies, pendingMirRecords } from '../model/mir'
import type { MirRecord } from '../model/mir'

const route = useRoute()
const search = ref<string>('')
const selectedCompany = ref<string>('Todas las empresas')

const columns: TableColumn<MirRecord>[] = [
  { accessorKey: 'company', header: 'Empresa', meta: { class: { th: 'w-[30%] md:w-[20%]', td: 'w-[30%] md:w-[20%]' } } },
  { accessorKey: 'reference', header: 'Nº MIR', meta: { class: { th: 'w-[25%] md:w-[13%]', td: 'w-[25%] md:w-[13%]' } } },
  { accessorKey: 'subject', header: 'Incidencia', meta: { class: { th: 'w-[45%] md:w-[25%]', td: 'w-[45%] md:w-[25%]' } } },
  { accessorKey: 'owner', header: 'Responsable', meta: { class: { th: 'hidden w-[14%] md:table-cell', td: 'hidden w-[14%] md:table-cell' } } },
  { accessorKey: 'priority', header: 'Prioridad', meta: { class: { th: 'hidden w-[10%] md:table-cell', td: 'hidden w-[10%] md:table-cell' } } },
  { accessorKey: 'status', header: 'Estado', meta: { class: { th: 'hidden w-[10%] md:table-cell', td: 'hidden w-[10%] md:table-cell' } } },
  { accessorKey: 'date', header: 'Fecha', meta: { class: { th: 'hidden w-[8%] md:table-cell', td: 'hidden w-[8%] md:table-cell' } } }
]

const companyOptions: string[] = ['Todas las empresas', ...mirCompanies.map(company => company.name)]
const companyRank = new Map<string, number>(mirCompanies.map((company, index) => [company.name, index]))
const records: MirRecord[] = [...pendingMirRecords, ...closedMirRecords]
  .sort((recordA, recordB) => (companyRank.get(recordA.company) ?? 0) - (companyRank.get(recordB.company) ?? 0))

const filteredRecords = computed<MirRecord[]>(() => {
  const query: string = search.value.trim().toLocaleLowerCase('es')

  return records.filter(record => (
    (selectedCompany.value === 'Todas las empresas' || record.company === selectedCompany.value)
    && (!query || [record.company, record.reference, record.subject, record.owner]
      .some(value => value.toLocaleLowerCase('es').includes(query)))
  ))
})

watch(() => route.query.company, (company) => {
  selectedCompany.value = typeof company === 'string' && mirCompanies.some(item => item.name === company)
    ? company
    : 'Todas las empresas'
  search.value = ''
}, { immediate: true })
</script>

<template>
  <UDashboardPanel id="admin-mir-companies">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">
              MIR por empresa
            </h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              Empresas ordenadas por expedientes que requieren atención
            </p>
          </div>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <main class="mx-auto w-full max-w-[1500px] p-4 sm:p-6 lg:p-8">
        <section aria-labelledby="priority-companies">
          <div class="mb-3 flex items-end justify-between gap-4">
            <div>
              <h2
                id="priority-companies"
                class="font-bold text-highlighted"
              >
                Empresas prioritarias
              </h2>
              <p class="mt-0.5 text-xs text-muted">
                Ordenadas por MIR pendientes y prioridad alta
              </p>
            </div>
            <UButton
              v-if="selectedCompany !== 'Todas las empresas'"
              label="Ver todas"
              color="neutral"
              variant="ghost"
              size="sm"
              @click="selectedCompany = 'Todas las empresas'"
            />
          </div>

          <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            <button
              v-for="(company, index) in mirCompanies.slice(0, 4)"
              :key="company.name"
              type="button"
              class="rounded-xl border bg-default p-4 text-left shadow-sm transition-colors hover:border-orange-500/50"
              :class="selectedCompany === company.name ? 'border-orange-500 ring-1 ring-orange-500/30' : 'border-default'"
              @click="selectedCompany = company.name"
            >
              <div class="flex items-start justify-between gap-3">
                <span class="grid size-8 shrink-0 place-items-center rounded-lg bg-orange-500/10 text-xs font-extrabold text-orange-400">
                  {{ index + 1 }}
                </span>
                <UBadge
                  :label="`${company.pending} pendientes`"
                  :color="company.highPriority > 0 ? 'error' : 'warning'"
                  variant="subtle"
                  size="sm"
                />
              </div>
              <p class="mt-4 truncate text-sm font-bold text-highlighted">
                {{ company.name }}
              </p>
              <p class="mt-1 text-xs text-muted">
                {{ company.highPriority }} de prioridad alta · {{ company.closed }} cerradas
              </p>
            </button>
          </div>
        </section>

        <UCard
          class="mt-6 overflow-hidden shadow-sm"
          :ui="{ header: 'p-4 sm:px-5', body: 'p-0 sm:p-0' }"
        >
          <template #header>
            <div class="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
              <div>
                <h2 class="text-base font-bold text-highlighted">
                  Todas las MIR
                </h2>
                <p class="mt-0.5 text-sm text-muted">
                  {{ filteredRecords.length }} expedientes en la selección actual
                </p>
              </div>

              <div class="flex w-full flex-col gap-2 sm:flex-row lg:w-auto">
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
                  :items="companyOptions"
                  icon="i-lucide-building-2"
                  color="neutral"
                  size="lg"
                  class="w-full sm:w-56"
                  aria-label="Filtrar por empresa"
                />
              </div>
            </div>
          </template>

          <UTable
            :data="filteredRecords"
            :columns="columns"
            caption="Expedientes MIR agrupados por empresa"
            sticky="header"
            empty="No se encontraron MIR"
            :ui="{
              root: 'overflow-x-auto md:max-h-[620px] md:overflow-auto',
              base: 'w-full table-fixed md:min-w-[1120px]',
              th: 'bg-mir-canvas px-2 py-3 text-xs font-semibold text-muted md:px-4',
              td: 'px-2 py-3.5 text-sm text-default md:px-4'
            }"
          >
            <template #company-cell="{ row }">
              <span class="block truncate font-bold text-highlighted">
                {{ row.original.company }}
              </span>
            </template>

            <template #reference-cell="{ row }">
              <span class="block truncate font-semibold text-highlighted">
                {{ row.original.reference }}
              </span>
            </template>

            <template #subject-cell="{ row }">
              <div class="min-w-0">
                <p class="whitespace-normal font-semibold leading-5 text-highlighted">
                  {{ row.original.subject }}
                </p>
                <p class="mt-0.5 truncate text-xs text-muted">
                  {{ row.original.department }}
                </p>
              </div>
            </template>

            <template #priority-cell="{ row }">
              <UBadge
                :label="row.original.priority"
                :color="row.original.priorityTone"
                variant="subtle"
                size="sm"
              />
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
