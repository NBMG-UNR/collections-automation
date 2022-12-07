import pandas as pd
import json
import RSAPI

md_files = pd.read_excel('')
print(md_files.columns.values)


"""
System metadata
'utme_83' 
'utmn_83' 
'long_w84' 
'lat_w84' 
'entered_by'
'entered_date' 

Resource Metadata
'district' -> 111
'nggdpp' 
'file_id' -> 101
 'dist_no' -> 107
 'county' -> 110
 'title' -> 8
 'author' -> 86
 'pub_date' -> 106   -- note that this is a date range
 'cross_referenced_pdfs' -> parse these out for now
 'quad' -> 100
 'pmc' -> 103
 'commodity' -> 91
 'notes' -> 99
 'donated_by' -> 104
 'donated_dt' -> 105

 'url' 
 'copyright' -> 108
 'scanned_by' -> 
 'scanned_date' 
 'num_pages'
 'file_size_mb' 
 'physical_location' 
 'box_no_tube' 
 'microfilm' 
 'old_id'
"""
# initiate API instance
private_key = "621649872514174080fc8ebd66e618af2fa9baaab1c699d97c35acc32d65e051"
user = "api_user"

api = RSAPI.RSAPI(user, private_key)

# Separate out single and multi-district files
# Single district

single_d = md_files[md_files["cross_referenced_pdfs"].isnull()]

# Loop through files and insert them into system if not already in system
for file in single_d:
    response = api.query("do_search", "&search=id%%n%3B%21collection5&restypes=2") % file.id

    if not response:
        api.create_resource()

