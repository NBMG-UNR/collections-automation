#generate publicly accessible URLs for objects in the GBSSRL collections system
#need to update keys and paths in main before running
#requires RSAPI.py and parameters.py

import json
import RSAPI
import pandas as pd

def update_public_links(overwrite, df, api):
    objects = []
    results = []
    values = []

    for index, row in df.iterrows():
        id = row['rsid']
        response = api.get_resource_metadata(id)
        objects.append(id)
        if len(response.text) == 0:
            print("incomplete: ")
            print(id)
            results.append("no response")
            values.append("null")
        else:
            data = json.loads(response.text)
            urlstr = "https%3A%2F%2Fcollections.nbmg.unr.edu%2F%3Fr%3D" + str(id)

            currentvalue = [item['value'] for item in data if item['name'] == 'publicurl'][0]

            if len(currentvalue) == 0 or overwrite is True:
                params = api.update_metadata_field(id, 125, urlstr)
                value = [item['value'] for item in data if item['name'] == 'publicurl']
                print(str(id))
                print("Updated value: " + str(value))
                values.append(value)
                results.append("updated")
            else:
                print("already contains value: " + str(currentvalue))
                values.append(currentvalue)
                results.append("not updated")

            response = api.get_resource_metadata(id)
            data = json.loads(response.text)

    results = pd.DataFrame(list(zip(objects, values, results)),
                           columns = ['IDs', 'Values', 'Results'])

    results.to_excel("output.xlsx", sheet_name='Sheet1')


def main():
    private_key = ""
    user = ""
    api = RSAPI.RSAPI(user, private_key)

    df = pd.read_excel('', sheet_name="Sheet1")

    update_public_links(False, df, api)