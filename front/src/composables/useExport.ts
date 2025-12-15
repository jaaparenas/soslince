import { useLoading } from "vue-loading-overlay";
import axios from "axios";

const loading = useLoading();

const useExport = () => {
  const excel = async (endpoint: string, name: string) => {
    const loader = loading.show({});
    await axios
      .get(endpoint.replace('format=datatables', 'export=excel'), { responseType: 'blob' })
      .then((resp: any) => {
          const url = window.URL.createObjectURL(new Blob([resp.data]));
          const a = document.createElement('a');
          a.href = url;
          a.download = name;
          a.click();
          window.URL.revokeObjectURL(url);
      })
      .catch(error => {
          console.error(error);
      });
      loader.hide();
  };

  return {
    excel
  };
};

export default useExport;