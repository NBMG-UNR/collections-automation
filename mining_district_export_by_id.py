## This script takes an excel file of ResourceSpace IDs, grabs the metadata for those objects, and then formats them
## into the enterprise geodatabse format.

## Need to edit before running: private_key, user,

import json
import RSAPI
import pandas as pd

#add the user and private key
private_key = ""
user = ""

#add the path in C:\\user\\filename format for the Excel sheet to import & path to export
export_path = ""
import_path = ""

api = RSAPI.RSAPI(user, private_key)

#change the list below
df = pd.read_excel('import_path',sheet_name="Sheet1")

#not the most elegant way of doing this: refactor later
i = 0
incomplete = list()
allmds = list()
titles = list()

for index, row in df.iterrows():
    id = row['rsid']
    response = api.get_resource_metadata(id)
    if len(response.text) == 0:
        incomplete.append(id)
    else:
        rsp = json.loads(response.text)
        if len(rsp) != 0:
            #the first time we go through the loop we get all of the metadata titles and store them in 'titles'
            values = [element['value'] for element in rsp]

            if values[0] != 'Mining District Files':
                continue

            values.append(id)
            allmds.append(values)
            if len(rsp[1]['value']) != 0:
                print(rsp[1]['value'])

            if i == 0:
                titles = [element['title'] for element in rsp]
                i = 1


titles.append('rsid')
df = pd.DataFrame(allmds, columns=titles)

# Export files in the SDE format to Excel
sde_format = df[['utme_83', 'utmn_83', 'long_w84', 'lat_w84', 'Mining District','NGGDPP Year', 'ID',
                 'Mining District ID', 'County', 'Title', 'Author', 'Date', 'Related PDFs', 'Quadrangle',
                 'PMC (Property, Mine, Claim)','Commodities','Notes','Donated by','Donated date',
                 'Entered by (legacy)','Entered date (legacy)','Public URL','Original filename','Copyrighted',
                 'Scanned by','Scanned Date','Physical Location','Legacy ID']].copy()

# Field mapping to sde format
sde_format.rename(columns={'utme_83': 'utme_83',
                    'utme_83': 'utme_83',
                    'utmn_83': 'utmn_83',
                    'long_w84': 'long_w84',
                    'lat_w84': 'lat_w84',
                    'Mining District': 'district',
                    'NGGDPP Year': 'nggdpp',
                    'ID': 'file_id',
                    'Mining District ID': 'district_id',
                    'County': 'county',
                    'Title': 'title',
                    'Author': 'author',
                    'Date': 'publication_date',
                    'Related PDFs': 'related_pdfs',
                    'Quadrangle': 'quadrangle',
                    'PMC (Property, Mine, Claim)': 'pmc',
                    'Commodities': 'commodities',
                    'Notes': 'notes',
                    'Donated by': 'donated_by',
                    'Donated date': 'donated_date',
                    'Entered by (legacy)': 'entered_by',
                    'Entered date (legacy)': 'entered_date',
                    'Public URL': 'url',
                    'Original filename': 'original_filename',
                    'Copyrighted': 'copyright',
                    'Scanned by': 'scanned_by',
                    'Scanned Date': 'scanned_date',
                    '': 'num_pages',
                    'Physical Location': 'physical_location',
                    'Legacy ID': 'legacy_id'}, inplace=True)

#change the path below
sde_format.to_excel(export_path)







