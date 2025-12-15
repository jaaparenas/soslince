import { defineStore } from "pinia";
import useEncode from "@/composables/useEncode";
import useConst from "@/composables/useConst";

const encode = useEncode();
const consts = useConst();

interface AuthState {
  accessToken: string;
  refreshToken: string;
  userData: string;
}

const dataToken = () => {
  try {
    let dataToken = JSON.parse(
    encode.decrypt(
      consts.saltCrypt,
      encode.base64Decode(localStorage.getItem("lince-auth") ?? "")
    ));
    return dataToken;
  } catch {
    return {};
  }
};

const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    accessToken: dataToken()["accessToken"] ?? "",
    refreshToken: dataToken()["refreshToken"] ?? "",
    userData: dataToken()["userData"] ?? "",
  }),
  getters: {
    getAuthData: (state) => state,
    getAccessToken: (state) => state.accessToken,
    getRefreshToken: (state) => state.refreshToken,
    getUserData: (state) => state.userData,
  },
  actions: {
    setAuthData(data: AuthState) {
      try {
        localStorage.setItem(
          "lince-auth",
          encode.base64Encode(
            encode.crypt(consts.saltCrypt, JSON.stringify(data))
          )
        );
      } catch {
        localStorage.setItem("lince-auth", "");
      }
      this.accessToken = data.accessToken;
      this.refreshToken = data.refreshToken;
      this.userData = data.userData;
    }
  },
});

export default useAuthStore