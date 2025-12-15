const router = {
  name: "auth",
  component: () => import("@/layouts/auth.vue" ),
  children: [
    {
      path: "",
      name: "auth-login",
      component: () => import( /* webpackChunkName: "AuthLogin" */ "@/modules/auth/pages/login.vue" ),
    },
    {
      path: "recovery",
      name: "auth-recovery",
      component: () => import( /* webpackChunkName: "AuthRecovery" */ "@/modules/auth/pages/recovery.vue" ),
    },
  ],
};

export default router;