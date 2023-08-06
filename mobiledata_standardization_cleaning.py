# Import libraries
import pandas as pd
import numpy as np
import re

# Read CSV file and check shape
df = pd.read_csv(r"/content/ml_project/flipkart_mobile.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)
df.shape

# Check Null values in Brand column
df['Brand'].isnull().sum()

# Aggrigate Phone Model and Phone Color
df[['PhoneModel', 'PhoneColor']] = df['PhoneName'].str.split('(', n=1, expand=True)
df[['PhoneColor','C_ROM']] = df['PhoneColor'].str.split(',', n=1, expand=True)

# Check Null values in PhoneModel column
df['PhoneModel'].isnull().sum()

def determine_networktype(phone_model):
    if '5G' in phone_model:
        return 5
    elif '4G' in phone_model:
        return 4
    elif '3G' in phone_model:
        return 3
    else:
        return 0

df['NetworkType'] = df['PhoneModel'].apply(determine_networktype)

df['NetworkType'].isnull().sum()

remove_gen = ['5G', '4G', '3G']
df['PhoneModel'] = df['PhoneModel'].replace('|'.join(remove_gen), '', regex=True)
df['PhoneModel']

df[~df['PhoneModel'].str.contains(r'3G|4G|5G', case=False)]

# Check Null values in PhoneColor column
df['PhoneColor'].isnull().sum()

# Fill Null values in PhoneColor column
df['PhoneColor'].fillna('NA Color', inplace = True)

df.sort_values(by=['PhoneColor'])

df.loc[df[df['PhoneColor'].str.contains('support')].index, 'PhoneColor'] = 'NA Color'
df.loc[df[df['PhoneColor'].str.contains('WiFi')].index, 'PhoneColor'] = 'NA Color'
df.loc[df[df['PhoneColor'].str.contains('PRODUCT')].index, 'PhoneColor'] = 'NA Color'
df.loc[df[df['PhoneColor'].str.contains('inch', case=False)].index, 'PhoneColor'] = 'NA Color'
df.loc[[5231, 5258, 7520], 'PhoneColor'] = ['BLACK', 'SILVER', 'NA Color']
df.loc[df[df['PhoneColor'].str.contains(r'200|256|2018|2023', case=False)].index, 'PhoneColor'] = ['RED', 'Champagne', 'Blue', 'NA Color', 'Terracotta Red', 'Charcoal', 'NA Color', 'Reliance', 'NA Color']
df.loc[df[(df['Brand'] == 'Nothing')].index, 'PhoneColor'] = ['Dark Grey', 'White', 'Dark Grey', 'White', 'Dark Grey', 'White', 'Black', 'Black', 'Black', 'White']
df.loc[df[df['PhoneColor'].str.contains('150W', case=False)].index, 'PhoneColor'] = ['Sprint White', 'Nitro Blue', 'Nitro Blue', 'Asphalt Black']
df.loc[df[df['PhoneColor'].str.contains(r'2nd|3rd', case=False)].index, 'PhoneColor'] = ['Black Leather', 'Red', 'White', 'Gold', 'Yellow']

filter_color = df[df['PhoneColor'].str.contains(r'5G|4G|3G', case=False)]
df.loc[filter_color.index, 'PhoneColor'] = ['Gold', 'NA Color', 'NA Color', 'Black', 'Latte Gold', 'Metal Gold', 'Gold']
df.loc[filter_color.index, 'PhoneName'] = ['SAMSUNG Galaxy J1 4G', 'itel MagicX Pro 4G', 'itel MagicX Pro 4G', 'IQOO 3 5G', 'XOLO Era 2X', 'Alcatel Pixi 4 4G', 'Alcatel Pixi 4 4G']

df['PhoneColor'] = df['PhoneColor'].str.replace("?", "")
df['PhoneColor'] = df['PhoneColor'].str.upper()
df['PhoneModel'] = df['PhoneModel'].str.upper()

df['PhoneColor']

# Check Null values in ProductRating column
df['ProductRating'].isnull().sum()

filter_ProductRating = df[(df['ProductRating'].isnull())]  # Filter Null values in ProductRating column
df['ProductRating'].fillna(0, inplace = True) # Fill Null values in ProductRating column

df[['Num_Ratings', 'Num_Reviews']] = df['Num_Rating_review'].str.split('&', n=1, expand=True) # Aggrigate Ratings and Reviews from Num_Rating_review column
df['Num_Ratings'] = df['Num_Ratings'].str.replace('Ratings','').str.replace(',', '')  # Remove Ratings and , into Ratings column
df['Num_Reviews'] = df['Num_Reviews'].str.replace('Reviews','').str.replace(',', '')  # Remove Reviews and , into Reviews column

df['Num_Ratings'].fillna(0, inplace = True) # Fill Null values in Ratings column
df['Num_Reviews'].fillna(0, inplace = True) # Fill Null values in Reviews column

df['Num_Ratings']= df['Num_Ratings'].astype(int)
df['Num_Reviews']= df['Num_Reviews'].astype(int)

df['comingsoon'].unique() # Chekc unique values in comingsoon column

filter_comingsoon = df[df['comingsoon'].str.contains('Coming Soon')]  # Filter comingsoon column
df.loc[filter_comingsoon.index, 'availability'] = filter_comingsoon['comingsoon']

filter_preorder = df[df['comingsoon'].str.contains('Pre Order')] # Filter comingsoon column
df.loc[filter_preorder.index, 'availability'] = filter_preorder['comingsoon']

df['availability'].unique() # Chekc unique values in availability column

df.columns

# Remove ₹ and , from DiscountPrice and OriginalPrice columns
df['DiscountPrice'] = df['DiscountPrice'].str.replace('[₹,]', '', regex=True)
df['OriginalPrice'] = df['OriginalPrice'].str.replace('[₹,]', '', regex=True)

df['DiscountPrice'].isnull().sum() # Check Null values in DiscountPrice column

# Filter and fill DiscountPrice, OriginalPrice, and Discount based ot phone availability
filter_DiscountPrice = df[(df['DiscountPrice'].isnull()) & (df['availability'] == 'Currently unavailable')]
filter_DiscountPrice['DiscountPrice'].fillna(0, inplace=True)
df.loc[filter_DiscountPrice.index, 'DiscountPrice'] = filter_DiscountPrice['DiscountPrice']
df.loc[filter_DiscountPrice.index, 'OriginalPrice'] = filter_DiscountPrice['DiscountPrice']
df.loc[filter_DiscountPrice.index, 'Discount'] = '0% off'

df['DiscountPrice'].isnull().sum() # Check Null values in DiscountPrice column

df['OriginalPrice'].isnull().sum()  # Check Null values in OriginalPrice column

# Filter OriginalPrice column based on availability of phone
filter_OriginalPrice = df[(df['OriginalPrice'].isnull()) & (df['Discount'].isnull()) & ((df['availability'] == 'Currently unavailable') | (df['availability'] == 'Coming Soon'))]
filter_OriginalPrice['OriginalPrice'].fillna(filter_OriginalPrice['DiscountPrice'], inplace=True)
df.loc[filter_OriginalPrice.index, 'OriginalPrice'] = filter_OriginalPrice['DiscountPrice']
df.loc[filter_OriginalPrice.index, 'Discount'] = '0% Off'

df['OriginalPrice'].isnull().sum()  # Check Null values in OriginalPrice column

# Filter and fill null values in OriginalPrice column
filter_OriginalPrice_null = df[df['OriginalPrice'].isnull()]
df.loc[filter_OriginalPrice_null.index, 'OriginalPrice'] = filter_OriginalPrice_null['DiscountPrice']
df.loc[filter_OriginalPrice_null.index, 'Discount'] = '0% off'

df['OriginalPrice'].isnull().sum() # Check Null values in OriginalPrice column

df[df['Discount'].isnull()] # Check Null values in Discount column

# Filter and fill Discount based on availability of phone
filter_Discount = df[(df['Discount'].isnull()) & ((df['availability'] == 'Currently unavailable') | (df['availability'] == 'Coming Soon') | (df['availability'] == 'Pre Order'))]
df.loc[filter_Discount.index, 'Discount'] = '0% Off'

# Fill null values in Discount column
df['Discount'].fillna('0% off', inplace=True)

df['Discount'].isnull().sum()

df['Discount']

# Remove % off and cast as int Discount column
df['Discount'] = df['Discount'].str.replace('% off', '', case=False).astype(int)

df['Discount']

df['Deals'].unique() #Check unique values in Deals column

df['exchange_offer'] = np.where(df['Deals'].str.contains('Exchange', case=False), 1, 0)
df['bank_offer'] = np.where(df['Deals'].str.contains('Bank Offer|EMI', case=False), 1, 0)
df['saver_deal'] = np.where(df['Deals'].str.contains('Saver'), 1, 0)


df[['RAM_ROM_Exp', 'Display', 'Camera', 'Battery', 'Processor', 'Warranty']] = df['Specification'].str.split(',', n=5, expand=True)

df[['RAM', 'ROM', 'Expandable']] = df['RAM_ROM_Exp'].str.split('|', n=2, expand=True)

df['RAM'].unique()

filter_ram_asrom = df[(df['RAM'].str.contains('ROM', case=False)) & (df['ROM'].isnull())]
df.loc[filter_ram_asrom.index, 'ROM'] = filter_ram_asrom['RAM']

filter_ramasrom = df[df['RAM'].str.contains('ROM', case=False)]
df.loc[filter_ramasrom.index, 'RAM'] = '0 MB RAM'

apple_df = df[(df['Brand'] == 'APPLE')]['Specification'].str.split(',', n=4, expand=True)
df.loc[apple_df.index, 'ROM'] = apple_df[0]
df.loc[apple_df.index, 'Display'] = apple_df[1]
df.loc[apple_df.index, 'Camera'] = apple_df[2]
df.loc[apple_df.index, 'Processor'] = apple_df[3]
df.loc[apple_df.index, 'Warranty'] = apple_df[4]

filter_ramasdisplay = df[(df['RAM'].str.contains('Display', case=False)) & (df['Display'].isnull())]
df.loc[filter_ramasdisplay.index, 'Display'] = df['RAM']
df.loc[filter_ramasdisplay.index, 'RAM'] = '0 MB RAM'

filter_ramasexpa = df[(df['RAM'].str.contains('Expandable', case=False)) & (df['Expandable'].isnull())]
df.loc[filter_ramasexpa.index, 'Expandable'] = df['RAM']
df.loc[filter_ramasexpa.index, 'RAM'] = '0 MB RAM'

df['RAM'].unique()

df[df['RAM'].str.contains('Display')]

filter_dis = df[(df['Display'].str.contains('Warranty', case=False)) & (df['Warranty'].isnull())]
df.loc[filter_dis.index, 'Warranty'] = filter_dis['Display']
df.loc[filter_dis.index, 'Display'] = filter_dis['RAM']
df.loc[filter_dis.index, 'RAM'] = '0 MB RAM'

filter_dis_batt = df[df['Display'].str.contains('Battery', case=False)]
df.loc[filter_dis_batt.index, 'Battery'] = filter_dis_batt['Display']
df.loc[filter_dis_batt.index, 'Display'] = filter_dis_batt['RAM']
df.loc[filter_dis_batt.index, 'RAM'] = '0 MB RAM'

filter_dis_war = df[(df['Display'].str.contains('Year', case=False))]
df.loc[filter_dis_war.index, 'Warranty'] = filter_dis_war['Display']
df.loc[filter_dis_war.index, 'Display'] = filter_dis_war['RAM']
df.loc[filter_dis_war.index, 'RAM'] = '0 MB RAM'

filter_dis_cam = df[df['Display'].str.contains('Camera')]
df.loc[filter_dis_cam.index, 'Warranty'] = filter_dis_cam['Battery']
df.loc[filter_dis_cam.index, 'Battery'] = filter_dis_cam['Camera']
df.loc[filter_dis_cam.index, 'Camera'] = filter_dis_cam['Display']
df.loc[filter_dis_cam.index, 'Display'] = filter_dis_cam['RAM']
df.loc[filter_dis_cam.index, 'RAM'] = '0 MB RAM'

df['RAM'] = df['RAM'].str.replace(r'\[|\]|\'', '', regex=True)

filter_ram = df[~df['RAM'].str.contains(r'TB|GB|MB|KB|NA', case=False)]
df.loc[filter_ram.index, 'RAM'] = ['0.53 MB RAM', '32 MB RAM', '32 MB RAM', '32 MB RAM']

df['RAM'].unique()

df['RAM'].isnull().sum()

# Function to convert RAM from MB to GB
def convert_mb_to_gb(ram_value):
    if 'GB' in ram_value:
        return ram_value
    elif 'MB' in ram_value:
        mb_value = float(ram_value.split(' MB')[0])
        gb_value = mb_value / 1024
        return f"{gb_value:.3f} GB RAM"
    else:
        return '0 GB RAM'

# Apply the conversion function to the 'RAM' column
df['RAM'] = df['RAM'].apply(convert_mb_to_gb)

df['RAM'] = df['RAM'].str.replace('GB RAM', '')

df['RAM'].unique

df['ROM'].isnull().sum()

df['ROM'].unique()

filter_rom_exp = df[(df['ROM'].str.contains('Expandable', case=False)) & (df['Expandable'].isnull())]
df.loc[filter_rom_exp.index, 'Expandable'] = df['ROM']
df.loc[filter_rom_exp.index, 'ROM'] = '0 MB ROM'

df['ROM'] = df['ROM'].str.replace(r'(\d+)\s+ROM', r'\1MB ROM', regex=True)

df['ROM'].unique()

filter_rom_null = df[(df['ROM'].isnull()) & (~df['Specification'].str.contains('ROM', case=False))]
df.loc[filter_rom_null.index, 'ROM'] = '0 MB ROM'

df['ROM'].isnull().sum()

filter_null_rom = df[df['ROM'].isnull()]
df.loc[filter_null_rom.index, 'Warranty'] = filter_null_rom['Processor']
df.loc[filter_null_rom.index, 'Processor'] = 'NA Processor'
df.loc[filter_null_rom.index, 'ROM'] = '0 MB ROM'

df['ROM'].isnull().sum()

filter_rom = df[~df['ROM'].str.contains(r'TB|GB|MB|KB|NA', case=False)]
filter_rom = df.loc[filter_rom_exp.index]
rom = filter_rom['RAM_ROM_Exp'].str.split('|', expand=True)
df.loc[filter_rom_exp.index, 'ROM'] = rom[0]

df['ROM'] = df['ROM'].str.replace(r'\[|\]|\'', '', regex=True).str.replace(r'\$\$', ' ', regex=True)

df['ROM'].unique()

filter_rom = df[df['ROM'].str.contains('/')]
df.loc[[4212,4434,4439,4448,4455], 'ROM'] = ['16 GB ROM', '64 MB ROM', '64 MB ROM', '32 MB ROM', '64 MB ROM']

df.loc[df[df['ROM'].str.contains('NA')].index, 'ROM'] = '0 MB ROM'

df['ROM'].unique()

filter_rom = df[df['ROM'].str.contains('+', regex=False)]

df.loc[filter_rom.index, 'ROM'] = '32 GB ROM'
df.loc[filter_rom.index, 'Expandable'] = '3 GB ROM'

pattern = r'^\s*(\d+(\.\d+)?)\s*(TB|GB|MB|KB)\s*'
def convert_to_gb(rom_size):
    match = re.match(pattern, rom_size)
    if match:
        value, _, unit = match.groups()
        value = float(value)
        if unit == 'TB':
            return value * 1024
        elif unit == 'GB':
            return value
        elif unit == 'MB':
            return value / 1024
        elif unit == 'KB':
            return value / (1024 * 1024)
    else:
        return None

# Apply the conversion function to the 'ROM' column and create a new 'ROM_GB' column
df['ROM'] = df['ROM'].apply(convert_to_gb)

df['ROM'].unique

df['RAM'].unique()

df['ROM'].unique()

df['Expandable'].isnull().sum()

filter_exp_null = df[(df['Expandable'].isnull()) & (~df['Specification'].str.contains('Expandable', case=False))]
df.loc[filter_exp_null.index, 'Expandable'] = '0 TB Expandable'

df['Expandable'].isnull().sum()

df.loc[df[df['Expandable'].isnull()].index, 'Expandable'] = '0 TB Expandable'

df['Expandable'] = df['Expandable'].str.replace(r'\'', '', regex=True)

df['Expandable'] = df['Expandable'].str.replace('\[', '').str.replace('Upto', '').str.replace('Expandable', '')

df['Expandable'].unique()

def convert_storage_to_gb(storage_value):
    if 'TB' in storage_value:
        tb_value = float(storage_value.split(' TB')[0])
        gb_value = tb_value * 1024
        return f"{gb_value:.3f}"
    elif 'GB' in storage_value:
        gb_value = float(storage_value.split(' GB')[0])
        return f"{gb_value:.3f}"
    elif 'MB' in storage_value:
        mb_value = float(storage_value.split(' MB')[0])
        gb_value = mb_value / 1024
        return f"{gb_value:.3f}"
    else:
        return '0'

df['Expandable'] = df['Expandable'].apply(convert_storage_to_gb)

df['Expandable'].unique()

df[(~df['Display'].str.contains('Display', case=False)) & (df['Specification'].str.contains('Display', case=False))]

df[df['Display'].str.contains('Display', case=False)]

df['Display'].isnull().sum()

df['Camera'].isnull().sum()

filter_cam = df[(df['Camera'].isnull()) & (~df['Specification'].str.contains('Camera'))]
df.loc[filter_cam.index, 'Camera'] = 'NA Camera'

df['Camera'].isnull().sum()

df[~df['Camera'].str.contains('Camera')]

df['Battery'].isnull().sum()

filter_batt = df[(df['Battery'].isnull()) & (~df['Specification'].str.contains('Battery'))]
df.loc[filter_batt.index, 'Battery'] = 'Battery info. unavailable'

df['Battery'].isnull().sum()

df['Processor'].isnull().sum()

filter_proc = df[(df['Processor'].isnull()) & (~df['Specification'].str.contains('Processor'))]
df.loc[filter_proc.index, 'Processor'] = 'NA Processor'

df['Processor'].isnull().sum()

df[~df['Battery'].str.contains('Battery')]

filter_bat_warr = df[(df['Battery'].str.contains('Warranty')) & (df['Warranty'].isnull())]
df.loc[filter_bat_warr.index, 'Warranty'] = filter_bat_warr['Battery']
df.loc[filter_bat_warr.index, 'Battery'] = 'Battery info. unavailable'

filter_batt_year = df[((df['Battery'].str.contains('year', case=False)) | (df['Battery'].str.contains('Months', case=False))) & (df['Warranty'].isnull())]
df.loc[filter_batt_year.index, 'Warranty'] = filter_batt_year['Battery']
df.loc[filter_batt_year.index, 'Battery'] = 'Battery info. unavailable'

filter_pro = df[(df['Processor'].str.contains('Year',case=False)) & (df['Warranty'].isnull()) & (df['Specification'].str.contains('Year',case=False)) & (~df['Specification'].str.contains('Processor',case=False))]
df.loc[filter_pro.index, 'Processor'] = 'NA Processor'

filter_pro_bat = df[(df['Processor'].str.contains('Year',case=False)) & (df['Battery'].str.contains('Processor',case=False)) & (df['Warranty'].isnull())]
df.loc[filter_pro_bat.index, 'Warranty'] = filter_pro_bat['Processor']
df.loc[filter_pro_bat.index, 'Processor'] = filter_pro_bat['Battery']
df.loc[filter_pro_bat.index, 'Battery'] = filter_pro_bat['Camera']
df.loc[filter_pro_bat.index, 'Camera'] = 'NA Camera'

filter_bat_mon = df[(df['Battery'].str.contains('month'))]
df.loc[filter_bat_mon.index, 'Warranty'] = filter_bat_mon['Battery']
df.loc[filter_bat_mon.index, 'Battery'] = filter_bat_mon['Camera']
df.loc[filter_pro_bat.index, 'Camera'] = 'NA Camera'

filter_batpro_apple = df[(df['Battery'].str.contains('Processor')) & (df['Brand'] == 'APPLE')]
df.loc[filter_batpro_apple.index, 'Battery'] = 'Battery info. unavailable'

filter_bat_app = df[(~df['Battery'].str.contains('Battery')) & (df['Brand'] == 'APPLE')]
df.loc[filter_bat_app.index, 'Battery'] = 'Battery info. unavailable'

filter_pro_mon = df[(df['Processor'].str.contains('Months',case=False)) & (df['Warranty'].isnull())]
df.loc[filter_pro_mon.index, 'Warranty'] = filter_pro_mon['Processor']
df.loc[filter_pro_mon.index, 'Processor'] = 'Processor info. unavailable'

filter_bat_mon = df[(df['Battery'].str.contains('Month')) & (df['Warranty'].isnull())]
df.loc[filter_bat_mon.index, 'Warranty'] = filter_bat_mon['Battery']
df.loc[filter_bat_mon.index, 'Battery'] = filter_bat_mon['Camera']
df.loc[filter_bat_mon.index, 'Camera'] = 'NA Camera'

filter_bat_cam = df[(df['Battery'].str.contains('Camera', case=False))]

filter_bat_cam = df[(df['Battery'].str.contains('Camera', case=False))]
df.loc[filter_bat_cam.index, 'Camera'] = filter_bat_cam['Camera'] + filter_bat_cam['Battery']
df.loc[filter_bat_cam.index, 'Battery'] = filter_bat_cam['Processor']

df.loc[filter_bat_cam.index, 'Processor'] = filter_bat_cam['Warranty'].str.split(',', n=1, expand=True)[0]

filter_bat_itel = df[(df['Battery'].str.contains('Processor', case=False)) & (df['Brand'] == 'itel')]
df.loc[filter_bat_itel.index, 'Processor'] = filter_bat_itel['Battery']
df.loc[filter_bat_itel.index, 'Battery'] = filter_bat_itel['Camera']
df.loc[filter_bat_itel.index, 'Camera'] = 'NA Camera'

filter_bat = df[~df['Battery'].str.contains('Battery')]
df.loc[filter_bat.index, 'Battery'] = filter_bat['Camera']
df.loc[filter_bat.index, 'Camera'] = 'NA Camera'

df[~df['Battery'].str.contains('Battery')]

filter_cam_bat = df[(df['Camera'].str.contains('Battery', case=False)) & (df['Battery'] == 'Battery info. unavailable')]
df.loc[filter_cam_bat.index, 'Battery'] = filter_cam_bat['Camera']
df.loc[filter_cam_bat.index, 'Camera'] = 'NA Camera'

filter_cam_batt = df[(df['Camera'].str.contains('Battery', case=False))]
df.loc[filter_cam_batt.index, 'Battery'] = filter_cam_batt['Camera']
df.loc[filter_cam_batt.index, 'Camera'] = 'NA Camera'

filter_cam_war = df[df['Camera'].str.contains(r'Warranty|Months', case=False)]
df.loc[filter_cam_war.index, 'Warranty'] = filter_cam_batt['Camera']
df.loc[filter_cam_war.index, 'Camera'] = 'NA Camera'

df[~df['Processor'].str.contains('Processor')]

filter_pro_warr = df[(df['Processor'].str.contains('Warranty', case=False)) & (df['Specification'].str.contains('Warranty')) & (df['Warranty'].isnull())]
df.loc[filter_pro_warr.index, 'Warranty'] = filter_pro_warr['Processor']
df.loc[filter_pro_warr.index, 'Processor'] = 'Processor info. unavailable'

filter_pro = df[(df['Processor'].str.contains('Warranty', case=False))]
df.loc[filter_pro.index, 'Warranty'] = filter_pro['Processor'] + filter_pro['Warranty']
df.loc[filter_pro.index, 'Processor'] = 'Processor info. unavailable'

filter_pro_mon = df[(df['Processor'].str.contains('month', case=False)) & (df['Specification'].str.contains('month', case=False)) & (df['Warranty'].isnull())]
df.loc[filter_pro_mon.index, 'Warranty'] = filter_pro_mon['Processor']
df.loc[filter_pro_mon.index, 'Processor'] = 'Processor info. unavailable'

filter_pro_day = df[(df['Processor'].str.contains(r'day|days', case=False)) & (df['Specification'].str.contains(r'day|days', case=False)) & (df['Warranty'].isnull())]
df.loc[filter_pro_day.index, 'Warranty'] = filter_pro_day['Processor']
df.loc[filter_pro_day.index, 'Processor'] = 'Processor info. unavailable'

filter_pro_serv = df[(df['Processor'].str.contains('service', case=False)) & (df['Warranty'].isnull())]
df.loc[filter_pro_serv.index, 'Warranty'] = filter_pro_serv['Processor']
df.loc[filter_pro_serv.index, 'Processor'] = 'NA Processor'

filter_pro_sams = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'SAMSUNG')]
df.loc[filter_pro_sams.index, 'Processor'] = filter_pro_sams['Processor'] + ' Octa Core Processor'

