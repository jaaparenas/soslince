import useAuthStore from "@/modules/auth/stores/auth";
import useGlobalState from "@/stores/global";
import axios from "axios";

const sGlobalState = useGlobalState();
const endpoint = "/api/1.0/core"

const useAuth = (authStore: any = null) => {
  if (authStore == undefined) {
    authStore = useAuthStore();
  }

  const authLogIn = (data: any) => {
    return new Promise((resolve, reject) => {
      authLogOut();
      axios
        .post(`/api/1.0/auth/jwt/create`, {
          username: data.username,
          password: data.password,
        })
        .then(async (resp: any) => {
          data = {
            accessToken: resp.data["access"],
            refreshToken: resp.data["refresh"],
            userData: ""
          }
          authStore.setAuthData(data);
          await authData();
          sGlobalState.value.auth = true;
          resolve(resp.data);
        })
        .catch((err) => {
          authLogOut();
          reject(err);
        });
    });
  };

  const authLogOut = () => {
    authStore.setAuthData({
      accessToken: "",
      refreshToken: "",
      userData: ""
    });
    sGlobalState.value.auth = false;
  };

  const authData = () => {
    return new Promise((resolve, reject) => {
      axios
        .get(`${endpoint}/user/data/`)
        .then((resp: any) => {
          const data = {
            accessToken: authStore.getAccessToken,
            refreshToken: authStore.getRefreshToken,
            userData: resp.data,
          }
          authStore.setAuthData(data);
          resolve(resp);
        })
        .catch((err) => {
          reject(err);
        });
    });
  };

  const isAuthenticated = () => {
    return getToken() != "";
  };

  const getUserData = () => {
    return authStore.getUserData || {};
  };

  const getUserId = () => {
    return authStore.getUserData ? authStore.getUserData["id"] : "";
  };

  const getToken = () => {
    return authStore.getAccessToken ?? "";
  };

  return {
    authLogIn,
    authLogOut,
    authData,
    isAuthenticated,
    getUserData,
    getUserId,
    getToken
  };
};

export default useAuth;
