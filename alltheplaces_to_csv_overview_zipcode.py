import os
from os.path import isfile, join
import json
import csv
import re

# Data structures for overview data
overview_data = {}
country_overview_data = {}
state_overview_data = {}


def print_countries_not_found(self):
    print("Countries not found:")
    for country in self.countries_not_found:
        print(country)

def update_overview_data(country, state, place_name, city, prop):
    # Update global overview
    key = (country.upper(), state.upper(), place_name.replace(' ', '').lower())
    overview_data[key] = overview_data.get(key, 0) + 1
    
    # Update country overview
    country_key = (state.upper(), place_name.replace(' ', '').lower(), city)
    if country.upper() not in country_overview_data:
        country_overview_data[country.upper()] = {}
    country_overview_data[country.upper()][country_key] = country_overview_data[country.upper()].get(country_key, 0) + 1
    
    # Update state overview
    state_key = (city, place_name.replace(' ', '').lower(), prop.get("addr:full", "").replace(',', ''))
    if country.upper() not in state_overview_data:
        state_overview_data[country.upper()] = {}
    if state.upper() not in state_overview_data[country.upper()]:
        state_overview_data[country.upper()][state.upper()] = {}
    state_overview_data[country.upper()][state.upper()][state_key] = prop

def write_country_state_overviews():
    for country, states in state_overview_data.items():
        country_path = f'location/2023/{country}'
        # Write country overview
        with open(join(country_path, f'{country}_overview.csv'), 'w', newline='', encoding='utf-8') as country_file:
            country_writer = csv.writer(country_file)
            country_writer.writerow(['State', 'Place Name', 'City', 'Establishments'])
            for (state, place_name, city), count in country_overview_data[country].items():
                country_writer.writerow([state, place_name, city, count])
        
        for state0, cities in states.items():
            
            state = sanitize_string(state0)
            state_path = join(country_path, state)
            os.makedirs(state_path, exist_ok=True)

            # Write state overview
            try:
                with open(join(state_path, f'{state}_overview.csv'), 'w', newline='', encoding='utf-8') as state_file:
                    state_writer = csv.writer(state_file)
                    state_writer.writerow(['City', 'Place Name', 'Zipcode', 'Name'])

                    for (city, place_name, address), prop in cities.items():
                        name = prop.get("name", "unknown")
                        zipcode = prop.get("addr:postcode", "unknown")
                        state_writer.writerow([city, place_name, address, zipcode, name])
            except Exception as e:
                print(e)
                pass

