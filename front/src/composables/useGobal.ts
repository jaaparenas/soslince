import useConst from "./useConst";
import useErrors from "./useErrors";
import useToast from "./useToast";
import useMask from "./useMask";

const useGlobal = () => {
  return {
    useConst: useConst,
    useErrors: useErrors,
    useToast: useToast,
    useMask: useMask,
  };
};
export default useGlobal;