filter_war_sams = df[(df['Warranty'].str.contains('Octa Core Processor', case=False)) & (df['Brand'] == 'SAMSUNG')]
df.loc[filter_war_sams.index, 'Warranty'] = filter_war_sams['Warranty'].str.replace('Octa Core Processor','')

filter_apple_warr = df[(df['Warranty'].str.contains('Processor', case=False)) & (df['Brand'] == 'APPLE')]
split_warr_apple = filter_apple_warr['Warranty'].str.split(',', n=1, expand = True)
df.loc[filter_apple_warr.index, 'Processor'] = filter_apple_warr['Processor'] + split_warr_apple[0]

df.loc[filter_apple_warr.index, 'Warranty'] = filter_apple_warr['Warranty'].str.replace('6 Core Processor Processor', '')

filter_apple = df[(df['Warranty'].str.contains('Processor', case=False)) & (df['Brand'] == 'APPLE')]
filter_app = filter_apple['Warranty'].str.split(',', expand = True)
df.loc[filter_apple.index, 'Processor'] = filter_apple['Processor'] + filter_app[1]

filter_pro_realme = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'realme')]
df.loc[filter_pro_realme.index, 'Processor'] = 'Qualcomm Snapdragon 865 Processor'
df.loc[filter_pro_realme.index, 'Warranty'] = 'Brand Warranty of 1 Year Available for Mobile and 6 Months for Accessories'

