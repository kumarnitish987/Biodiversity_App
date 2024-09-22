import requests
from PIL import Image
import piexif

def get_decimal_from_dms(dms, ref):
    # Convert DMS (Degrees, Minutes, Seconds) to decimal format
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0
    decimal = degrees + minutes + seconds
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_gps_info(image_path):
    try:
        img = Image.open(image_path)
        exif_data = piexif.load(img.info['exif'])
        
        # Check for GPS data
        gps_data = exif_data.get('GPS', {})
        if not gps_data:
            print("No GPS information found.")
            return None

        # Extract latitude and longitude
        gps_latitude = gps_data.get(piexif.GPSIFD.GPSLatitude)
        gps_latitude_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef).decode()
        gps_longitude = gps_data.get(piexif.GPSIFD.GPSLongitude)
        gps_longitude_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef).decode()

        if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
            lat = get_decimal_from_dms(gps_latitude, gps_latitude_ref)
            lon = get_decimal_from_dms(gps_longitude, gps_longitude_ref)
            return lat, lon
        else:
            print("Incomplete GPS information.")
            return None
        
    except KeyError:
        print("No EXIF data found.")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def get_current_environment_conditions(lat, lon):
  url = f'https://atlas.microsoft.com/weather/currentConditions/json?api-version=1.1&query={lat},{lon}&subscription-key=6wxJJ9n07L45hUeCEPzbdPbImO8ftJSW2N0DR8IwSnjuPHK7eQuWJQQJ99AIACYeBjFXlSElAAAgAZMPAcYg'

  # Make a request to the API
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
      data = response.json()
      temperature = data.get('results')[0]['temperature']['value']
      precipitation = data.get('results')[0]['precipitationSummary']['past24Hours']['value']
      return temperature, precipitation
  else:
      print(f"Error: {response.status_code}")
    
