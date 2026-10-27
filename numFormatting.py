import pandas as pd
import phonenumbers

df = pd.read_csv("test_Gs 1.csv")

country_to_iso_dictionary = {
    'andorra': 'AD', 'argentina': 'AR', 'australia': 'AU', 'aus': 'AU', 'austria': 'AT', 'aut': 'AT',
    'bahamas': 'BS', 'bahrain': 'BH', 'bangladesh': 'BD', 'belarus': 'BY', 'belgium': 'BE', 'bel': 'BE', 'benin': 'BJ',
    'bermuda': 'BM', 'bosnia and herzegovina': 'BA', 'botswana': 'BW', 'brazil': 'BR', 'bra': 'BR',
    'bulgaria': 'BG', 'canada': 'CA', 'ca': 'CA', 'can': 'CA', 'cayman islands': 'KY',
    'chile': 'CL', 'china': 'CN', 'chn': 'CN', 'colombia': 'CO', 'costa rica': 'CR', "cote-d'ivoire": 'CI',
    'croatia': 'HR', 'czech republic': 'CZ', 'denmark': 'DK', 'dnk': 'DK', 'ecuador': 'EC', 'egypt': 'EG',
    'el salvador': 'SV', 'estonia': 'EE', 'finland': 'FI', 'fin': 'FI', 'france': 'FR', 'fra': 'FR',
    'germany': 'DE', 'deu': 'DE', 'ghana': 'GH', 'gibraltar': 'GI', 'greece': 'GR', 'guernsey': 'GG',
    'hong kong': 'HK', 'hkg': 'HK', 'hong kong sar': 'HK', 'hungary': 'HU', 'iceland': 'IS',
    'india': 'IN', 'ind': 'IN', 'indonesia': 'ID', 'ireland': 'IE', 'isle of man': 'IM', 'israel': 'IL',
    'italy': 'IT', 'japan': 'JP', 'jpn': 'JP', 'jersey': 'JE', 'jordan': 'JO', 'kazakhstan': 'KZ',
    'kenya': 'KE', 'kuwait': 'KW', 'latvia': 'LV', 'lebanon': 'LB', 'liechtenstein': 'LI', 'lithuania': 'LT',
    'luxembourg': 'LU', 'madagascar': 'MG', 'malaysia': 'MY', 'mys': 'MY', 'malta': 'MT', 'mauritius': 'MU',
    'mexico': 'MX', 'mex': 'MX', 'monaco': 'MC', 'morocountry_codeo': 'MA', 'namibia': 'NA', 'netherlands': 'NL',
    'nld': 'NL', 'new zealand': 'NZ', 'nigeria': 'NG', 'norway': 'NO', 'oman': 'OM', 'pakistan': 'PK',
    'panama': 'PA', 'peru': 'PE', 'philippines': 'PH', 'poland': 'PL', 'portugal': 'PT', 'puerto rico': 'PR',
    'qatar': 'QA', 'romania': 'RO', 'russian federation': 'RU', 'san marino': 'SM', 'saudi arabia': 'SA',
    'sau': 'SA', 'senegal': 'SN', 'singapore': 'SG', 'sgp': 'SG', 'singapore ': 'SG', 'slovakia': 'SK',
    'slovenia': 'SI', 'south africa': 'ZA', 'zaf': 'ZA', 'south korea': 'KR', 'korea, republic of': 'KR',
    'korea, rep. (south)': 'KR', 'spain': 'ES', 'sri lanka': 'LK', 'sudan': 'SD', 'sweden': 'SE',
    'swe': 'SE', 'switzerland': 'CH', 'che': 'CH', 'taiwan': 'TW', 'twn': 'TW', 'taiwan, r.o.c.': 'TW',
    'tanzania': 'TZ', 'tanzania, united republic of': 'TZ', 'thailand': 'TH', 'tha': 'TH', 'tunisia': 'TN',
    'turkey': 'TR', 'ukraine': 'UA', 'united arab emirates': 'AE', 'are': 'AE', 'united kingdom': 'GB',
    'gbr': 'GB', 'england': 'GB', 'scotland': 'GB', 'united kingdon': 'GB', 'united states': 'US',
    'us': 'US', 'usa': 'US', 'uruguay': 'UY', 'uzbekistan': 'UZ', 'venezuela': 'VE', 'virgin islands': 'VI',
    'virgin islands, u.s.': 'VI', 'vietnam': 'VN', 'zimbabwe': 'ZW'
}

