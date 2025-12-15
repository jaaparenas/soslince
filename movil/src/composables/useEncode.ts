const useEncode = () => {
  const base64Encode = (data: string) => {
    try {
      return btoa(data).toString();
    } catch {
      return "";
    }
  };

  const base64Decode = (data: string) => {
    try {
      return atob(data).toString();
    } catch {
      return "";
    }
  };

  const crypt = (salt: string, text: any) => {
    const textToChars = (text: string) =>
      text.split("").map((c: any) => c.charCodeAt(0));
    const byteHex = (n: any) => ("0" + Number(n).toString(16)).substr(-2);
    const applySaltToChar = (code: any) =>
      textToChars(salt).reduce((a: any, b: any) => a ^ b, code);

    return text
      .split("")
      .map(textToChars)
      .map(applySaltToChar)
      .map(byteHex)
      .join("");
  };

  const decrypt = (salt: string, encoded: any) => {
    const textToChars = (text: string) =>
      text.split("").map((c) => c.charCodeAt(0));
    const applySaltToChar = (code: any) =>
      textToChars(salt).reduce((a: any, b: any) => a ^ b, code);
    return encoded
      .match(/.{1,2}/g)
      .map((hex: any) => parseInt(hex, 16))
      .map(applySaltToChar)
      .map((charCode: any) => String.fromCharCode(charCode))
      .join("");
  };

  return {
    base64Encode,
    base64Decode,
    crypt,
    decrypt,
  };
};
export default useEncode;
