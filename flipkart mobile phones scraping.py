import requests
import bs4
import pandas as pd

url = 'https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_3_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_3_0_na_na_na&as-pos=3&as-type=HISTORY&suggestionId=mobiles&requestId=b7266836-d46d-41bb-bdc5-e196b56f66ce&p%5B%5D=facets.brand%255B%255D%3D{}&page={}'

brand = ['SAMSUNG', 'APPLE', 'realme', 'POCO', 'Infinix', 'OPPO', 'vivo', 'REDMI', 'Nothing', 'MOTOROLA',
         'Mi', 'LAVA', 'Nokia', 'KARBONN', 'I Kall', 'OnePlus', 'Kechaoda', 'itel', 'ASUS', 'Tecno', 'IQOO',
         'Snexian', 'MTR', 'Micromax', 'Honor', 'Lenovo', 'Cellecor', 'Panasonic', 'BlackZone', 'LG', 'IAIR',
         'ANGAGE', 'GIONEE', 'SAREGAMA', 'Tork', 'Intex', 'GFive', 'LYF', 'Lvix', 'SONY', 'HTC', 'XOLO', 'BlackBear',
         'SPICE', 'KXD', 'Alcatel', 'Videocon', 'Forme', 'Coolpad', 'iSmart', 'MAXX', 'Celkon', 'Grabo', 'GREENBERRI',
         'MAFE', 'Goof One', 'YU', 'TMB', 'Jmax', 'Easyfone', 'CAUL', 'Infocus', 'Eunity', 'Maplin', 'GIVA', 'Pear', 'iball',
         'Zen', 'Salora', 'Peace', 'Sony Ericsson', 'Huawei', 'Muphone', 'Google', 'Jivi', 'MBO', 'FELSONE', 'Ziox', 'MU', 'ringme',
         'hopi5', 'Zopo', 'Voto', 'Ssky', 'Nuvo', 'Vox', 'Telefono', 'MaQ by Flipkart', 'Lephone', 'DUOSS', 'BlackBerry', 'mobiistar',
         'iVoomi', 'UiSmart', 'Ui Phones', 'Meizu', 'Kenxinda', 'Ecotel', 'Trusme', 'Poya', 'PHILIPS', 'DIZO', 'TRYTO', 'Swipe', 'Nubia',
         'Beetel', 'anee', 'WIZPHONE', 'Rokea', 'Pluzz', 'ONIDA', 'MITASHI', 'Hexin', 'GREENBERRY', 'Fliky', 'XTOUCH', 'TRiO', 'Swiss Voice',
         'Smartron', 'Otho', 'MTS', 'M-tech', 'Lemon', 'Energizer', 'DETEL', 'Acer', 'sainatel', 'intaek', 'Zoom Me', 'Wings', 'VICTOR',
         'UR SMART', 'STK', 'Olive', 'Nexbit', 'MAXKING', 'Kechadda', 'KAWL', 'Idea', 'Hyve', 'Hicell', 'Elephone', 'EL', 'DAPS', 'Byond',
         'AirTyme', 'nuveck', 'kytes', 'amp', 'WhiteCherry', 'Virat FANBOX', 'Unihertz', 'Ulefonr', 'TCL', 'RYTE', 'Monix', 'MAYA', 'LeEco',
         'Kult', 'Krex', 'Jalsa', 'Heemax', 'HP', 'Geotel', 'Gamma', 'E&L', 'E L', 'Doogee', 'Do', 'DELL', 'Cospex', 'Comio', 'Chilli', 'Benco', 'AXXA']

all_phones = []
for i in brand:
  for j in range(1,44):
    print('brand',i, 'pageno', j)
    page = requests.get(url.format(i,j), headers={"Accept-Language": "en-US"})
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    ph_div = soup.findAll('div', class_='_2kHMtA')

    for ph in ph_div:
      phone = {}
      phone['Brand'] = i
      phone['PhoneName'] = ph.find('div', class_='_4rR01T').text if ph.find('div', class_='_4rR01T') else ''
      phone['Specification'] = [ph.text for ph in ph.find_all('li', class_='rgWa7D')] if ph.find('div', class_='_4rR01T') else ''
      phone['ProductRating'] = ph.find('span', class_='_1lRcqv').text if ph.find('span', class_='_1lRcqv') else ''
      phone['Num_Rating_review'] = ph.find('span', class_='_2_R_DZ').text if ph.find('span', class_='_2_R_DZ') else ''
      phone['DiscountPrice'] = ph.find('div', class_='_30jeq3 _1_WHN1').text if ph.find('div', class_='_30jeq3 _1_WHN1') else ''
      phone['OriginalPrice'] = ph.find('div', class_='_3I9_wc _27UcVY').text if ph.find('div', class_='_3I9_wc _27UcVY') else ''
      phone['Discount'] = ph.find('div', class_='_3Ay6Sb').text if ph.find('div', class_='_3Ay6Sb') else ''
      phone['Deals'] = [ph.text for ph in ph.find_all('div', class_='_2Tpdn3 _18hQoS')] if ph.find('div', class_='_4rR01T') else ''
      phone['availability'] = ph.find('span', class_='_192laR').text if ph.find('span', class_='_192laR') else 'Available'
      phone['comingsoon'] = ph.find('span', class_='u05wbu').text if ph.find('span', class_='u05wbu') else ''
      all_phones.append(phone)

df = pd.DataFrame(all_phones)
df.to_csv('/content/drive/MyDrive/DA DS/flipkart_mobile_1.csv')
