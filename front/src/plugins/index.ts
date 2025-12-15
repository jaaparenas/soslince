// Plugins
import { loadFonts } from "./webfontloader";
import vuetify from "./vuetify";
import router from "../router";
import { createPinia } from "pinia";
import Vue3Toasity from "vue3-toastify";
import axios from "axios";
import i18n from './i18n'

import type { App } from "vue";
import useAuth from "@/modules/auth/composables/useAuth";
import useConst from "@/composables/useConst";

const consts = useConst();
axios.defaults.baseURL = consts.baseApi;
axios.interceptors.request.use((config) => {
  const auth = useAuth();
  if (auth.isAuthenticated() && auth.getToken() != "") {
    config.headers["Authorization"] = 'Bearer ' + auth.getToken();
  }
  return config
})
axios.interceptors.response.use((resp) => {
  return resp
})

export function registerPlugins(app: App) {
  loadFonts();
  app
    .use(i18n)
    .use(vuetify)
    .use(router)
    .use(createPinia())
    .use(Vue3Toasity, {
      autoClose: 3000,
    })
}
