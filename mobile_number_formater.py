import pandas as pd

source_path = r"C:\Users\suganya\Downloads\test_Gs 1.csv"
destination_path = r"C:\Users\suganya\Downloads\sample.csv"

df = pd.read_csv(source_path, nrows=300000, encoding='utf-8-sig')

df.columns = df.columns.str.strip() # Clean column headers to prevent spacing bugs

# Removing duplicates
print(f"Total rows loaded: {len(df)}")
df = df.drop_duplicates(subset=['contact_cust_id'], keep='first')   # keep the first encountered and delete duplicate after this
print(f"Unique rows to process: {len(df)}")

dial_codes = {
    'Lithuania': '+370', 'Indonesia': '+62',
    'India': '+91', 'IND': '+91',
    'United States': '+1', 'US': '+1', 'USA': '+1', 'UNITED STATES': '+1', 'UNITED States': '+1', 'usa': '+1', 'united states': '+1', 'United states': '+1', 
    'CA': '+1', 'Canada': '+1', 'canada': '+1', 'CAN': '+1', 'Puerto Rico': '+1', 'Virgin Islands': '+1', 'Virgin Islands, U.S.': '+1',
    'United Kingdom': '+44', 'England': '+44', 'Scotland': '+44', 'GBR': '+44', 'United Kingdon': '+44', 'Guernsey': '+44', 'Jersey': '+44', 'Isle of Man': '+44',
    'United Arab Emirates': '+971', 'ARE': '+971', 'Bahrain': '+973', 'Kuwait': '+965', 'Qatar': '+974', 'Saudi Arabia': '+966', 'SAU': '+966', 'Oman': '+968', 'Jordan': '+962', 'Lebanon': '+961',
    'Japan': '+81', 'JPN': '+81', 'China': '+86', 'CHN': '+86', 'Hong Kong': '+852', 'HONG KONG': '+852', 'Hong Kong SAR': '+852', 'HKG': '+852',
    'Singapore': '+65', 'Singapore ': '+65', 'SGP': '+65', 'Malaysia': '+60', 'MYS': '+60', 'Thailand': '+66', 'THA': '+66', 'Taiwan': '+886', 'Taiwan, R.O.C.': '+886', 'TWN': '+886',
    'South Korea': '+82', 'Korea, Republic of': '+82', 'Korea, Rep. (South)': '+82', 'Vietnam': '+84', 'Pakistan': '+92', 'Bangladesh': '+880', 'Philippines': '+63', 'Sri Lanka': '+94', 'Uzbekistan': '+998', 'Kazakhstan': '+7',
    'Germany': '+49', 'DEU': '+49', 'France': '+33', 'FRA': '+33', 'Netherlands': '+31', 'NLD': '+31', 'Spain': '+34', 'Italy': '+39', 'Switzerland': '+41', 'CHE': '+41', 'Ireland': '+353', 'Norway': '+47', 'Sweden': '+46', 'SWE': '+46', 'Denmark': '+45', 'DNK': '+45', 'Finland': '+358', 'FIN': '+358', 'Belgium': '+32', 'BEL': '+32',
    'Poland': '+48', 'Austria': '+43', 'Luxembourg': '+352', 'Liechtenstein': '+423', 'Ukraine': '+380', 'Slovenia': '+386', 'Czech Republic': '+420', 'Hungary': '+36', 'Romania': '+40', 'Croatia': '+385', 'Greece': '+30', 'Iceland': '+354', 'Estonia': '+372', 'Latvia': '+371', 'Portugal': '+351', 'Andorra': '+376', 'Slovakia': '+421', 'Bulgaria': '+359', 'Malta': '+356', 'Monaco': '+377', 'San Marino': '+378', 'Gibraltar': '+350', 'Bosnia and Herzegovina': '+387',
    'Australia': '+61', 'AUS': '+61', 'New Zealand': '+64',
    'Brazil': '+55', 'BRA': '+55', 'Mexico': '+52', 'MEX': '+52', 'Peru': '+51', 'Colombia': '+57', 'Chile': '+56', 'Argentina': '+54', 'Ecuador': '+593', 'Uruguay': '+598', 'Venezuela': '+58', 'Panama': '+507', 'Costa Rica': '+506', 'El Salvador': '+503', 'Bahamas': '+1', 'Cayman Islands': '+1', 'Bermuda': '+1',
    'South Africa': '+27', 'ZAF': '+27', 'Morocco': '+212', 'Egypt': '+20', 'Tanzania': '+255', 'Tanzania, United Republic of': '+255', 'Kenya': '+254', 'Nigeria': '+234', 'Ghana': '+233', 'Botswana': '+267', 'Madagascar': '+261', "Cote-D'Ivoire": '+225', 'Zimbabwe': '+263', 'Namibia': '+264', 'Sudan': '+249', 'Benin': '+229', 'Tunisia': '+216', 'Senegal': '+221', 'Mauritius': '+230',
    'Russian Federation': '+7', 'Turkey': '+90', 'Israel': '+972', 'Belarus': '+375'
}

def format_clean_numbers(row):
    raw_phone = str(row['contact_phone1'])
    country_name = str(row['country']).strip()
    
    dial_code = dial_codes.get(country_name)
    if not dial_code:
        return f"Check Country: ({country_name})"
        
    main_digits = ''.join(c for c in raw_phone if c.isdigit())
    
    clean_code_digits = dial_code.replace('+', '')
    if main_digits.startswith(clean_code_digits):
        main_digits = main_digits[len(clean_code_digits):]
    elif main_digits.startswith('0'): 
        main_digits = main_digits[1:]

    if len(main_digits) >= 6:
        midpoint = len(main_digits) // 2
        first_half = main_digits[:midpoint]
        second_half = main_digits[midpoint:]
        
        return f"{dial_code} {first_half} {second_half}"
    else:
        return f"Invalid Digits: {raw_phone}"

print("Processing data and formatting numbers row-by-row...")
df['Formatted_Phone'] = df.apply(format_clean_numbers, axis=1)  #creating new column and axis = 1 -> move horizontally row by row, axis = 1 -> move vertically col by col

subset_df = df[['contact_cust_id', 'Formatted_Phone']]

subset_df.to_csv(destination_path, index=False)
print(f"\nSuccess! Separate file created at:\n{destination_path}")