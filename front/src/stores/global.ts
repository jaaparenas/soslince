import { createGlobalState, useStorage } from "@vueuse/core";

export const useGlobalState = createGlobalState(() =>
  useStorage("tires-global", {
    auth: false,
    lang: "en-US"
  })
);

export default useGlobalState;
