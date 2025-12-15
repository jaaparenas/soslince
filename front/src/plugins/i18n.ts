import { createI18n } from 'vue-i18n'

import enUS from "@/locales/en-US.json";
import esCO from "@/locales/es-CO.json";
type MessageSchema = typeof enUS;
const i18n = createI18n<[MessageSchema], "en-US" | "es-CO">({
  legacy: false,
  locale: "es-CO",
  messages: {
    "en-US": enUS,
    "es-CO": esCO
  },
});

export default i18n