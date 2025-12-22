<template>
  <div>
    <exp-page-header :title="'commons.common.locations'"> </exp-page-header>
    <v-card class="mb-4">
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedCompanies"
              :items="companies"
              item-title="name"
              item-value="id"
              :label="$t('commons.common.company')"
              multiple
              clearable
              hide-details
              density="compact"
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-date-input
              :label="$t('commons.common.date_filter')"
              variant="outlined"
              multiple="range"
              v-model="dateRange"
              prepend-icon=""
              density="compact"
              :hide-details="true"
              :max="new Date().toISOString().split('T')[0]"
              clearable
            ></v-date-input>
          </v-col>
          <v-col cols="12" md="1">
             <v-text-field
                v-model="ageMin"
                :label="$t('commons.common.age_min')"
                type="number"
                density="compact"
             ></v-text-field>
          </v-col>
          <v-col cols="12" md="1">
            <v-text-field
                v-model="ageMax"
                :label="$t('commons.common.age_max')"
                type="number"
                density="compact"
                :rules="[ageMaxRule]"
             ></v-text-field>
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="selectedGenders"
              :items="genders"
              item-title="label"
              item-value="id"
              :label="$t('commons.common.gender')"
              multiple
              clearable
              hide-details
              density="compact"
            ></v-select>
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="selectedBloodTypes"
              :items="bloodTypes"
              item-title="label"
              item-value="id"
              :label="$t('commons.common.blood_type')"
              multiple
              clearable
              hide-details
              density="compact"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <div class="mapContainer">
      <l-map ref="map" :zoom="zoom" :center="center" :useGlobalLeaflet="true">
        <l-tile-layer
          :url="getWsUrl()"
          layer-type="base"
          name="OpenStreetMap"
        />
        <l-marker-cluster-group>
                    <l-marker
                      v-for="(location, index) in validLocations"
                      :key="index"
                      :lat-lng="[parseFloat(location.latitude), parseFloat(location.longitude)]"
                      @click="showHistory(location)"
                      :icon="getCustomMarkerIcon(location.timestamp)"
                    >
                       <l-tooltip :content="`${location.customer?.first_name ?? ''} ${location.customer?.last_name ?? ''}<br/> ${uCustomer.adjustDate(location.timestamp)}`" />
                    </l-marker>        </l-marker-cluster-group>
      </l-map>
    </div>
    <exp-modal-form                                                                                             
      :title="$t('modules.core.history_location')"                                                              
      :width="1100"                                                                                             
      v-model="modalHistory"                                                                                    
      :btn-save="false"                                                                                         
    >                                                                                                           
      <history-locations :userId="selectedUserId" />                                                            
    </exp-modal-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import useCrud from "@/composables/useCrud";
import { VDateInput } from 'vuetify/labs/VDateInput'
import useCustomer from "@/modules/core/composables/useCustomer";
import ExpPageHeader from "@/components/expPageHeader/expPageHeader.vue";
import { useI18n } from "vue-i18n";
import { useLoading } from "vue-loading-overlay";
import dayjs from "dayjs";

import * as L from 'leaflet'
globalThis.L = L
import { LMap, LTileLayer, LMarker, LTooltip } from '@vue-leaflet/vue-leaflet'
import { LMarkerClusterGroup } from 'vue-leaflet-markercluster'
import 'leaflet/dist/leaflet.css';
import 'vue-leaflet-markercluster/dist/style.css'

import expModalForm from "@/components/expModalForm";
import historyLocations from "../components/history_locations.vue";

const loading = useLoading();
const uCustomer = useCustomer();
const { t } = useI18n();
const companyCrud = useCrud('/api/1.0/core/company');

// Custom marker icons
  const getCustomMarkerIcon = (timestamp: string) => {
    const color = uCustomer.getMarkerColor(timestamp);
    let markerHtml = `<div class="marker-pin marker-${color}"></div><i class="marker-icon mdi mdi-map-marker" style="color: ${color};"></i>`;

    switch (color) {
      case 'green':
        markerHtml = `<div class="marker-pin marker-${color}"></div><i class="marker-icon mdi mdi-map-marker" style="color: green; font-size: 50px;"></i>`;
        break;
      case 'blue':
        markerHtml = `<div class="marker-pin marker-${color}"></div><i class="marker-icon mdi mdi-map-marker" style="color: blue; font-size: 50px;"></i>`;
        break;
      case 'yellow':
        markerHtml = `<div class="marker-pin marker-${color}"></div><i class="marker-icon mdi mdi-map-marker" style="color: gold; font-size: 50px;"></i>`;
        break;
      case 'orange':
        markerHtml = `<div class="marker-pin marker-${color}"></div><i class="marker-icon mdi mdi-map-marker" style="color: orange; font-size: 50px;"></i>`;
        break;
      case 'red':
        markerHtml = `<div class="marker-pin marker-${color}"></div><i class="marker-icon mdi mdi-map-marker" style="color: red; font-size: 50px;"></i>`;
        break;
      default:
        markerHtml = `<div class="marker-pin marker-default"></div><i class="marker-icon mdi mdi-map-marker" style="color: gray; font-size: 50px;"></i>`;
    }

    return L.divIcon({
      className: `custom-div-icon marker-color-${color}`,
      html: markerHtml,
      iconSize: [36, 48], // Increased size of the icon
      iconAnchor: [18, 48] // Adjusted anchor point
    });
  };
