<script setup lang="ts">
import { getLocalTimeZone, today } from "@internationalized/date";
import type { CalendarDate } from "@internationalized/date";
import { useMirRequests } from "@/entities/mir-request";
import type { CreateMirRequestInput } from "@/entities/mir-request";
import { formatDate } from "@/shared/lib";

type ResolutionAnswer = "Sí" | "No";

interface MirRequestFormState {
  createdBy: string;
  detectionDate: CalendarDate;
  detectedBy: string;
  description: string;
  resolved: ResolutionAnswer;
  attachments: File[];
  company: string;
  contactPerson: string;
  phone: string;
  email: string;
  customerCode: string;
}

const currentUser = "PABLO SANTIAGO/AINIALAN";
const maximumDetectionDate = today(getLocalTimeZone());
const resolutionItems: ResolutionAnswer[] = ["No", "Sí"];
const calendarOpen = ref<boolean>(false);
const toast = useToast();
const { createMirRequest } = useMirRequests();

const formState = shallowReactive<MirRequestFormState>({
  createdBy: currentUser,
  detectionDate: maximumDetectionDate,
  detectedBy: currentUser,
  description: "",
  resolved: "No",
  attachments: [],
  company: "",
  contactPerson: "",
  phone: "",
  email: "",
  customerCode: "",
});

const submitRequest = async (): Promise<void> => {
  const input: CreateMirRequestInput = {
    createdBy: formState.createdBy,
    detectionDate: formState.detectionDate.toString(),
    detectedBy: formState.detectedBy.trim(),
    description: formState.description.trim(),
    resolved: formState.resolved === "Sí",
    company: formState.company.trim(),
    contactPerson: formState.contactPerson.trim(),
    phone: formState.phone.trim(),
    email: formState.email.trim(),
    customerCode: formState.customerCode.trim(),
    attachments: formState.attachments.map((file) => ({
      name: file.name,
      size: file.size,
    })),
  };

  const request = createMirRequest(input);

  toast.add({
    title: "MIR creada",
    description: `${request.reference} se ha registrado correctamente.`,
    color: "success",
    icon: "i-lucide-circle-check",
  });

  await navigateTo(`/usuario/solicitudes/${request.id}`);
};
</script>

