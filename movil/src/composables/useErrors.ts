import { useI18n } from 'vue-i18n'

const useErrors = () => {

    const { t } = useI18n()

    const byCode = (code: number) => {
        let _msg = ""
        switch(code) {
            case 404:
                _msg = t('commons.errors.page_no_found')
                break;
            default:
                _msg = t('commons.errors.undefined_error')
        }
        return _msg;
    }

    const byText = (string: string) => {
        let _msg = ""
        switch(string) {
            case "Page no found":
                _msg = t('commons.errors.page_no_found')
                break;
            case "_BAD_USERNAME_PASSWORD":
                _msg = t('commons.errors.bad_username_password')
                break;
            case "_NO_COORDINATES":
                _msg = t('commons.errors.error_getting_coordinates')
            default:
                _msg = t('commons.errors.undefined_error')
        }
        return _msg;
    }

    return {
        byCode,
        byText
    }
}
export default useErrors