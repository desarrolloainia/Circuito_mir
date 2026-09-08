<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { obtenerDocumentos } from '@/entities/archivos'
import type { DocumentoDTO } from '@/entities/archivos'

const route = useRoute()
const search = ref<string>('')
const selectedType = ref<string>('Todos los tipos')

const { data: documentos } = await useAsyncData('archivos', () => obtenerDocumentos(), { default: () => [] })

const columns: TableColumn<DocumentoDTO>[] = [
  { accessorKey: 'nombre', header: 'Documento' },
  { accessorKey: 'tipo', header: 'Tipo' },
  { accessorKey: 'creado_en', header: 'Fecha de subida' }
]

const documentTypes: string[] = ['Todos los tipos', ...new Set(documentos.value.map(document => document.tipo))]

const filteredDocuments = computed<DocumentoDTO[]>(() => {
  const query: string = search.value.trim().toLocaleLowerCase('es')

  return documentos.value.filter(document => (
    (selectedType.value === 'Todos los tipos' || document.tipo === selectedType.value)
    && (!query || document.nombre.toLocaleLowerCase('es').includes(query))
  ))
})

watch(() => route.query.search, (query) => {
  search.value = typeof query === 'string' ? query : ''
  selectedType.value = 'Todos los tipos'
}, { immediate: true })
</script>

<template>
  <UDashboardPanel id="admin-mir-documents">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">
              Todos los documentos
            </h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              Documentación adjunta a los expedientes MIR
            </p>
          </div>
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
              <div>
                <h2 class="text-base font-bold text-highlighted">
                  {{ documentos.length }} documentos
                </h2>
                <p class="mt-0.5 text-sm text-muted">
                  Localiza archivos por nombre
                </p>
              </div>

              <div class="flex w-full flex-col gap-2 xl:w-auto xl:flex-row">
                <UInput
                  v-model="search"
                  type="search"
                  icon="i-lucide-search"
                  placeholder="Buscar documento..."
                  color="neutral"
                  size="lg"
                  class="w-full xl:w-72"
                />
                <USelect
                  v-model="selectedType"
                  :items="documentTypes"
                  icon="i-lucide-file-type-2"
                  color="neutral"
                  size="lg"
                  class="w-full xl:w-44"
                  aria-label="Filtrar por tipo"
                />
              </div>
            </div>
          </template>

          <UTable
            :data="filteredDocuments"
            :columns="columns"
            caption="Documentación de expedientes MIR"
            sticky="header"
            empty="No se encontraron documentos"
            :ui="{
              root: 'overflow-x-auto md:max-h-[620px] md:overflow-auto',
              base: 'w-full table-fixed md:min-w-[1050px]',
              th: 'bg-mir-canvas px-2 py-3 text-xs font-semibold text-muted md:px-5',
              td: 'px-2 py-3.5 text-sm text-default md:px-5'
            }"
          >
            <template #nombre-cell="{ row }">
              <div class="flex min-w-0 items-center gap-3">
                <span class="grid size-8 shrink-0 place-items-center rounded-lg bg-orange-500/10 text-orange-400">
                  <UIcon
                    name="i-lucide-file-text"
                    class="size-4"
                  />
                </span>
                <span class="min-w-0 truncate font-semibold text-highlighted">
                  {{ row.original.nombre }}
                </span>
              </div>
            </template>

            <template #tipo-cell="{ row }">
              <UBadge
                :label="row.original.tipo"
                color="neutral"
                variant="subtle"
                size="sm"
              />
            </template>

            <template #creado-en-cell="{ row }">
              {{ row.original.creado_en.slice(0, 10) }}
            </template>
          </UTable>
        </UCard>
      </main>
    </template>
  </UDashboardPanel>
</template>
