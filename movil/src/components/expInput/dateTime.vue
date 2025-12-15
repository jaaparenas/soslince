<template>
  <calculated
    :value="dateTextFormatted"
    @click="openPicker()"
    :label="label"
    :align="'left'"
    :customClass="customClass"
  />
  <exp-modal-form
    v-model="showPicker"
    :width="type == 'date' ? 320 : type == 'time' ? 140 : 420"
    :title="$t('commons.common.select')"
    :btn-save-text="'commons.forms.accept'"
    @fnSave="selectDate"
    :class="['time',].indexOf(type) > -1 ? 'only-time': ''"
    :customClass="'pa-0'"
  >
    <v-row>
      <v-col class="px-0" :cols="`${(type == 'date' ? '12': '9')}`" v-if="['date', 'datetime'].indexOf(type) > -1">
        <v-date-picker
          hide-header
          style="display: block"
          height="340px"
          width="100%"
          v-model="selectedDate"
          :min="props.minDate"
          :max="props.maxDate"
        ></v-date-picker>
      </v-col>
      <v-col class="px-0" :cols="`${(type == 'time' ? '12': '3')}`" v-if="['time', 'datetime'].indexOf(type) > -1">
        <div class="time-value">
          {{ selectedHour }}:{{ selectedMinute }}
        </div>
        <div class="time-picker">
          <div class="hour-picker" ref="hourPicker" @scroll="handleHourScroll">
            <div class="hour" v-for="hour in hours" :key="hour" :class="{ selected: selectedHour === hour }" @click="selectHour(hour)">
              {{ hour }}
            </div>
          </div>
          <div class="minute-picker" ref="minutePicker" @scroll="handleMinuteScroll">
            <div class="minute" v-for="minute in minutes" :key="minute" :class="{ selected: selectedMinute === minute }" @click="selectMinute(minute)">
              {{ minute }}
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </exp-modal-form>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import calculated from "./calculated.vue";
import expModalForm from "@/components/expModalForm";
import dayjs from "dayjs";

