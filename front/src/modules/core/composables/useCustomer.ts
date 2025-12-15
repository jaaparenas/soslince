import useAuthStore from "@/modules/auth/stores/auth";
import useGlobalState from "@/stores/global";
import axios from "axios";
import useExport from "@/composables/useExport";

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

  const getExport = (type:string, userId: number, filters: string) => {
    useExport().excel(`${endpoint}/customer/list_${type}/?f=export&userId=${userId}&filter=${filters}`, "data.xlsx")
  }

  return {
    getListLocation,
    getListSos,
    getPendingSos,
    getCloseSos,
    getExport,
    setPassword,
    adjustDate
  };
};

export default useCustomer;
