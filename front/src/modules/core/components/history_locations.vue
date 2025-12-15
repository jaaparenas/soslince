<template>
  <v-row>
    <v-col cols="3">
      <v-row dense>
        <v-col cols="10">
          <v-date-input
            :label="$t('commons.common.date_filter')"
            variant="outlined"
            multiple="range"
            v-model="range"
            prepend-icon=""
            density="compact"
            :hide-details="true"
          ></v-date-input>
        </v-col>
        <v-col cols="2">
          <v-btn block color="green" @click="clickExport()">
            <v-icon>mdi-file-excel</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-table height="600px" fixed-header style="min-height: 600px;">
        <thead>
          <tr>
            <th class="text-left">{{ $t('commons.common.date_time') }}</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in listLocations?.results" :key="item.id">
            <td>{{ uCustomer.adjustDate(item.timestamp) }}</td>
            <td><v-btn size="small" color="primary" icon="mdi-map-marker" @click="clickView(item)"></v-btn></td>
          </tr>
        </tbody>
      </v-table>
      <v-pagination
        :length="numPages"
        size="30"
        v-model="page"
      ></v-pagination>
    </v-col>
    <v-col cols="9">
      <div class="mapContainer">
        <l-map ref="map" :zoom="zoom" :center="center" :useGlobalLeaflet="false">
          <l-tile-layer :url="getWsUrl()" layer-type="base" name="OpenStreetMap"></l-tile-layer>
          <l-feature-group ref="fg">
            <l-marker v-if="viewLocation" :lat-lng="objLocation" />
          </l-feature-group>
        </l-map>
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { ref, watch, computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";

import { VDateInput } from 'vuetify/labs/VDateInput'
import 'leaflet/dist/leaflet.css'
import { LMap, LTileLayer, LMarker, LPolygon, LTooltip, LFeatureGroup } from '@vue-leaflet/vue-leaflet'

import useCustomer from "@/modules/core/composables/useCustomer";

const { t } = useI18n();
const uCustomer = useCustomer();

const listLocations = ref();
const range = ref();
const page = ref(1);
const numPages = ref(0);

const viewLocation = ref(false);
const objLocation = ref([]);
const zoom = ref(15)
const center = ref([19.3906594,-99.3084211])
const map = ref<typeof LMap>()
const fg = ref<typeof LFeatureGroup | null>(null)

const props = defineProps({
  userId: {
    type: Number,
    default: null,
  },
});

onMounted(async () => {
  loadData();
});

const rangeFixed = computed(() => {
  if (range.value && range.value?.length > 0) {
    return [
      range.value[0].toISOString(),
      range.value[range.value.length - 1].toISOString()
    ];
  }
  return []
});

const loadData = async () => {
  listLocations.value = await uCustomer.getListLocation(props.userId, page.value, (rangeFixed as any).value);
  numPages.value = Math.ceil(listLocations.value.count / 10);
};

const getWsUrl = (): string => {
  return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
};

const clickView = (item: any) => {
  objLocation.value = [item.latitude, item.longitude];
  center.value = objLocation.value;
  viewLocation.value = true;
};

const clickExport = async () => {
  uCustomer.getExport('location', props.userId, (rangeFixed as any).value);
}

watch(page, async (newValue, oldValue) => {
  if (newValue == oldValue)
    return;

  loadData();
});

watch(range, async (newValue, oldValue) => {
  if (newValue == oldValue)
    return;

  loadData();
});
</script>


<style scoped>
  .mapContainer {
    width: 100%;
    height: 680px;
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