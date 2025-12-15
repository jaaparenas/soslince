import { toast } from 'vue3-toastify';
import type { ToastOptions } from 'vue3-toastify';
//import useErrors from "./useErrors";

const useToast = () => {
    //const errors = useErrors()

    const toastError = (msg: string) => {
        toast.error(msg);
    }

    const toastSuccess = (msg: string) => {
        toast.success(msg);
    }

    const toastWarning = (msg: string) => {
        toast.warning(msg);
    }

    const toastInfo = (msg: string) => {
        toast.info(msg);
    }

    const toastHTML = (msg: string, options: ToastOptions = {}) => {
        toast(msg, { ...options, dangerouslyHTMLString: true });
    }

    const toastCustom = (msg: string, options: ToastOptions = {}) => {
        toast(msg, options);
    }

    return {
        toastError,
        toastSuccess,
        toastWarning,
        toastInfo,
        toastHTML,
        toastCustom
    }
}
export default useToast