filter_pro_redmi = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'REDMI')]
df.loc[filter_pro_redmi.index, 'Processor'] = 'Processor info. unavailable'
df.loc[filter_pro_redmi.index, 'Warranty'] = 'Brand Warranty of 1 Year Available for Mobile and 6 Months for Accessories'

filter_Ecotel = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'Ecotel')]
df.loc[filter_Ecotel.index, 'Processor'] = 'NA Processor'
df.loc[filter_Ecotel.index, 'Warranty'] = 'NA Warranty'

filter_Pear = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'Pear')]
df.loc[filter_Pear.index, 'Processor'] = 'NA Processor'
df.loc[filter_Pear.index, 'Warranty'] = 'NA Warranty'

filter_Eunity = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'Eunity')]
df.loc[filter_Eunity.index, 'Processor'] = 'NA Processor'
df.loc[filter_Eunity.index, 'Warranty'] = 'NA Warranty'

filter_itel = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'itel')]
filter_it = filter_itel['Specification'].str.split(',', n=4, expand=True)
df.loc[filter_itel.index, 'Battery'] = filter_it[3]
df.loc[filter_itel.index, 'Display'] = filter_it[1]
df.loc[filter_itel.index, 'Processor'] = 'Processor info. unavailable'

filter_pro_Easyfone = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'Easyfone')]
df.loc[filter_pro_Easyfone.index, 'Processor'] = 'NA Processor'

