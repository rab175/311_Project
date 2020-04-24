import pandas as pd
import requests
import json

#get list of all zipcodes in NYC separated by commas
nyc_zips = pd.read_csv('data/nyc_zips.csv')
nyc_zips = list(nyc_zip_df.nyc_zips.values)
nyc_zips = ','.join(nyc_zips)

#census API key
apiKey = "48784222002d7edac2b67d73b9fba16530797dcd"

#construct the API call we will use
baseAPI = "https://api.census.gov/data/2017/acs/acs5?key=%s&get=B01003_001E&for=zip%%20code%%20tabulation%%20area:%s"
calledAPI = baseAPI % (apiKey, nyc_zips)

#call the API and collect the response
response = requests.get(calledAPI)

#load the response into a JSON, ignoring the first element which is just field labels
formattedResponse = json.loads(response.text)[1:]

#flip the order of the response from [population, zipcode] -> [zipcode, population]
formattedResponse = [item[::-1] for item in formattedResponse]

#store the response in a dataframe
nyc_zip_populations = pd.DataFrame(columns=['zipcode', 'population'], data=formattedResponse)

#save that dataframe to a CSV spreadsheet
nyc_zip_populations.to_csv('nyc_zip_populations.csv', index=False)