const props = defineProps({
  format: {
    type: String,
    default: "",
  },
  minDate: {
    type: String,
    default: "1900-01-01",
  },
  maxDate: {},
  minTime: {
    type: String,
    default: "00:00",
  },
  maxTime: {
    type: String,
    default: "23:59",
  },
  stepTime: {
    type: Number,
    default: 5,
  },
  type: {
    type: String,
    default: "date",
  },
  customClass: {
    type: String,
    default: "white-background",
  },
  label: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["change"]);

const inputVModel = defineModel();
const showPicker = ref(false);

const selectedDate = ref();
const selectedHour = ref("12");
const selectedMinute = ref("00");

const dateTextFormatted = ref("");

const hours = computed(() => {
  return Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'))
});
const minutes = computed(() => {
  return Array.from({ length: 60 / props.stepTime }, (_, i) => (i * props.stepTime).toString().padStart(2, '0'));
});
const hourPicker = ref();
const minutePicker = ref();

const ignoreScrollHour = ref(false);
const ignoreScrollMinute = ref(false);

onMounted(async () => {
  setInitDateTime(inputVModel.value);
});

const openPicker = () => {
  setInitDateTime(inputVModel.value);
  showPicker.value = true;
};

const setInitDateTime = (newValue: any) => {
  if (props.type === "time") {
    if (newValue === "" || newValue === null || newValue === undefined) {
      selectedHour.value = "12";
      selectedMinute.value = "00";
    } else {
      let timeInput = "";
      if(newValue.length > 8 && dayjs(newValue).isValid()) {
        timeInput = newValue;
      } else {
        timeInput = `1900-01-01 ${newValue}`;
      }
      if (!dayjs(timeInput).isValid())
        timeInput = "1900-01-01 12:00:00";

      selectedHour.value = dayjs(timeInput).format("HH").toString();
      selectedMinute.value = dayjs(timeInput).format("mm").toString();
    }
  } else {
    if (newValue === "" || newValue === null || newValue === undefined) {
      newValue = dayjs().format("YYYY-MM-DD");
    }

    if (typeof newValue == "object") {
      try {
        newValue = newValue[0];
      } catch (error) {
        newValue = dayjs().format("YYYY-MM-DD");
      }
    }

    let dateInput: any = dayjs(newValue);
    if (dateInput.isValid()) {
      dateInput = dateInput.toDate();
    } else {
      dateInput = new Date();
    }

    selectedDate.value = dateInput;
    selectedHour.value = dayjs(dateInput).format("HH").toString();
    selectedMinute.value = dayjs(dateInput).format("mm").toString();
  }

  if (props.type === "time" || props.type === "datetime") {
    setTimeout(() => {
      ignoreScrollHour.value = true;
      ignoreScrollMinute.value = true;
      scrollToHour(selectedHour.value);
      scrollToMinute(selectedMinute.value);
    }, 100);
  }

  let outDate = "";
  if (props.type === "time") {
    outDate = `2000-01-01 ${selectedHour.value}:${selectedMinute.value}:00`;
  } else {
    outDate = selectedDate.value;
  }

  dateTextFormatted.value = dayjs(outDate).format(defaultFormat.value);
};

const selectDate = () => {
  let newValue = dayjs(selectedDate.value).format("YYYY-MM-DD");
  showPicker.value = false;
  if (newValue !== inputVModel.value) {
    let outValue = dayjs(selectedDate.value).format("YYYY-MM-DD");

    if (props.type === "datetime") {
      outValue = `${outValue} ${selectedHour.value}:${selectedMinute.value}:00`;
    } else if (props.type === "time") {
      outValue = `${selectedHour.value}:${selectedMinute.value}:00`;
    }

    inputVModel.value = outValue;
    emit("change", outValue);
  }
};

const selectHour = (hour: any) => {
  ignoreScrollHour.value = true;
  selectedHour.value = hour;
  scrollToHour(hour);
};

const selectMinute = (minute: any) => {
  ignoreScrollMinute.value = true;
  selectedMinute.value = minute;
  scrollToMinute(minute);
};

const scrollToHour = (hour: any) => {
  const container = hourPicker.value;
  const hourIndex = (hours.value as any).indexOf(hour);
  if (container && hourIndex !== -1) {
    const hourElement = container.querySelector(`.hour:nth-child(${hourIndex + 1})`);
    container.scrollTop = hourElement.offsetTop - container.offsetTop - container.clientHeight / 2 + hourElement.clientHeight / 2;
  }
};

const scrollToMinute = (minute: any) => {
  const container = minutePicker.value;
  const minuteIndex = (minutes.value as any).indexOf(minute);
  if (container && minuteIndex !== -1) {
    const minuteElement = container.querySelector(`.minute:nth-child(${minuteIndex + 1})`);
    container.scrollTop = minuteElement.offsetTop - container.offsetTop - container.clientHeight / 2 + minuteElement.clientHeight / 2;
  }
};

const handleHourScroll = (event: any) => {
  if (ignoreScrollHour.value) {
    ignoreScrollHour.value = false;
    return;
  }

  const container = event.target;
  const scrollOffset = container.scrollTop;
  const itemHeight = container.clientHeight / (250 / 32);
  let selectedIndex = Math.round(scrollOffset / itemHeight);
  if (selectedIndex > 23) selectedIndex = 23;
  selectedHour.value = (hours.value as any)[selectedIndex];
};

const handleMinuteScroll = (event: any) => {
  if (ignoreScrollMinute.value) {
    ignoreScrollMinute.value = false;
    return;
  }

  const container = event.target;
  const scrollOffset = container.scrollTop;
  const itemHeight = container.clientHeight / (250 / 32);
  let selectedIndex = Math.round(scrollOffset / itemHeight);

  if (selectedIndex > Math.floor((60 / props.stepTime) - 1)) {
    selectedIndex = Math.floor((60 / props.stepTime) - 1);
  }
  selectedMinute.value = (minutes.value as any)[selectedIndex];
};

const defaultFormat = computed(() => {
  if (props.format !== "") return props.format;

  if (props.type === "date") {
    return "YYYY-MM-DD";
  } else if (props.type === "time") {
    return "HH[h] mm[m]";
  } else {
    return "YYYY-MM-DD HH:mm";
  }
});

watch( () => [inputVModel.value], (newValue) => {
  setInitDateTime(newValue);
});
</script>

<style scoped>
.time-value {
  text-align: center;
  margin-top: 14px;
  font-weight: bold;
  padding-bottom: 10px;
  border-left: 1px solid #ccc;
}

.time-picker {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Arial, sans-serif;
  position: relative;
  width: 100%;
  overflow: auto;
  overflow-x: hidden;
  height: 250px;
  border-left: 1px solid #ccc;
}

.hour-picker,
.minute-picker {
  overflow-y: auto;
  overflow-x: hidden;
  margin: 0;
  height: 100%;
  padding-top: 125px;
  padding-bottom: 125px;
}

.hour,
.minute {
  cursor: pointer;
  padding: 8px;
  height: 32px;
  width: 32px;
  font-size: 12px;
  font-weight: bold;
}

.selected {
  background-color: #424242;
  border-radius: 50%;
  color: white;
}

::-webkit-scrollbar {
  background-color: transparent;
}

::-webkit-scrollbar-track {
  background-color: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: transparent;
}

::-webkit-scrollbar-thumb {
  border: transparent;
}

.only-time .hour-picker {
    padding-left: 15px;
    padding-right: 15px;
}
</style>
<style>
.only-time button {
  width: 100% !important;
}

.custom-input-label.active.white-background,
.white-background {
  background: white !important;
}
</style>