def formatting(row):
    if pd.isna(row['contact_phone1']):
        return "Phone Number Missing"
    
    phone = str(row['contact_phone1']).strip()
    country = str(row['country']).strip()
    
    if country.lower() in ["", "nan", "none"]:
        country = ""
    if phone.lower() in ["", "nan", "none"]:
        return "Missing Phone Number"

    extension = ""
    for marker in ["ext", "ex", "x"]:
        if marker in phone.lower():
            position = phone.lower().index(marker)
            digits_after_marker = phone[position:]
            for c in digits_after_marker:
                if c.isdigit():
                    extension += c
            phone = phone[:position]
            break

    # Manual Updation
    phone = phone.replace('(', '').replace(')', '').strip(' ,;')
    if phone.startswith('00'):
        phone = '+' + phone[2:]
    if phone.startswith('+011'):
        phone = '+' + phone[4:].strip()

    iso = country_to_iso_dictionary.get(country.lower())

    # No country provided, So use phone number and format it        
    if not iso and phone.startswith('+'):
        try:
            number = phonenumbers.parse(phone, None)
        except phonenumbers.NumberParseException as error:
            if error.error_type == phonenumbers.NumberParseException.INVALID_COUNTRY_CODE:
                return "Invalid Country"
            else:
                return "Parsing Error"

        # Using parsed_number, We are predicting the iso
        iso = phonenumbers.region_code_for_number(number) or phonenumbers.region_code_for_country_code(number.country_code)

    country_code = ""
    if iso:
        country_code = str(phonenumbers.country_code_for_region(iso))

    digits = ""
    for c in phone:
        if c.isdigit():
            digits += c

    # Build permutations tries table array without list comprehensions
    tries = [(phone, iso or 'US', extension)]
    tries.append(('+' + digits, None, extension))

    # (iso, size, old, new)
    repairs = [
    ('IT', 0, '', '0'),     # +39 2-8515-4273 -->  +39 02 8515 4273     size = 0 bcoz Italian phone numbers are 6 to 11 digits long
    ('CO', 8, '1', '601'), ('CO', 8, '2', '602'), ('CO', 8, '4', '604'),
    ('CO', 8, '5', '605'), ('CO', 8, '6', '606'), ('CO', 8, '8', '608'),
    ('VN', 9, '4', '24'), ('VN', 9, '8', '28'),
    ('PH', 8, '2', '28'),
    ('GB', 10, '171', '207'), ('GB', 10, '181', '208')
    ]

    # To remove extra country codes like +91 91 91
    d = digits
    if country_code != '' and (digits.startswith(country_code) or not phone.startswith('+')):
        while d.startswith(country_code):
                d = d[len(country_code):]
            
        options = [d, d.lstrip('0')]    # removing trailing zeroes: Some users accidentally type a zero 
        for r, size, old, new in repairs:
            if r == iso and d.startswith(old) and (size == 0 or size == len(d)):
                options.append(new + d[len(old):])
                
        for option in options:
            tries.append(('+' + country_code + option, None, extension))

    '''
        • digits = "5714886000", iso = 'CO' #('CO', 8, '1', '601')
        d → "14886000"
        new num = 6014886000
    '''

    # Checking if its a extension bcoz num with ext might throw Invalid: Large
    last_part = phone.rsplit(' ', 1)[-1]
    if ' ' in phone and last_part.isdigit() and len(last_part) <= 5:
        tries.append((phone.rsplit(' ', 1)[0], iso or 'US', last_part))

    # Storing first for backup -> Can say short or long
    # Trying all combinations and choosing the correct number
    first, number = None, None
    for text, parse_iso, ext in tries:
        try:
            candidate = phonenumbers.parse(text, parse_iso)
        except phonenumbers.NumberParseException:
            continue
        first = first or candidate
        if phonenumbers.is_valid_number(candidate):
            number, extension = candidate, ext
            break

    # If number not valid or unable to guess it
    isValid = False
    if number is None:
        if first is None:
            return "Parsing Error"
        if not iso:
            return "Invalid Country"
            
        reason = phonenumbers.is_possible_number_with_reason(first) #checks if the number looks structurally correct based on its length and formatting rules

        # Converting --> + [Country Code] [Digits].
        if phone.startswith('+'):
            typed = '+' + digits
        else:
            if digits.startswith(country_code) and country_code != '1':
                typed = '+' + country_code + digits[len(country_code):]
            else:
                typed = '+' + country_code + digits
                
        try:
            number = phonenumbers.parse(typed, None)
            is_possible_reason = phonenumbers.is_possible_number_with_reason(number)    #0 means Possible, 1 means Invalid Country Code, 2 means Too Short, and 3 means Too Long 
            isValid = len(str(number.national_number)) >= 6 and is_possible_reason not in (phonenumbers.ValidationResult.TOO_LONG, phonenumbers.ValidationResult.INVALID_COUNTRY_CODE)
        except phonenumbers.NumberParseException:
            pass
            
        if not isValid:
            if reason == phonenumbers.ValidationResult.TOO_SHORT:
                return "Invalid: Too Short"
            elif reason == phonenumbers.ValidationResult.TOO_LONG:
                return "Invalid: Too Long"
            else:
                return "Invalid Number"

    # Formatting standardisation standard outputs strings
    if isValid:
        formatted_phone = f"+{number.country_code} {number.national_number}"
    else:
        formatted_phone = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_phone = formatted_phone.replace('(', '').replace(')', '').replace('-', ' ')
        formatted_phone = " ".join(formatted_phone.split())
        
    if extension:
        formatted_phone += f" ext. {extension}"
        
    return formatted_phone

df['new_formatted_number'] = df.apply(formatting, axis=1)
df.to_csv("test_output.csv", index=False)

print("Saved to test_output.csv !")
