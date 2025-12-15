<template>
  <div>
    <v-btn class="btn-sos" color="red" :disabled="sosActivated" @click="activateSos">
      <template v-if="!sosActivated">
        <v-icon icon="mdi-bell"></v-icon>
      </template>
      <template v-else>
        <span class="counter">{{ counter }}</span>
      </template>
    </v-btn>
    <v-row>
      <v-col cols="9">
        <v-btn class="btn-cancel" :color="sosActivated ? '#20282d' : '#20282d00'" :disabled="!sosActivated" @click="cancelSos" >
          Cancel
        </v-btn>
      </v-col>
      <v-col cols="3">
        <v-btn class="btn-hide" :color="'#20282d'" @click="activateHidden">
          <v-icon icon="mdi-eye-off" ></v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
  import { ref, onBeforeUnmount, onMounted } from 'vue';
  import BackgroundGeolocation from '@transistorsoft/capacitor-background-geolocation';
  import { Preferences } from '@capacitor/preferences';

  import useGlobalState from "@/stores/global";
  import useCore from "@/modules/core/composables/useCore";
  import useUtils from "@/composables/useUtils";
  import useAuth from "@/modules/auth/composables/useAuth";
  import useConst from '@/composables/useConst';

  const sGlobalState = useGlobalState();
  const uCore = useCore();
  const uUtils = useUtils();
  const uAuth = useAuth();
  const uConst = useConst();

  const sosActivated = ref(false);
  const counter = ref(0);
  const uuid = ref('')

  const ctrIntervalCoordinates = ref();
  const ctrIntervalSos = ref();
  const ctrIntervalPosition = ref();

  const enabled = ref(false);

  const initBackgroundGeolocation = async () => {
    BackgroundGeolocation.ready({
      debug: false,
      logLevel: BackgroundGeolocation.LOG_LEVEL_OFF,
      desiredAccuracy: BackgroundGeolocation.DESIRED_ACCURACY_HIGH,
      distanceFilter: 100,
      stopTimeout: 10,
      stopOnTerminate: false,
      startOnBoot: true,
      heartbeatInterval: 15*60,
      preventSuspend: true,
      url: `${uConst.baseApi}/api/1.0/customer/location/`,
      headers: {
        "authorization": `Bearer ${uAuth.getToken()}`
      },
      batchSync: false,
      autoSync: true,
    }).then(state => {
      enabled.value = state.enabled;
      if (!state.enabled) {
        BackgroundGeolocation.start();
      }

      fnGetCurrentPosition();
    });
  };

  BackgroundGeolocation.onHeartbeat((event) => {
    fnGetCurrentPosition();
  });

  onMounted(async () => {
    if (uAuth.isAuthenticated()) {
      initBackgroundGeolocation();
    }
  });

  const fnGetCurrentPosition = async () => {
    BackgroundGeolocation.getCurrentPosition({
      samples: 1,
      persist: true
    }).then((location) => {
      (sGlobalState as any).value.latitude = location.coords.latitude;
      (sGlobalState as any).value.longitude = location.coords.longitude;
      (sGlobalState as any).value.timestamp = location.timestamp;
    });
  }

  onBeforeUnmount(() => {
    clearInterval(ctrIntervalCoordinates.value);
    clearInterval(ctrIntervalPosition.value);
    clearInterval(ctrIntervalSos.value);

    BackgroundGeolocation.stop();
  })

  const activateSos = async () => {
    BackgroundGeolocation.changePace(true);

    sosActivated.value = true;
    counter.value = 10;
    uuid.value = uUtils.createUUID();

    ctrIntervalSos.value = setInterval(() => {
      try {
        let latitude = (sGlobalState as any).value.latitude;
        let longitude = (sGlobalState as any).value.longitude;
        (sGlobalState as any).value.runningSos = {
          key: uuid.value,
          latitude: latitude,
          longitude: longitude
        };
      } catch { }

      if (counter.value > 0) {
        counter.value--;
      } else {
        clearInterval(ctrIntervalSos.value);
        (sGlobalState as any).value.hidden = true;
        sosActivated.value = false;

        BackgroundGeolocation.changePace(false);
        loopSendSos(uuid.value);
      }
    }, 1000);
  }

  const cancelSos = () => {
    BackgroundGeolocation.changePace(false);

    sosActivated.value = false;
    clearInterval(ctrIntervalSos.value);
    (sGlobalState as any).value.runningSos = null;
  }

  const activateHidden = () => {
    (sGlobalState as any).value.hidden = true;
  }

  const loopSendSos = async (key: string = "") => {
    try {
      let latitude = (sGlobalState as any).value.latitude;
      let longitude = (sGlobalState as any).value.longitude;
      if (latitude != 0 && longitude != 0) {
        const resp: any = await uCore.sendSos(key, latitude, longitude);
        console.log("Sent SOS", latitude, longitude, resp.data.mgs)

        if (resp.data.mgs !== key) {
          throw new Error("Error");
        } else {
          (sGlobalState as any).value.runningSos = null;
        }
      }
    } catch {
      setTimeout(() => {
        loopSendSos(key);
      }, 5000);
    }
  }
</script>

<style lang="scss">
  .btn-sos {
    width: 100%;
    height: calc(100vh - 165px) !important;
    margin-bottom: 15px;

    i {
      font-size: 220px;
    }

    .counter {
      font-size: 220px;
    }
  }

  .btn-cancel,
  .btn-hide {
    width: 100%;
    height: 50px !important;
  }
</style>