import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import coreRouter from "../modules/core/router";
import authRouter from "../modules/auth/router";

import useGlobalState from "../stores/global";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    meta: { requiresAuth: false },
    ...coreRouter,
  },
  {
    path: "/auth",
    meta: { requiresAuth: false },
    ...authRouter,
  },
  {
    path: "/:pathMatch(.*)*",
    component: () => import("@/modules/core/pages/error.vue"),
  },
];

const router = createRouter({
  //history: createWebHashHistory(),
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 };
  },
});

router.beforeEach(async (to, from, next) => {
  const globalState = useGlobalState();
  if (to.meta.requiresAuth && !globalState.value.auth) {
    next({ name: "auth-login" });
  } else {
    next();
  }
});

export default router;
