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
      path: "profile",
      name: "core-profile",
      component: () => import( /* webpackChunkName: "CoreProfile" */ "@/modules/core/pages/profile.vue"),
    },
  ],
};

export default router;