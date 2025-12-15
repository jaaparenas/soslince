import httpRequest from "@/composables/useRequest";

import useGlobalState from "@/stores/global";
import useUtils from "@/composables/useUtils";

const endpoint = "/api/1.0/customer";
const uUtils = useUtils();

const useCore = () => {
  /*
  const getCoordinates = (): Promise<{ latitude: number, longitude: number }> => {
    return new Promise(async (resolve) => {
      const sGlobalState = useGlobalState();
      let latitude = 0;
      let longitude = 0;

      try {
        const lastCoordinates = await Geolocation.getCurrentPosition();
        latitude = lastCoordinates.coords.latitude;
        longitude = lastCoordinates.coords.longitude;
      } catch {
        latitude = (sGlobalState as any).value.latitude ?? 0;
        longitude = (sGlobalState as any).value.longitude ?? 0;
      }

      (sGlobalState as any).value.latitude = latitude;
      (sGlobalState as any).value.longitude = longitude;
      (sGlobalState as any).value.timestamp = new Date().toLocaleString();
      resolve({ latitude: latitude, longitude: longitude });
    });
  }
  */

  const sendSos = (key: string, latitude: number, longitude: number) => {
    return new Promise((resolve, reject) => {
      httpRequest
        .post(`${endpoint}/sos/`, { key, latitude, longitude })
        .then((resp: any) => {
          resolve(resp);
        })
        .catch((err: any) => {
          reject(err);
        });
    });
  };

  const sendLocation = (latitude: number, longitude: number) => {
    return new Promise((resolve, reject) => {
      httpRequest
        .post(`${endpoint}/location/`, { latitude, longitude })
        .then((resp: any) => {
          resolve(resp);
        })
        .catch((err: any) => {
          reject(err);
        });
    });
  };

  const getUserData = () => {
    return new Promise((resolve, reject) => {
      httpRequest
        .get(`${endpoint}/data/`)
        .then((resp: any) => {
          resolve(resp);
        })
        .catch((err: any) => {
          reject(err);
        });
    });
  }

  const updateUserData = (data: any) => {
    return new Promise((resolve, reject) => {
      httpRequest
        .post(`${endpoint}/profile/`, uUtils.JsonParse(JSON.stringify(data)))
        .then((resp: any) => {
          resolve(resp);
        })
        .catch((err: any) => {
          reject(err);
        });
    });
  };

  const updateUserPassword = (data: any) => {
    return new Promise((resolve, reject) => {
      httpRequest
        .post(`${endpoint}/password/`, data)
        .then((resp: any) => {
          resolve(resp);
        })
        .catch((err: any) => {
          reject(err);
        });
    });
  };

  return {
    sendSos,
    sendLocation,
    //getCoordinates,
    getUserData,
    updateUserData,
    updateUserPassword,
  };
};

export default useCore;