def write_overview_csv():
    for year in ['2023']:
        overview_csv_path = f'location/{year}/overview.csv'
        os.makedirs(os.path.dirname(overview_csv_path), exist_ok=True)
        with open(overview_csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Country', 'State', 'Place', 'Establishments'])
            for (country, state, place), count in overview_data.items():
                writer.writerow([country, state, place, count])

def sanitize_string(s):
    s = ''.join(s)
    s = s.replace(' ', '').replace('?', 'unknown').replace('|', '').replace('<', '').replace('>', '').replace('\t', '').replace('Ήπειρος','EPIRUS').replace('BAKIRKÖY','BAKIRKOY').replace('KADIKÖY','KADIKOY')

    # clean GA language
    s = s.replace('GÖLBAŞI', 'GOLBASI')\
     .replace('ALTIEYLÜL', 'ALTIEYLUL')\
     .replace('ÇAYIROVA', 'CAYIROVA')\
     .replace('DÖŞEMEALTI', 'DOSEMEALTI')\
     .replace('ᲐᲭᲐᲠᲐ', 'ADJARA')\
     .replace('ᲗᲑᲘᲚᲘᲡᲘ', 'TBILISI')\
     .replace('ᲥᲣᲗᲐᲘᲡᲘ', 'KUTAISI')\
     .replace('ᲒᲝᲠᲘ', 'GORI')\
     .replace('ᲡᲔᲜᲐᲙᲘ', 'SENAKI')\
     .replace('ᲥᲕᲔᲛᲝᲥᲐᲠᲗᲚᲘ', 'KVEMO KARTLI')\
     .replace('ᲚᲐᲜᲩᲮᲣᲗᲘ', 'LANCHKHUTI')\
     .replace('ᲡᲐᲛᲪᲮᲔᲯᲐᲕᲐᲮᲔᲗᲘ', 'SAMTSKHE-JAVAKHETI')\
     .replace('ᲘᲛᲔᲠᲔᲗᲘ', 'IMERETI')\
     .replace('ᲑᲐᲗᲣᲛᲘ', 'BATUMI')\
     .replace('ᲥᲝᲑᲣᲚᲔᲗᲘ', 'KOBULETI')\
     .replace('ᲗᲔᲚᲐᲕᲘ', 'TELAVI')\
     .replace('ᲐᲛᲑᲠᲝᲚᲐᲣᲠᲘ', 'AMBROLAURI')\
     .replace('ᲖᲣᲒᲓᲘᲓᲘ', 'ZUGDIDI')\
     .replace('ᲝᲖᲣᲠᲒᲔᲗᲘ', 'OZURGETI')\
     .replace('ᲤᲝᲗᲘ', 'POTI')\
     .replace('ᲙᲐᲭᲠᲔᲗᲘ', 'KACHRETI')\
     .replace('ᲛᲐᲠᲜᲔᲣᲚᲘ', 'MARNEULI')\
     .replace('ᲑᲝᲠᲯᲝᲛᲘ', 'BORJOMI')
    
    s = re.sub(r'[^\w\s]', '', s)
    return s  # Remove non-alphanumeric characters

def cn_state(s):
    if s.endswith("Sheng"):
        s = s[:-5]  # Remove 'Sheng' from the end
    if s.endswith("Province"):
        s = s[:-8]  # Remove 'Sheng' from the end
    if s.endswith("Shi"):
        s = s[:-3]  # Remove 'Sheng' from the end
    # Mapping of Chinese province names to their English equivalents
    province_translations = {
    "北京": "Beijing",
    "天津": "Tianjin",
    "上海": "Shanghai",
    "重庆": "Chongqing",
    "河北": "Hebei",
    "山西": "Shanxi",
    "辽宁": "Liaoning",
    "吉林": "Jilin",
    "黑龙江": "Heilongjiang",
    "江苏": "Jiangsu",
    "浙江": "Zhejiang",
    "安徽": "Anhui",
    "福建": "Fujian",
    "江西": "Jiangxi",
    "山东": "Shandong",
    "河南": "Henan",
    "湖北": "Hubei",
    "湖南": "Hunan",
    "广东": "Guangdong",
    "海南": "Hainan",
    "四川": "Sichuan",
    "贵州": "Guizhou",
    "云南": "Yunnan",
    "陕西": "Shaanxi",
    "甘肃": "Gansu",
    "青海": "Qinghai",
    "台湾": "Taiwan",
    "内蒙古": "Inner Mongolia",
    "广西": "GuangxiZhuangzuZizhiqu",
    "西藏": "Tibet",
    "宁夏": "Ningxia",
    "新疆": "Xinjiang",
    "香港": "Hong Kong",
    "澳门": "Macau"}

    # Convert input string to uppercase for case-insensitive match
    for chinese, english in province_translations.items():
        if chinese in s:
            return english
    return s  # This should be outside the loop

def replace_country_name_with_code(s):
    country_codes = {
        'ÍSLAND': 'IS',
        'DANMARK': 'DK',
        "CÔTE D'IVOIRE": 'CI', 
        'CONGO': 'CD',
        'BRASIL': 'BR',
        'MAROC': 'MA',
        'BÉNIN': 'BJ',
        'CZECH REPUBLIC': 'CZ',
        'SÉNÉGAL': 'SN',
        'DEUTSCHLAND': 'DE',
        'CAMEROUN': 'CM',
        'PRC': 'CN',
        'TUNISIE': 'TN',
        'CHINA': 'CN',
        'HONDURAS': 'HN',
        'SVERIGE': 'SE',
        'REPÚBLICA DOMINICANA': 'DO',
        'REPUBLIC OF SERBIA': 'RS',
        'PRINCIPAUTÉ DE MONACO': 'MC',
        'NICARAGUA': 'NI',
        'GABON': 'GA',
        'TOGO': 'TG'
    }
    # Convert input string to uppercase for case-insensitive match
    s_upper = s.upper()
    for country, code in country_codes.items():
        if country in s_upper:
            return code
    return s  # This should be outside the loop

def main():
    alltheplaces_dir = 'output_2023'
    files = [f for f in os.listdir(alltheplaces_dir) if isfile(join(alltheplaces_dir, f))]
    for file in files:
        full_file = join(alltheplaces_dir, file)
        if os.stat(full_file).st_size > 0:
            try:
                with open(full_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {full_file}: {e}")
                continue
                
            if data['type'] != 'FeatureCollection':
                print(f"{file} is not a FeatureCollection: {data['type']}")
                continue

            for feature in data['features']:
                prop = feature['properties']
                # get country information
                country = prop.get('addr:country', 'unknown')
                # if country contains the states
                country_original = country.split(", ")
                state = None
                if len(country_original) > 1:
                    country = country_original[1]
                    state = country_original[0]
                    state = sanitize_string(state)
                # clean all countries to two digit codes
                country = replace_country_name_with_code(country)
                if not state:
                    state = prop.get('addr:state', 'unknown')
                    state = sanitize_string(state)
                place_name = prop.get('@spider', 'unknown')
                city = prop.get('addr:city', 'unknown')

                # The existing logic to write detailed CSV files for each place remains unchanged...

                if country != 'unknown':
                    country_folder = os.path.join('location/2023', country.upper())
                else:
                    country_folder = 'location/2023/unknown'

                zipcode = str(prop.pop('addr:postcode', "unknown"))                    
                
                # Replace special characters in zipcode
                zipcode = re.sub(r'\s+', '', zipcode)  # Remove whitespace characters
                zipcode = re.sub(r'<br>', '', zipcode)  # Remove '<br>'
                zipcode = re.sub(r'\r\n', '', zipcode)  # Remove '\r\n'
                zipcode = re.sub(r'[^\w\s]', '', zipcode)  # Remove non-alphanumeric characters
                
                # Remove any empty or invalid zipcodes
                if zipcode == "NULL":
                    zipcode = "unknown"

                # Determine the directory and filename based on the modified structure for US only
                if country == 'US' and zipcode != "unknown":
                    zipcode_digits = ''.join(filter(str.isdigit, zipcode))[:5]
                    # Split the zipcode into individual folders
                    folders = [zipcode_digits[i:i+2] for i in range(0, len(zipcode_digits)-1, 2)]
                    csv_dir = os.path.join(country_folder, state, *folders)
                elif country == 'CN' and zipcode != "unknown":
                    state = cn_state(state)
                    zipcode_digits = ''.join(filter(str.isdigit, zipcode))
                    # Split the zipcode into individual folders
                    folders = [zipcode_digits[i:i+2] for i in range(0, len(zipcode_digits)-1, 2)]
                    csv_dir = os.path.join(country_folder, state, *folders)

                elif zipcode != "unknown":
                    zipcode_digits = ''.join(filter(str.isdigit, zipcode))
                    # Assuming non-US zipcodes use a different structure or are just placed under the state/country
                    folders = [zipcode_digits[i:i+2] for i in range(0, len(zipcode_digits)-1, 2)]
                    csv_dir = os.path.join(country_folder, state, *folders)
                else:
                    csv_dir = os.path.join(country_folder, state)

                
                update_overview_data(country, state, place_name, city, prop)


                csv_filename = f"{zipcode}.csv"
                csv_path = join(csv_dir, csv_filename)
                
                try:
                    os.makedirs(csv_dir, exist_ok=True)
                except OSError as e:
                    print(f"OS error with file {csv_dir}: {e}")

                csv_data = {
                    "Ref": prop.get("ref", ""),
                    "Spider": prop.get("@spider", ""),
                    "Name": prop.get("name", ""),
                    "Address": prop.get("addr:full", ""),
                    "City": prop.get("addr:city", ""),
                    "State": prop.get("addr:state", ""),
                    "Zipcode": prop.pop('addr:postcode', ""),
                    "Country": country,  # Add country column
                    "Phone": prop.get("phone", ""),
                    "Website": prop.get("website", ""),
                    "Hours": prop.get("opening_hours", ""),
                    "Brand": prop.get("brand", ""),
                    "WikiData": prop.get("brand:wikidata", "")
                }
                    
                with open(csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=csv_data.keys())
                    if not os.path.isfile(csv_path) or os.stat(csv_path).st_size == 0:
                        writer.writeheader()
                    writer.writerow(csv_data)
    
    # After processing all files:
    write_overview_csv()  # Global overview
    write_country_state_overviews()
 # Generate overview CSV after processing all files

if __name__ == "__main__":
    main()