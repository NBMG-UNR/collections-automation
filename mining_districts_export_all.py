# WARNING: this function hits the API for each object. Only run this if you really need to get a clean database export.
# Export ALL mining district file objects from the system
# This is a pretty clunky script due to some errors I've experienced in RS
# The script runs through twice - first to grab groups of objects and then go back and get any that had errors

import json
import RSAPI
import pandas as pd

private_key = ""
user = ""
export_path = ''
api = RSAPI.RSAPI(user, private_key)

# get all resources in a collection
# digital files: collection 64329
# copyrighted files: collection 64321
# multidistrict files: collection 64312
# ALL md files: collection 64716

#The first loop gathers all ResourceSpace IDs of the Mining District Files in groups of 100

#It is currently done in groups because there are some problematic resources that create errors - hence the second
# function

#note that the range to 320 will need to be changed as the collection grows, but everything else should be ok

offseterror = list()
data = list()
for x in range(0, 320):
    offset = x * 100
    params = "search=%21collection64716&fetchrows=50&offset={}".format(offset)
    response = api.query("do_search", params)

    if len(response.text) == 0:
        offseterror.append(offset)
    else:
        text = json.loads(response.text)
        data.extend(text)


#This function loops back through and pulls out the problematic objects from the first loop

data2 = list()
offseterror2 = list()
for x in offseterror:
    for i in range(0, 50):
        offset = x + i
        params = "search=%21collection64716&fetchrows=1&offset={}".format(offset)
        response = api.query("do_search", params)
        if len(response.text) == 0:
            offseterror2.append(offset)
        else:
            text = json.loads(response.text)
            data2.extend(text)


# Now we should have all our ids together
data3 = data + data2

# Extract the IDs from the above list, and then go back and get the actual metadata. This hits the API as many times
# as there are IDs in the ids list.
ids = [element['ref'] for element in data3]
incomplete = list()
allmds = list()
titles = list()
i = 0
for id in ids[0:]:
    response = api.get_resource_metadata(id)
    if len(response.text) == 0:
        incomplete.append(id)
    else:
        rsp = json.loads(response.text)
        if len(rsp) != 0:
            if i == 0:
                titles = [element['title'] for element in rsp]
                i = 1
            values = [element['value'] for element in rsp]
            values.append(id)
            allmds.append(values)
            if len(rsp[1]['value']) != 0:
                print(rsp[1]['value'])

titles.append('rsid')
df = pd.DataFrame(allmds, columns=titles)

df.to_excel(export_path)





