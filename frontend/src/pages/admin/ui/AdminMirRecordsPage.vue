<script setup lang="ts">
import type { TableColumn } from "@nuxt/ui";
import { listarMir } from "@/entities/mir";
import type { MirDTO } from "@/entities/mir";
import type { MirView } from "../model/mir";

const props = defineProps<{
  view: MirView;
}>();

const route = useRoute();
const search = ref<string>("");
const selectedCompany = ref<string>("Todas las empresas");

const { data: mir } = await useAsyncData("mir", () => listarMir(), { default: () => [] });

const columns: TableColumn<MirDTO>[] = [
  {
    accessorKey: "id",
    header: "Nº MIR",
    meta: { class: { th: "w-[30%] md:w-[22%]", td: "w-[30%] md:w-[22%]" } },
  },
  {
    accessorKey: "descripcion",
    header: "Incidencia y empresa",
    meta: { class: { th: "w-[45%] md:w-[48%]", td: "w-[45%] md:w-[48%]" } },
  },
  {
    accessorKey: "solucionado",
    header: "Estado",
    meta: { class: { th: "w-[25%] md:w-[12%]", td: "w-[25%] md:w-[12%]" } },
  },
  {
    accessorKey: "prioridad",
    header: "Prioridad",
    meta: { class: { th: "hidden w-[12%] md:table-cell", td: "hidden w-[12%] md:table-cell" } },
  },
  {
    accessorKey: "fecha_deteccion",
    header: "Fecha",
    meta: { class: { th: "hidden w-[12%] md:table-cell", td: "hidden w-[12%] md:table-cell" } },
  },
];

const records = computed<MirDTO[]>(() =>
  mir.value.filter((record) => record.solucionado === (props.view === "closed" ? "si" : "no")),
);

const pageConfig = computed(() =>
  props.view === "pending"
    ? {
        title: "MIR pendientes",
        description: "Incidencias que requieren seguimiento o actuación",
        cardTitle: `${records.value.length} MIR pendientes`,
        cardDescription: "Consulta las incidencias pendientes",
      }
    : {
        title: "MIR cerradas",
        description: "Histórico de incidencias y reclamaciones resueltas",
        cardTitle: `${records.value.length} MIR cerradas`,
        cardDescription: "Consulta las incidencias resueltas",
      },
);

const companies = computed<string[]>(() => [
  "Todas las empresas",
  ...new Set(records.value.map((record) => record.nombre_empresa)),
]);

const filteredRecords = computed<MirDTO[]>(() => {
  const query: string = search.value.trim().toLocaleLowerCase("es");

  return records.value.filter((record) => {
    if (
      selectedCompany.value !== "Todas las empresas" &&
      record.nombre_empresa !== selectedCompany.value
    ) {
      return false;
    }

    return (
      !query ||
      [
        record.id,
        record.descripcion,
        record.nombre_empresa,
        record.nombre_persona_empresa,
        record.codigo_cliente,
        record.correo_cliente,
      ].some((value) => value.toLocaleLowerCase("es").includes(query))
    );
  });
});

watch(
  [() => props.view, () => route.query.search],
  ([, query]) => {
    search.value = typeof query === "string" ? query : "";
    selectedCompany.value = "Todas las empresas";
  },
  { immediate: true },
);
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
              td: 'px-2 py-3.5 text-sm text-default md:px-4',
            }"
          >
            <template #id-cell="{ row }">
              <span class="block truncate font-bold text-highlighted">
                {{ row.original.id }}
              </span>
            </template>

            <template #descripcion-cell="{ row }">
              <div class="min-w-0">
                <p class="whitespace-normal font-semibold leading-5 text-highlighted">
                  {{ row.original.descripcion }}
                </p>
                <p class="mt-0.5 truncate text-xs text-muted">
                  {{ row.original.nombre_empresa }} · {{ row.original.nombre_persona_empresa }}
                </p>
              </div>
            </template>

            <template #solucionado-cell="{ row }">
              <UBadge
                :label="row.original.solucionado === 'si' ? 'Cerrada' : 'Pendiente'"
                :color="row.original.solucionado === 'si' ? 'success' : 'warning'"
                variant="subtle"
                size="sm"
              />
            </template>

            <template #prioridad-cell="{ row }">
              <UBadge
                :label="row.original.prioridad"
                :color="row.original.prioridad === 'alta' ? 'error' : row.original.prioridad === 'media' ? 'warning' : 'neutral'"
                variant="subtle"
                size="sm"
                class="capitalize"
              />
            </template>
          </UTable>
        </UCard>
      </main>
    </template>
  </UDashboardPanel>
</template>
