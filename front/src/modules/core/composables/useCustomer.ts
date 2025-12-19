import useAuthStore from "@/modules/auth/stores/auth";
import useGlobalState from "@/stores/global";
import axios from "axios";
import useExport from "@/composables/useExport";
import dayjs from "dayjs";

const sGlobalState = useGlobalState();
const endpoint = "/api/1.0/core"

const useCustomer = () => {

  const getListLocation = (userId: number, page: number, filters: string) => {
    return new Promise((resolve, reject) => {
      axios
        .get(`${endpoint}/customer/list_location/?userId=${userId}&page=${page}&filter=${filters}`)
        .then(async (resp: any) => {
          resolve(resp.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const getListSos = (userId: number, page: number, filters: string) => {
    return new Promise((resolve, reject) => {
      axios
        .get(`${endpoint}/customer/list_sos/?userId=${userId}&page=${page}&filter=${filters}`)
        .then(async (resp: any) => {
          resolve(resp.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const getPendingSos = () => {
    return new Promise((resolve, reject) => {
      axios
        .get(`${endpoint}/customer/list_pending/`)
        .then(async (resp: any) => {
          resolve(resp.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const getCloseSos = (item: any) => {
    return new Promise((resolve, reject) => {
      axios
        .post(`${endpoint}/customer/close_sos/`, item)
        .then(async (resp: any) => {
          resolve(resp.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const getLastLocations = (params: any = {}) => {
    return new Promise((resolve, reject) => {
      axios
        .get(`${endpoint}/customer/last_locations/`, { params })
        .then(async (resp: any) => {
          resolve(resp.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const setPassword = (item: any) => {
    return new Promise((resolve, reject) => {
      axios
        .post(`${endpoint}/customer/password/`, item)
        .then(async (resp: any) => {
          resolve(resp.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const adjustDate = (date: string): string => {
    const fechaUTC = new Date(date);
    return fechaUTC.toLocaleString("en-CA", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false
    }).replace(',', '');
  };

  const getMarkerColor = (timestamp: string): string => {
    const now = dayjs();
    const locationTime = dayjs(timestamp);
    const diffHours = now.diff(locationTime, 'hour');

    if (diffHours < 24) {
      return 'green'; // menos de 24 horas
    } else if (diffHours < 72) { // 3 days * 24 hours
      return 'blue'; // entre 24 y 3 días
    } else if (diffHours < 168) { // 7 days * 24 hours
      return 'yellow'; // entre 3 días y 1 semana
    } else if (diffHours < 360) { // 15 days * 24 hours
      return 'orange'; // entre 1 semana y 15 días
    } else {
      return 'red'; // más de 15 días
    }
  };

  const getExport = (type:string, userId: number, filters: string) => {
    useExport().excel(`${endpoint}/customer/list_${type}/?f=export&userId=${userId}&filter=${filters}`, "data.xlsx")
  }

  return {
    getListLocation,
    getListSos,
    getPendingSos,
    getCloseSos,
    getLastLocations,
    getExport,
    setPassword,
    adjustDate,
    getMarkerColor
  };
};

export default useCustomer;