// Filter Data
const companies = ref([]);
const bloodTypes = ref([
  { id: "1", label: "A+" },
  { id: "2", label: "A-" },
  { id: "3", label: "B+" },
  { id: "4", label: "B-" },
  { id: "5", label: "AB+" },
  { id: "6", label: "AB-" },
  { id: "7", label: "O+" },
  { id: "8", label: "O-" },
  { id: "9", label: "Unknown" },
]);
const genders = ref([
  { id: 'M', label: 'Male' },
  { id: 'F', label: 'Female' }
]);

// Filter State
const selectedCompanies = ref([]);
const dateRange = ref([]);
const ageMin = ref(null);
const ageMax = ref(null);
const selectedGenders = ref([]);
const selectedBloodTypes = ref([]); 

watch(ageMin, (val) => {
  if (val < 0) ageMin.value = 0;
  if (val > 100) ageMin.value = 100;
});

watch(ageMax, (val) => {
  if (val < 0) ageMax.value = 0;
  if (val > 100) ageMax.value = 100;
});

const ageMaxRule = () => {
  if (ageMin.value && ageMax.value && ageMax.value < ageMin.value) {
    return t('commons.errors.age_max_less_than_min');
  }
  return true;
};

const filterParams = computed(() => {
  const params: any = {};
  if (selectedCompanies.value.length) {
    params['customer__company__in'] = selectedCompanies.value.join(',');
  }
  if (dateRange.value && dateRange.value.length > 0) {
    const startDate = new Date(dateRange.value[0]);
    const endDate = new Date(dateRange.value[dateRange.value.length - 1]);
    if (!isNaN(startDate.getTime()) && !isNaN(endDate.getTime())) {
      params['timestamp__range'] = [
        startDate.toISOString(),
        endDate.toISOString()
      ].join(',');
    }
  }
  if (ageMin.value && ageMax.value) {
    params['customer__customer_info__birth_date__lte'] = new Date(new Date().setFullYear(new Date().getFullYear() - ageMin.value)).toISOString().split('T')[0];
    params['customer__customer_info__birth_date__gte'] = new Date(new Date().setFullYear(new Date().getFullYear() - ageMax.value - 1)).toISOString().split('T')[0];
  }
  if (selectedGenders.value.length) {
    params['customer__customer_info__gender__in'] = selectedGenders.value.join(',');
  }
  if (selectedBloodTypes.value.length) {
    params['customer__customer_info__blood_type__in'] = selectedBloodTypes.value.join(',');
  }
  return params;
});

const locations = ref<any[]>([]);
const zoom = ref(6);
const center = ref([19.3906594,-99.3084211]);
const map = ref<any>(null);
const modalHistory = ref(false);                                                                                
const selectedUserId = ref(null);    

const showHistory = (location: any) => {                                                                        
  selectedUserId.value = location.customer.id;                                                                  
  modalHistory.value = true;                                                                                    
};

const validLocations = computed(() => {
  return locations.value.filter(item => {
    return item?.latitude && item?.longitude && !Number.isNaN(parseFloat(item.latitude)) && !Number.isNaN(parseFloat(item.longitude));
  });
});

const getWsUrl = (): string => {
  return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
};

const loadLocations = async () => {
  if (
    (ageMin.value && !ageMax.value) ||
    (!ageMin.value && ageMax.value) ||
    (ageMin.value && ageMax.value && ageMax.value < ageMin.value)
  ) {
    return;
  }
  console.log("Loading locations with params:", filterParams.value);
  const loader = loading.show({});
  locations.value = await uCustomer.getLastLocations(filterParams.value);
  loader.hide();
};

watch(filterParams, loadLocations, { deep: true });

onMounted(async () => {
  companyCrud.list().then(resp => {
    companies.value = resp;
  });
  await loadLocations();
});

</script>

<style scoped>
.mapContainer {
  width: 100%;
  height: 75vh;
}
</style>