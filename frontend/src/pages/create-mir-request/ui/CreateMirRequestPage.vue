<script setup lang="ts">
import { getLocalTimeZone, today } from "@internationalized/date";
import type { CalendarDate } from "@internationalized/date";
import { crearMir } from "@/entities/mir";
import type { CrearMirInput } from "@/entities/mir";
import { formatDate } from "@/shared/lib";

type ResolutionAnswer = "Sí" | "No";
type Priority = CrearMirInput["prioridad"];

interface MirRequestFormState {
  detectionDate: CalendarDate;
  description: string;
  resolved: ResolutionAnswer;
  priority: Priority;
  attachments: File[];
  company: string;
  contactPerson: string;
  phone: string;
  email: string;
  customerCode: string;
}

const maximumDetectionDate = today(getLocalTimeZone());
const resolutionItems: ResolutionAnswer[] = ["No", "Sí"];
const priorityItems: Array<{ label: string; value: Priority }> = [
  { label: "Baja", value: "baja" },
  { label: "Media", value: "media" },
  { label: "Alta", value: "alta" },
];
const calendarOpen = ref<boolean>(false);
const toast = useToast();

const formState = shallowReactive<MirRequestFormState>({
  detectionDate: maximumDetectionDate,
  description: "",
  resolved: "No",
  priority: "baja",
  attachments: [],
  company: "",
  contactPerson: "",
  phone: "",
  email: "",
  customerCode: "",
});

const submitRequest = async (): Promise<void> => {
  const input: CrearMirInput = {
    descripcion: formState.description.trim(),
    solucionado: formState.resolved === "Sí" ? "si" : "no",
    prioridad: formState.priority,
    nombre_empresa: formState.company.trim(),
    nombre_persona_empresa: formState.contactPerson.trim(),
    telefono_empresa: Number(formState.phone.replace(/\D/g, "")),
    codigo_cliente: formState.customerCode.trim(),
    correo_cliente: formState.email.trim(),
    fecha_deteccion: formState.detectionDate.toString(),
  };

  try {
    await crearMir(input, formState.attachments);
  } catch {
    toast.add({
      title: "No se ha podido crear la MIR",
      description: "Revisa los datos del formulario e inténtalo de nuevo.",
      color: "error",
      icon: "i-lucide-circle-x",
    });
    return;
  }

  toast.add({
    title: "MIR creada",
    description: "La MIR se ha registrado correctamente.",
    color: "success",
    icon: "i-lucide-circle-check",
  });

  await navigateTo("/usuario/dashboard");
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

                <UFormField label="Fecha de detección" name="detectionDate" required>
                  <UPopover v-model:open="calendarOpen">
                    <UButton :label="formatDate(formState.detectionDate.toString())" icon="i-lucide-calendar-days"
                      color="neutral" variant="outline" size="lg" class="w-full justify-start font-normal sm:w-64"
                      aria-label="Seleccionar fecha de detección" />

                    <template #content>
                      <UCalendar v-model="formState.detectionDate" :max-value="maximumDetectionDate" locale="es-ES"
                        class="p-2" @update:model-value="calendarOpen = false" />
                    </template>
                  </UPopover>
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

                <UFormField label="Prioridad" name="priority" required>
                  <USelect v-model="formState.priority" :items="priorityItems" icon="i-lucide-flag"
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
                  <UFormField label="Empresa" name="company" required>
                    <UInput v-model="formState.company" icon="i-lucide-building-2" placeholder="Nombre de la empresa"
                      size="lg" class="w-full" maxlength="160" required />
                  </UFormField>

                  <UFormField label="Persona" name="contactPerson" required>
                    <UInput v-model="formState.contactPerson" icon="i-lucide-contact" placeholder="Persona de contacto"
                      size="lg" class="w-full" maxlength="120" required />
                  </UFormField>

                  <UFormField label="Teléfono" name="phone" required>
                    <UInput v-model="formState.phone" type="tel" icon="i-lucide-phone"
                      placeholder="Teléfono de contacto" size="lg" class="w-full" maxlength="30" required />
                  </UFormField>

                  <UFormField label="Código de cliente" name="customerCode" required>
                    <UInput v-model="formState.customerCode" icon="i-lucide-hash" placeholder="Código de cliente"
                      size="lg" class="w-full" maxlength="50" required />
                  </UFormField>

                  <UFormField label="Correo electrónico" name="email" class="sm:col-span-2" required>
                    <UInput v-model="formState.email" type="email" icon="i-lucide-mail" placeholder="correo@empresa.com"
                      size="lg" class="w-full" maxlength="160" required />
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
