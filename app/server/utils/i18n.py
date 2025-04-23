from .locales_dict import TRANSLATIONS

DEFAULT_LOCALE = 'en'

def translate_error(err_code: str, locale: str = DEFAULT_LOCALE) -> str:
    return TRANSLATIONS.get(locale, {}).get(err_code, err_code)
