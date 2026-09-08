<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { users } from '../model/users'
import type { User } from '../model/users'

const columns: TableColumn<User>[] = [
  { accessorKey: 'id', header: 'ID' },
  { accessorKey: 'role', header: 'Rol' }
]
</script>

<template>
  <UDashboardPanel id="admin-users">
    <template #header>
      <UDashboardNavbar>
        <template #title>
          <div>
            <h1 class="text-base font-bold text-highlighted">
              Usuarios
            </h1>
            <p class="mt-0.5 hidden text-xs text-muted sm:block">
              Roles disponibles en Circuito MIR
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
            <div>
              <h2 class="text-base font-bold text-highlighted">
                {{ users.length }} usuarios
              </h2>
              <p class="mt-0.5 text-sm text-muted">
                Relación de usuarios y roles asignados
              </p>
            </div>
          </template>

          <UTable
            :data="users"
            :columns="columns"
            caption="Usuarios y roles de Circuito MIR"
            empty="No hay usuarios"
            :ui="{
              root: 'overflow-x-auto',
              base: 'w-full table-fixed',
              th: 'bg-mir-canvas px-3 py-3 text-xs font-semibold text-muted sm:px-5',
              td: 'px-3 py-3.5 text-sm text-default sm:px-5'
            }"
          >
            <template #id-cell="{ row }">
              <span class="font-semibold text-highlighted">
                {{ row.original.id }}
              </span>
            </template>

            <template #role-cell="{ row }">
              <UBadge
                :label="row.original.role"
                color="neutral"
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
