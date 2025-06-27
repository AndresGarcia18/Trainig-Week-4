import re
import pandas

def extract_email(email):
    if pandas.isna(email):
        return ''
    else:
        match = re.search(r'<([^>]+)>', email)
        if match:
            return match.group(1)
        else:
            return ''

def country_recognition(value):
    city_country = {
        "Dublin": "Ireland",
        "Oxford": "England",
        "Limerick": "Ireland",
        "Cork": "Ireland",
        "Winchester": "England",
        "Plymouth": "England",
        "Milton Keynes": "England",
        "London": "England",
        "Waterford": "Ireland"
    }
    known_countries = {"England", "Ireland"}
    value = str(value).strip()
    if value in city_country:
        return (city_country[value], value)
    elif value in known_countries:
        return (value, '')
    else:
        return (value, '')

def format_phone(phone_number: str, country: str) -> tuple[str , str]:
        
    ext_match = re.search(r'(ext\s*\d+)', phone_number, re.IGNORECASE)
    ext = ext_match.group(1) if ext_match else ""

    if ext:
        phone_number = re.sub(r'(ext\s*\d+)', '', phone_number, flags=re.IGNORECASE).strip()

    phone_number = phone_number.replace('-', '').replace(' ', '')
    phone_number = phone_number.lstrip('0')

    if len(phone_number) > 4:
        phone_number = phone_number[:4] + ' ' + phone_number[4:]

    if country.lower() == "england":
        phone_number = "+(44)" + phone_number
    elif country.lower() == "ireland":
        phone_number = "+(353)" + phone_number

    return (phone_number, ext)

def fix_industry_multicheck(value):
    if pandas.isna(value):
        return ""
    value = str(value).strip()

    val_lower = value.lower()
    if val_lower == "poultry and fish":
        return "Poultry;Fish"
    elif val_lower == "fruit and vegetables":
        return "Fruit;Vegetables"
    else:
        return value