const router = {
  name: "",
  component: () => import("@/layouts/default.vue" ),
  children: [
    {
      path: "",
      name: "core-index",
      component: () => import( /* webpackChunkName: "CoreIndex" */ "@/modules/core/pages/index.vue"),
    },
    {
      path: "core/customer",
      name: "core-customer",
      component: () => import( /* webpackChunkName: "CoreCustomer" */ "@/modules/core/pages/customer.vue"),
    },
    {
      path: "core/staff",
      name: "core-staff",
      component: () => import( /* webpackChunkName: "CoreStaff" */ "@/modules/core/pages/staff.vue"),
    },
    {
      path: "core/company",
      name: "core-company",
      component: () => import( /* webpackChunkName: "CoreCompany" */ "@/modules/core/pages/company.vue"),
    }
  ],
};

export default router;