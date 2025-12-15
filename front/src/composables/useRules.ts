import { useI18n } from 'vue-i18n'

const useRules = () => {

    const { t } = useI18n()

    return {
        required: (value: any) => !!value || t("commons.validators.required"),
        min8: (value: any) => value.length >= 8 || t("commons.validators.min_8_characters")
    }
}
export default useRules