filter_pro_nullwar = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Warranty'].isnull())]
df.loc[filter_pro_nullwar.index, 'Warranty'] = filter_pro_nullwar['Processor']
df.loc[filter_pro_nullwar.index, 'Processor'] = 'Processor info. unavailable'

filter_war_micromax = df[(df['Warranty'].str.contains('Processor')) & (df['Brand'] == 'Micromax')]
df.loc[filter_war_micromax.index, 'Processor'] = 'ARM Cortex A75 Octa Core Processor Unisoc T610 Processor'

filter_war_ASUS = df[(df['Warranty'].str.contains('Processor')) & (df['Brand'] == 'ASUS')]
df.loc[filter_war_ASUS.index, 'Warranty'] ='1 Year Warranty for Handset and 6 Months for Accessories'

filter_war_Coolpad = df[(df['Warranty'].str.contains('Processor')) & (df['Brand'] == 'Coolpad')]
df.loc[filter_war_Coolpad.index, 'Processor'] = 'Quad Core SC9850K Processor'

filter_war_LG = df[(df['Warranty'].str.contains('Processor')) & (df['Brand'] == 'LG')]
df.loc[filter_war_LG.index, 'Processor'] = 'Qualcomm Snapdragon 821 2.35 Ghz Processor'

filter_pro_oneplus = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'OnePlus')]
df.loc[[4588,4655,4687,4688], 'Warranty'] = filter_pro_oneplus['Processor'] + filter_pro_oneplus['Warranty']
df.loc[[4588,4655,4687,4688], 'Processor'] = 'Processor info. unavailable'

