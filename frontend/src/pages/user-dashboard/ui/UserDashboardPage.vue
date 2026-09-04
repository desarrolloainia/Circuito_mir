<script setup lang="ts">
import { useMirRequests } from "@/entities/mir-request";
import { formatDate } from "@/shared/lib";

const { requests } = useMirRequests();
const search = ref<string>("");

const filteredRequests = computed(() => {
  const query: string = search.value.trim().toLocaleLowerCase("es");

  return requests.value.filter(
    (request) =>
      !query ||
      [request.reference, request.description, request.company, request.detectedBy].some((value) =>
        value.toLocaleLowerCase("es").includes(query),
      ),
  );
});
</script>

<template>
  <UDashboardPanel id="user-dashboard">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">Mis solicitudes</h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              Crea solicitudes MIR y consulta su seguimiento
            </p>
          </div>
        </template>
        <template #right>
          <UButton to="/usuario/solicitudes/nueva" icon="i-lucide-plus">
            <span class="hidden sm:inline">Nueva MIR</span>
          </UButton>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <main
        id="contenido-principal"
        tabindex="-1"
        class="mx-auto w-full max-w-6xl p-4 sm:p-6 lg:p-8"
      >
        <section
          class="relative overflow-hidden rounded-2xl border border-orange-400/20 bg-linear-to-br from-orange-500 via-orange-600 to-orange-800 p-6 shadow-xl shadow-orange-950/20 sm:p-8"
        >
          <div class="relative z-10 max-w-2xl">
            <p class="text-xs font-bold tracking-[0.16em] text-orange-100 uppercase">
              Portal de solicitudes MIR
            </p>
            <h2 class="mt-3 text-2xl font-extrabold tracking-tight text-white sm:text-3xl">
              Registra una nueva MIR
            </h2>
            <p class="mt-3 max-w-xl text-sm leading-6 text-orange-50/90 sm:text-base">
              Indica qué ha sucedido, cuándo se detectó y consulta desde aquí cómo avanza tu
              solicitud.
            </p>
            <UButton
              to="/usuario/solicitudes/nueva"
              label="Crear nueva MIR"
              icon="i-lucide-circle-plus"
              color="neutral"
              variant="solid"
              size="lg"
              class="mt-6"
            />
          </div>
          <UIcon
            name="i-lucide-route"
            class="absolute -right-8 -bottom-10 size-48 rotate-[-8deg] text-white/10 sm:right-8 sm:size-56"
            aria-hidden="true"
          />
        </section>

        <section aria-labelledby="requests-heading" class="mt-6">
          <UCard
            class="overflow-hidden shadow-sm"
            :ui="{ header: 'p-4 sm:p-5', body: 'p-0 sm:p-0' }"
          >
            <template #header>
              <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                <div>
                  <h2 id="requests-heading" class="font-bold text-highlighted">
                    Solicitudes recientes
                  </h2>
                  <p class="mt-1 text-sm text-muted">
                    {{ requests.length }} solicitudes registradas
                  </p>
                </div>
                <UInput
                  v-model="search"
                  type="search"
                  icon="i-lucide-search"
                  placeholder="Buscar solicitud..."
                  color="neutral"
                  size="lg"
                  class="w-full sm:w-72"
                  aria-label="Buscar por referencia, descripción, empresa o persona"
                />
              </div>
            </template>

            <ul v-if="filteredRequests.length" class="divide-y divide-default">
              <li v-for="request in filteredRequests" :key="request.id">
                <article
                  class="grid gap-4 p-4 sm:grid-cols-[auto_minmax(0,1fr)_auto] sm:items-center sm:px-5"
                >
                  <span
                    class="grid size-10 place-items-center rounded-xl bg-orange-500/10 text-orange-400"
                  >
                    <UIcon name="i-lucide-file-warning" class="size-5" aria-hidden="true" />
                  </span>

                  <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-2">
                      <span class="text-xs font-bold text-orange-400">{{ request.reference }}</span>
                      <UBadge :label="request.status" color="success" variant="subtle" size="sm" />
                    </div>
                    <h3 class="mt-1 truncate text-sm font-bold text-highlighted sm:text-base">
                      {{ request.description }}
                    </h3>
                    <p class="mt-1 text-xs text-muted">
                      Detectada el {{ formatDate(request.detectionDate) }} ·
                      {{ request.company || request.detectedBy }}
                    </p>
                  </div>

                  <UButton
                    :to="`/usuario/solicitudes/${request.id}`"
                    label="Ver seguimiento"
                    trailing-icon="i-lucide-arrow-right"
                    color="neutral"
                    variant="outline"
                    class="w-full justify-center sm:w-auto"
                  />
                </article>
              </li>
            </ul>

            <div v-else class="grid place-items-center px-6 py-14 text-center">
              <span
                class="grid size-12 place-items-center rounded-2xl bg-orange-500/10 text-orange-400"
              >
                <UIcon name="i-lucide-search-x" class="size-6" aria-hidden="true" />
              </span>
              <h3 class="mt-4 font-bold text-highlighted">No encontramos solicitudes</h3>
              <p class="mt-1 text-sm text-muted">
                Prueba con otra referencia, descripción, empresa o persona.
              </p>
            </div>
          </UCard>
        </section>
      </main>
    </template>
  </UDashboardPanel>
</template>
