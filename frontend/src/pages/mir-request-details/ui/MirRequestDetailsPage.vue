<script setup lang="ts">
import type { TimelineItem } from "@nuxt/ui";
import { useMirRequests } from "@/entities/mir-request";
import { formatDate, formatDateTime } from "@/shared/lib";

const route = useRoute();
const { getMirRequestById } = useMirRequests();

const requestId = computed<string>(() => String(route.params.id ?? ""));
const request = computed(() => getMirRequestById(requestId.value));

const timelineItems = computed<TimelineItem[]>(() =>
  request.value
    ? [
        {
          value: 1,
          date: formatDateTime(request.value.createdAt),
          title: "Solicitud creada",
          description:
            "Tu solicitud se ha registrado correctamente y está disponible para su revisión.",
          icon: "i-lucide-circle-check",
        },
      ]
    : [],
);

const fileSizeFormatter = new Intl.NumberFormat("es-ES", {
  maximumFractionDigits: 1,
});

const formatFileSize = (size: number): string =>
  `${fileSizeFormatter.format(size / 1024 / 1024)} MB`;
</script>

<template>
  <UDashboardPanel id="mir-request-details">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">Seguimiento de solicitud</h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              Consulta los movimientos de tu solicitud MIR
            </p>
          </div>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <main
        id="contenido-principal"
        tabindex="-1"
        class="mx-auto w-full max-w-6xl p-4 sm:p-6 lg:p-8"
      >
        <UButton
          to="/usuario/dashboard"
          label="Volver a mis solicitudes"
          icon="i-lucide-arrow-left"
          color="neutral"
          variant="ghost"
          class="mb-4"
        />

        <template v-if="request">
          <section class="rounded-2xl border border-default bg-default p-5 shadow-sm sm:p-6">
            <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
              <div class="min-w-0">
                <div class="flex flex-wrap items-center gap-2">
                  <span class="text-sm font-extrabold text-orange-400">{{
                    request.reference
                  }}</span>
                  <UBadge :label="request.status" color="success" variant="subtle" />
                </div>
                <h2 class="mt-3 text-xl font-extrabold text-highlighted sm:text-2xl">
                  MIR detectada el {{ formatDate(request.detectionDate) }}
                </h2>
                <p class="mt-2 text-sm text-muted">
                  Registrada por {{ request.createdBy }} · {{ formatDateTime(request.createdAt) }}
                </p>
              </div>
              <span
                class="grid size-12 shrink-0 place-items-center rounded-2xl bg-orange-500/10 text-orange-400"
              >
                <UIcon name="i-lucide-file-check-2" class="size-6" aria-hidden="true" />
              </span>
            </div>
          </section>

          <div class="mt-6 grid gap-6 lg:grid-cols-[minmax(0,1.4fr)_minmax(18rem,.8fr)]">
            <UCard
              class="shadow-sm"
              :ui="{
                header: 'px-5 pt-5 pb-4 sm:px-6 sm:pt-6 sm:pb-5',
                body: 'px-5 pb-5 pt-0 sm:px-6 sm:pb-6',
              }"
            >
              <template #header>
                <h2 class="font-bold text-highlighted">Seguimiento</h2>
                <p class="mt-1 text-sm text-muted">Historial cronológico de la solicitud</p>
              </template>

              <UTimeline :items="timelineItems" :default-value="1" color="primary" size="lg" />
            </UCard>

            <div class="space-y-6">
              <UCard
                class="shadow-sm"
                :ui="{
                  header: 'px-5 pt-5 pb-4',
                  body: 'px-5 pb-5 pt-0',
                }"
              >
                <template #header>
                  <h2 class="font-bold text-highlighted">Detalles</h2>
                </template>
                <dl class="space-y-4 text-sm">
                  <div>
                    <dt class="text-xs font-semibold text-muted">Persona que detectó la MIR</dt>
                    <dd class="mt-1 font-semibold text-highlighted">
                      {{ request.detectedBy }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs font-semibold text-muted">¿Estaba solucionada?</dt>
                    <dd class="mt-1 font-semibold text-highlighted">
                      {{ request.resolved ? "Sí" : "No" }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs font-semibold text-muted">Descripción</dt>
                    <dd class="mt-1 whitespace-pre-line leading-6 text-default">
                      {{ request.description }}
                    </dd>
                  </div>
                </dl>
              </UCard>

              <UCard
                class="shadow-sm"
                :ui="{
                  header: 'px-5 pt-5 pb-4',
                  body: 'px-5 pb-5 pt-0',
                }"
              >
                <template #header>
                  <h2 class="font-bold text-highlighted">Empresa y contacto</h2>
                </template>
                <dl class="grid gap-4 text-sm sm:grid-cols-2 lg:grid-cols-1">
                  <div>
                    <dt class="text-xs font-semibold text-muted">Empresa</dt>
                    <dd class="mt-1 text-default">
                      {{ request.company || "No indicada" }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs font-semibold text-muted">Persona</dt>
                    <dd class="mt-1 text-default">
                      {{ request.contactPerson || "No indicada" }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs font-semibold text-muted">Teléfono</dt>
                    <dd class="mt-1 text-default">
                      {{ request.phone || "No indicado" }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs font-semibold text-muted">Correo electrónico</dt>
                    <dd class="mt-1 break-all text-default">
                      {{ request.email || "No indicado" }}
                    </dd>
                  </div>
                  <div>
                    <dt class="text-xs font-semibold text-muted">Código de cliente</dt>
                    <dd class="mt-1 text-default">
                      {{ request.customerCode || "No indicado" }}
                    </dd>
                  </div>
                </dl>
              </UCard>

              <UCard
                class="shadow-sm"
                :ui="{
                  header: 'px-5 pt-5 pb-4',
                  body: 'px-5 pb-5 pt-0',
                }"
              >
                <template #header>
                  <h2 class="font-bold text-highlighted">Adjuntos</h2>
                </template>
                <ul v-if="request.attachments.length" class="space-y-2">
                  <li
                    v-for="attachment in request.attachments"
                    :key="attachment.name"
                    class="flex min-w-0 items-center gap-3 rounded-xl border border-default p-3"
                  >
                    <UIcon
                      name="i-lucide-paperclip"
                      class="size-4 shrink-0 text-orange-400"
                      aria-hidden="true"
                    />
                    <span class="min-w-0">
                      <span class="block truncate text-sm font-semibold text-highlighted">{{
                        attachment.name
                      }}</span>
                      <span class="block text-xs text-muted">{{
                        formatFileSize(attachment.size)
                      }}</span>
                    </span>
                  </li>
                </ul>
                <p v-else class="text-sm text-muted">No se añadieron archivos a esta solicitud.</p>
              </UCard>
            </div>
          </div>
        </template>

        <UAlert
          v-else
          title="Solicitud no encontrada"
          description="La solicitud no existe o no pertenece a tu usuario."
          icon="i-lucide-file-question"
          color="warning"
          variant="subtle"
        />
      </main>
    </template>
  </UDashboardPanel>
</template>
