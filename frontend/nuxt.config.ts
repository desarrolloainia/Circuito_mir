// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@nuxt/ui"],

  devtools: {
    enabled: true,
  },

  css: ["~/app/styles/main.css"],

  dir: {
    pages: "app/routes",
    layouts: "app/layouts",
  },

  srcDir: "src",

  routeRules: {
    "/usuario": { redirect: "/usuario/dashboard" },
    "/usuario/dashboard": { prerender: true },
    "/admin/dashboard": { prerender: true },
    "/admin/mir/pendientes": { prerender: true },
    "/admin/mir/cerradas": { prerender: true },
    "/admin/mir/documentos": { prerender: true },
    "/admin/mir/empresas": { prerender: true },
    "/admin/pmp/sin-procesar": { prerender: true },
    "/admin/pmp/procesadas": { prerender: true },
  },

  compatibilityDate: "2026-06-30",
});
