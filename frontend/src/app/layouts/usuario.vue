<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const sidebarOpen = ref<boolean>(false);

const closeSidebar = (): void => {
  sidebarOpen.value = false;
};

const navigationItems = [
  {
    label: "Mis solicitudes",
    icon: "i-lucide-files",
    to: "/usuario/dashboard",
    exact: true,
    onSelect: closeSidebar,
  },
  {
    label: "Nueva MIR",
    icon: "i-lucide-circle-plus",
    to: "/usuario/solicitudes/nueva",
    exact: true,
    onSelect: closeSidebar,
  },
] satisfies NavigationMenuItem[];

const navigationUi = {
  label: "px-2 text-[10px] font-bold tracking-[0.14em] text-slate-500 uppercase",
  link: "text-slate-300 hover:bg-white/6 hover:text-white data-[active]:bg-white/10 data-[active]:text-white",
  linkLeadingIcon: "text-slate-400 group-data-[active]:text-orange-400",
};
</script>

<template>
  <UDashboardGroup storage-key="circuito-mir-user-dashboard" unit="rem">
    <a
      href="#contenido-principal"
      class="fixed top-3 left-3 z-50 -translate-y-20 rounded-lg bg-orange-500 px-4 py-2 font-semibold text-white transition-transform focus:translate-y-0"
    >
      Saltar al contenido principal
    </a>

    <UDashboardSidebar
      id="circuito-mir-user-sidebar"
      v-model:open="sidebarOpen"
      collapsible
      resizable
      :default-size="16.5"
      :min-size="14"
      :max-size="20"
      :collapsed-size="4.5"
      class="border-default bg-mir-sidebar text-white"
      :ui="{
        header: 'border-b border-white/6 px-3',
        body: 'gap-5 px-3 py-4',
        footer: 'border-t border-white/6 px-3 py-3',
        content: 'bg-mir-sidebar text-white',
      }"
    >
      <template #header="{ collapsed }">
        <NuxtLink
          v-if="!collapsed"
          to="/usuario/dashboard"
          class="flex min-w-0 items-center gap-3"
          aria-label="Circuito MIR, mis solicitudes"
          @click="closeSidebar"
        >
          <span
            class="grid size-9 shrink-0 place-items-center rounded-xl bg-linear-to-br from-orange-500 to-orange-400 text-sm font-extrabold text-white shadow-lg shadow-orange-950/25"
          >
            M
          </span>
          <span class="min-w-0">
            <span class="block truncate text-sm font-bold text-white">Circuito MIR</span>
            <span class="block truncate text-[11px] text-slate-400">Portal de solicitudes</span>
          </span>
        </NuxtLink>

        <UDashboardSidebarCollapse
          color="neutral"
          variant="ghost"
          class="text-slate-400 hover:bg-white/8 hover:text-white"
          :class="collapsed ? 'mx-auto' : 'ms-auto'"
        />
      </template>

      <template #default="{ collapsed }">
        <div class="space-y-1">
          <p
            v-if="!collapsed"
            class="px-2 pb-1 text-[10px] font-bold tracking-[0.14em] text-slate-500 uppercase"
          >
            Solicitudes
          </p>
          <UNavigationMenu
            :collapsed="collapsed"
            :items="navigationItems"
            :tooltip="{ delayDuration: 0, content: { side: 'right' } }"
            orientation="vertical"
            color="primary"
            variant="pill"
            :ui="navigationUi"
          />
        </div>

        <div class="mt-auto">
          <UTooltip text="Ayuda sobre solicitudes MIR" :disabled="!collapsed">
            <div
              class="flex items-center gap-3 rounded-xl border border-white/8 bg-white/4 p-2.5 text-slate-300"
              :class="collapsed ? 'justify-center' : ''"
            >
              <UIcon name="i-lucide-circle-help" class="size-5 shrink-0 text-orange-400" />
              <span v-if="!collapsed" class="min-w-0">
                <span class="block text-xs font-semibold text-white">¿Necesitas ayuda?</span>
                <span class="mt-0.5 block text-[11px] leading-4 text-slate-400"
                  >El manual estará disponible próximamente.</span
                >
              </span>
            </div>
          </UTooltip>
        </div>
      </template>

      <template #footer="{ collapsed }">
        <UTooltip text="Usuario MIR" :disabled="!collapsed">
          <div class="flex min-w-0 items-center gap-3" :class="collapsed ? 'justify-center' : ''">
            <UAvatar
              alt="Usuario MIR"
              text="UM"
              size="sm"
              class="shrink-0 bg-orange-500 text-white"
            />
            <span v-if="!collapsed" class="min-w-0">
              <span class="block truncate text-xs font-semibold text-white">Usuario MIR</span>
              <span class="block truncate text-[11px] text-slate-400">Solicitante</span>
            </span>
          </div>
        </UTooltip>
      </template>
    </UDashboardSidebar>

    <slot />
  </UDashboardGroup>
</template>
