const useUtils = () => {

  const consoleLog = (data: any) => {
    console.log(data);
  }

  const isNullOrUndefined = (data: any) => {
    return data == null || data == undefined || typeof data === "undefined";
  }

  const toFloat = (number: any)  => {
    try {
      let nFloat = parseFloat(number)
      if (isNaN(nFloat)) return 0
      return nFloat
    }
    catch { return 0 }
  }

  const isset = (data: any) => {
    return typeof data !== "undefined" && data !== null && data !== "";
  }

  const issetArray = (data: any) => {
    return Array.isArray(data) && data.length > 0;
  }

  const issetObject = (data: any) => {
    return typeof data === 'object' && data !== null && Object.keys(data).length > 0;
  }

  const JsonParse = (data: string) => {
    if (data != null && data !== "") {
      try {
        return JSON.parse(data);
      } catch { }
      try {
        return JSON.parse(data.replace(/'/g, "\"")); // Usar expresión regular en lugar de replaceAll
      } catch { }
    }
    return {};
  }

  const createUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0,
        v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  const getUrlImg = (image: any) => {
    const baseMedia = import.meta.env.VITE_BASE_MEDIA;

    if (image == "" || image == null || image == undefined) return "";

    return `${baseMedia}/${image}`;
  };

  const clone = (data: any) => {
    return JSON.parse(JSON.stringify(data));
  }

  const sortList = (obj: any, sortBy: string) => {
    return obj.sort((item1: any, item2: any) => {
      const obj1 = item1[sortBy] !== undefined ? String(item1[sortBy]).toUpperCase() : "";
      const obj2 = item2[sortBy] !== undefined ? String(item2[sortBy]).toUpperCase() : "";

      if (obj1 < obj2) {
        return -1;
      }
      if (obj1 > obj2) {
        return 1;
      }
      return 0;
    });
  }


  return {
    consoleLog,
    createUUID,
    isNullOrUndefined,
    toFloat,
    isset,
    issetArray,
    issetObject,
    JsonParse,
    getUrlImg,
    clone,
    sortList
  };
};

export default useUtils;