filter_pro_avai = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['availability'] == 'Currently unavailable')]
df.loc[filter_pro_avai.index, 'Processor'] = 'Processor info. unavailable'

filter_iqoo = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'IQOO')]
df.loc[filter_iqoo.index, 'Warranty'] = '1 Year for handset	6 months for accessories'
df.loc[filter_iqoo.index, 'Processor'] = 'Processor info. unavailable'

filter_Tecno = df[(~df['Processor'].str.contains('Processor', case=False)) & (df['Brand'] == 'Tecno')]
df.loc[filter_Tecno.index, 'Warranty'] = 'Domestic Warranty of 1 Year Available for handset and 6 month for Accessories'
df.loc[filter_Tecno.index, 'Processor'] = '2GHz	Quad Core Processor Processor'

df[~df['Processor'].str.contains('Processor', case=False)]

df['Processor'].isnull().sum()

df['Brand_Warranty'] = np.where(df['Specification'].str.contains(r'Brand|Warranty|Manufacturer', case=False), 1, 0)
df['year_month_Warranty'] = np.where(df['Specification'].str.contains(r'Warranty|year|years|months|month', case=False), 1, 0)
df['accessories_Warranty'] = np.where(df['Specification'].str.contains('accessories',case=False),1 , 0)
df['rplc_rep_ser_Warranty'] = np.where(df['Specification'].str.contains(r'replacement|repair|service',case=False),1,0)

df.describe(include='all')

df.drop(['PhoneName', 'Specification', 'Num_Rating_review', 'Deals', 'comingsoon', 'C_ROM', 'RAM_ROM_Exp','Warranty'], axis=1, inplace=True)

df.columns

new_df = df[['Brand', 'PhoneModel', 'PhoneColor', 'NetworkType', 'ProductRating', 'DiscountPrice', 'OriginalPrice', 'Discount',
             'availability', 'Num_Ratings','Num_Reviews', 'Display', 'Camera', 'Battery', 'Processor',
             'RAM', 'ROM', 'Expandable', 'exchange_offer', 'bank_offer', 'saver_deal',
             'Brand_Warranty', 'year_month_Warranty', 'accessories_Warranty', 'rplc_rep_ser_Warranty']]

new_df.describe(include='all')

new_df.to_csv(r'/content/ml_project/Preprocessed_Mobile_Data.csv', index=False)
