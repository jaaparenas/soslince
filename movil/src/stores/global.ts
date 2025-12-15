import { createGlobalState, useStorage } from "@vueuse/core";

export const useGlobalState = createGlobalState(() =>
  useStorage("tires-global", {
    auth: false,
    lang: "en-US",
    hidden: false,
    runningSos: null,
    isAppActive: true,
    latitude: null,
    longitude: null,
    timestamp: null
  })
);

export default useGlobalState;