<template>
  <UDashboardPanel id="create-mir-request">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">Nueva MIR</h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              Registra los datos de la mejora, incidencia o reclamación
            </p>
          </div>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <main id="contenido-principal" tabindex="-1" class="mx-auto w-full max-w-5xl p-4 sm:p-6">
        <UButton to="/usuario/dashboard" label="Volver a mis solicitudes" icon="i-lucide-arrow-left" color="neutral"
          variant="ghost" class="mb-5" />

        <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_18rem]">
          <UCard class="shadow-sm" :ui="{
            header: 'px-5 pt-5 pb-4 sm:px-6 sm:pt-6 sm:pb-5',
            body: 'px-5 pt-0 pb-5 sm:px-6 sm:pb-6',
          }">
            <template #header>
              <h2 class="text-lg font-bold text-highlighted">Datos M.I.R</h2>
              <p class="mt-1 text-sm leading-6 text-muted">
                Completa los datos de detección y, cuando proceda, los datos del cliente.
              </p>
            </template>

            <UForm :state="formState" class="space-y-7" @submit="submitRequest">
              <fieldset class="space-y-5">
                <legend class="mb-4 text-sm font-bold text-orange-400">Datos de detección</legend>

                <div class="grid gap-5 sm:grid-cols-[minmax(0,1fr)_13rem]">
                  <UFormField label="Usuario" name="createdBy">
                    <UInput v-model="formState.createdBy" icon="i-lucide-user" size="lg" class="w-full" readonly />
                  </UFormField>

                  <UFormField label="Fecha de detección" name="detectionDate" required>
                    <UPopover v-model:open="calendarOpen">
                      <UButton :label="formatDate(formState.detectionDate.toString())" icon="i-lucide-calendar-days"
                        color="neutral" variant="outline" size="lg" class="w-full justify-start font-normal"
                        aria-label="Seleccionar fecha de detección" />

                      <template #content>
                        <UCalendar v-model="formState.detectionDate" :max-value="maximumDetectionDate" locale="es-ES"
                          class="p-2" @update:model-value="calendarOpen = false" />
                      </template>
                    </UPopover>
                  </UFormField>
                </div>

                <UFormField label="Persona que ha detectado la MIR" name="detectedBy" required>
                  <UInput v-model="formState.detectedBy" icon="i-lucide-user-round-search"
                    placeholder="Nombre de la persona" size="lg" class="w-full" maxlength="120" required />
                </UFormField>

                <UFormField label="Descripción" name="description"
                  description="Indica brevemente solo lo que ha sucedido, sin explicar la solución adoptada." required>
                  <UTextarea v-model="formState.description" placeholder="¿Qué ha sucedido?" :rows="6" autoresize
                    class="w-full" minlength="20" maxlength="2000" required />
                </UFormField>

                <UFormField label="¿Está solucionada ya la M.I.R?" name="resolved" required>
                  <USelect v-model="formState.resolved" :items="resolutionItems" icon="i-lucide-circle-check-big"
                    size="lg" class="w-full sm:w-48" required />
                </UFormField>

                <UFormField label="Archivos adjuntos" name="attachments"
                  description="Opcional. Puedes añadir imágenes o documentos PDF.">
                  <UFileUpload v-model="formState.attachments" multiple accept="image/*,application/pdf"
                    label="Arrastra los archivos aquí" description="PNG, JPG o PDF" layout="list" position="inside"
                    class="w-full" :ui="{
                      base: 'min-h-28',
                    }" />
                </UFormField>
              </fieldset>

              <fieldset class="space-y-5 border-t border-default pt-6">
                <legend class="px-2 text-sm font-bold text-orange-400">
                  Datos de empresa y contacto
                </legend>

                <div class="grid gap-5 sm:grid-cols-2">
                  <UFormField label="Empresa" name="company">
                    <UInput v-model="formState.company" icon="i-lucide-building-2" placeholder="Nombre de la empresa"
                      size="lg" class="w-full" maxlength="160" />
                  </UFormField>

                  <UFormField label="Persona" name="contactPerson">
                    <UInput v-model="formState.contactPerson" icon="i-lucide-contact" placeholder="Persona de contacto"
                      size="lg" class="w-full" maxlength="120" />
                  </UFormField>

                  <UFormField label="Teléfono" name="phone">
                    <UInput v-model="formState.phone" type="tel" icon="i-lucide-phone"
                      placeholder="Teléfono de contacto" size="lg" class="w-full" maxlength="30" />
                  </UFormField>

                  <UFormField label="Código de cliente" name="customerCode">
                    <UInput v-model="formState.customerCode" icon="i-lucide-hash" placeholder="Código de cliente"
                      size="lg" class="w-full" maxlength="50" />
                  </UFormField>

                  <UFormField label="Correo electrónico" name="email" class="sm:col-span-2">
                    <UInput v-model="formState.email" type="email" icon="i-lucide-mail" placeholder="correo@empresa.com"
                      size="lg" class="w-full" maxlength="160" />
                  </UFormField>
                </div>
              </fieldset>

              <div class="flex flex-col-reverse gap-3 border-t border-default pt-5 sm:flex-row sm:justify-end">
                <UButton to="/usuario/dashboard" label="Cancelar" color="neutral" variant="outline" size="lg"
                  class="justify-center" />

                <UButton type="submit" label="Crear MIR" icon="i-lucide-send" size="lg" class="justify-center" />
              </div>
            </UForm>
          </UCard>

          <aside aria-labelledby="form-help-title">
            <UCard class="shadow-sm lg:sticky lg:top-6" :ui="{
              body: 'p-5',
            }">
              <span class="grid size-10 place-items-center rounded-xl bg-orange-500/10 text-orange-400">
                <UIcon name="i-lucide-lightbulb" class="size-5" aria-hidden="true" />
              </span>

              <h2 id="form-help-title" class="mt-3 font-bold text-highlighted">
                Cómo describir la MIR
              </h2>

              <p class="mt-3 text-sm leading-6 text-muted">
                Explica únicamente el hecho detectado. La solución aplicada se documentará en la
                fase correspondiente del circuito.
              </p>
            </UCard>
          </aside>
        </div>
      </main>
    </template>
  </UDashboardPanel>
</template>
