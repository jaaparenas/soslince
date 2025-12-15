<template>
  <h1 class="text-center text-uppercase">{{ $t('modules.core.active_sos_alert') }}</h1>
  <div class="d-flex flex-wrap justify-content-between text-center">
    <v-card class="ma-2" width="350px" v-for="item in listPending" :key="item.id">
      <customer-card :item="item" />
      <div class="pa-3">
        <v-btn color="red" block @click="clickView(item)">
          <v-icon icon="mdi-map-marker"></v-icon>
          {{ $t('commons.common.details') }}
        </v-btn>
      </div>
    </v-card>
  </div>
  <exp-modal-form
    :title="$t('commons.common.details')"
    :width="1200"
    v-model="viewLocation"
    :btn-save-text="'commons.common.attended_successfully'"
    :btn-cancel-text="'commons.common.close'"
    @fn-save="closeAlert"
  >
    <v-row>
      <v-col cols="4">
        <v-card class="" width="100%">
          <customer-card :item="selectedItem" />
        </v-card>
        <div>
          <h2>{{ $t('commons.common.details') }}</h2>
          <span v-html="selectedItem.customer.details"></span>
        </div>
      </v-col>
      <v-col>
        <div class="mapContainer" v-if="viewLocation">
          <l-map ref="map" :zoom="zoom" :center="center" :useGlobalLeaflet="false">
            <l-tile-layer :url="getWsUrl()" layer-type="base" name="OpenStreetMap"></l-tile-layer>
            <l-feature-group ref="fg">
              <l-marker :lat-lng="objLocation" />
            </l-feature-group>
          </l-map>
        </div>
      </v-col>
    </v-row>
  </exp-modal-form>
  <exp-modal-form
    :title="$t('commons.common.alert')"
    :width="600"
    v-model="alarmModal"
    :btn-save="false"
    btn-cancel-text="commons.common.close"
    style="background-color:rgba(255,0,0,0.8)"
  >
    <div class="text-center">
      <v-icon size="400" color="red">mdi-bell-ring-outline</v-icon>
    </div>
    <audio ref="audioAlert" src="https://sos.lincesr.com/assets/alarm.mp3" loop></audio>
  </exp-modal-form>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import useAuth from "@/modules/auth/composables/useAuth";
import useGlobalState from "@/stores/global";

import 'leaflet/dist/leaflet.css'
import { LMap, LTileLayer, LMarker, LPolygon, LTooltip, LFeatureGroup } from '@vue-leaflet/vue-leaflet'

import { useLoading } from "vue-loading-overlay";
import CustomerCard from "../components/customer_card.vue";
import expModalForm from "@/components/expModalForm";
import useCustomer from "@/modules/core/composables/useCustomer";

const uCustomer = useCustomer();
const uLoading = useLoading();
const uAuth = useAuth();
const sGlobalState = useGlobalState();

const numPending = ref();
const listPending = ref();
const audioAlert = ref();
const ctrIntervalSos = ref();
const selectedItem = ref();
const viewLocation = ref(false);
const objLocation = ref([]);
const zoom = ref(15);
const center = ref([19.3906594,-99.3084211]);
const map = ref<typeof LMap>();
const fg = ref<typeof LFeatureGroup | null>(null);

const alarmModal = ref(false);

onMounted(async () => {
  if (uAuth.isAuthenticated() && sGlobalState.value.auth) {
    let loader = uLoading.show({});
    listPending.value = await uCustomer.getPendingSos();
    numPending.value = listPending.value.length;
    loader.hide();

    ctrIntervalSos.value = setInterval(async () => {
      try {
        listPending.value = await uCustomer.getPendingSos();
        numPending.value = listPending.value.length;
      } catch { }
    }, 1000 * 60 * 0.1);
  }
});

onBeforeUnmount(() => {
  clearInterval(ctrIntervalSos.value);
})

const getWsUrl = (): string => {
  return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
}

const clickView = (item: any) => {
  selectedItem.value = item;
  objLocation.value = [item.latitude, item.longitude];
  center.value = objLocation.value;
  viewLocation.value = true;
};

const closeAlert = async () => {
  let loader = uLoading.show({});
  viewLocation.value = false;

  await uCustomer.getCloseSos({
    user: selectedItem.value.customer.user.id,
    customer: selectedItem.value.customer.id,
    id: selectedItem.value.id,
    key: selectedItem.value.key
  });
  listPending.value = await uCustomer.getPendingSos();
  numPending.value = listPending.value.length;
  loader.hide();
};

const triggerAlert = () => {
  alarmModal.value = true;
  setTimeout(() => {
    audioAlert.value.play();
  }, 500);
}

watch(numPending, (newValue, oldValue) => {
  if (newValue == undefined || newValue == null || newValue == 0)
    return;

  if (newValue > oldValue) {
    triggerAlert();
  }
})
</script>

<style scoped>
  .mapContainer {
    width: 100%;
    height: 600px;
  }

  .leaflet-div-icon {
    background: steelblue;
    color: rgba(255, 255, 255, 0.5);
    border-radius: 80%;
    font-weight: bold;
    font-size: large;
    text-align: center;
    line-height: 21px;
  }
</style>