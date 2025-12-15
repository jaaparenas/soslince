const useConst = () => {
    return {
        baseApi: import.meta.env.VITE_BASE_API,
        baseMedia: import.meta.env.VITE_BASE_MEDIA,
        saltCrypt: import.meta.env.VITE_SALT_CRYPT
    }
}
export default useConst