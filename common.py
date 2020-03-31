URL_CASES_TIME = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases2_v1/FeatureServer/4" \
                 "/query?where=1%3D1&outFields=Country_Region,Last_Update,Confirmed,Deaths&outSR=4326&f=json"

# For some reason, using the 'where 1=1' clause does not include us data, so we have to get that explicitly
URL_CASES_TIME_US = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases2_v1/FeatureServer" \
                    "/4/query?outFields=Country_Region,Last_Update,Confirmed,Deaths&where=UPPER(" \
                    "Country_Region)%20%3D%20'US'&f=json"

URL_CASES = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/Coronavirus_2019_nCoV_Cases" \
            "/FeatureServer/2/query?where=1%3D1&outFields=Country_Region,Last_Update,Confirmed," \
            "Deaths&outSR=4326&f=json"


class Cols:
    LastUpdate, Country, Confirmed, Deaths, Data, Feature = "Last_Update", "Country_Region", "Confirmed", "Deaths", "Data", "Feature"
