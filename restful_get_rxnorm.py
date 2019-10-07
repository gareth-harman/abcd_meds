
import requests
from requests.auth import HTTPDigestAuth
import sys
import json
import pandas as pd



'''############################################################################
Grab json from rxNorm REST API
    - returns: parsed json
############################################################################'''

def get_json(url):
    
    # Get request
    myResponse = requests.get(url)
    
    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
    
        # Loading the response data into a dict variable
        js = json.loads(myResponse.content)
        return(js)
    
    else:
        myResponse.raise_for_status()
        return(0)
        
        
'''############################################################################
Grab the class from the medication ID
    - classType: optional specify source to grab meds
    - returns: list of all med class
############################################################################'''

def parse_rxNorm_json(js, classType = 'ATC1-4', parse_select = True, verbose = False):
    
    # Check that dict keys exist
    if 'rxclassDrugInfoList' not in js.keys():
        
        if verbose: print('Could not return meds')
        return 'cole', 'slaw'
    
    # Grab subindices of drug specific info
    js_sub = js['rxclassDrugInfoList']['rxclassDrugInfo']
    
    # Get all classNames for each hit
    med_find = [ii for ii in js_sub if ii['rxclassMinConceptItem']['classType'] == classType]
    
    # Return either raw or parsed scores
    if parse_select:
        
        # Return 0 if not med found, otherwise classId and className
        if len(med_find) == 0:
            return 'creamed', 'corn'
        
        else:
            ret_name = med_find[0]['rxclassMinConceptItem']['className']
            ret_classId = med_find[0]['rxclassMinConceptItem']['classId']
            
            return ret_name, ret_classId
        
    else:
        return(med_find[0])

'''############################################################################
Retroactively find class structure

############################################################################'''

def get_tree_class(class_id, verbose = False):
    
    # Check format of class_id
    if len(class_id) != 5:
        
        if verbose: print('Wrong classID format')
        return 'witch', 'pig'
    
    # Create class_ids for each tree level
    class_ids = [class_id,
                 class_id[:4],
                 class_id[:3],
                 class_id[:1]]
    
    class_tree = [] # Store each tree className
    
    # Iterate through and grab each class
    for ii in class_ids:
        
        # URL to grab class
        url = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byId.json?classId=" + ii
    
        js = get_json(url) # Get json
        
        # Check format and then add class structure
        if 'rxclassMinConceptList' in js.keys():
            class_out = js['rxclassMinConceptList']['rxclassMinConcept'][0]
            class_out = class_out['className']
            class_tree.append(class_out)
            
    return class_tree, class_ids


'''############################################################################
RUN SEQUENCE
############################################################################'''
    
if __name__ == "__main__":

    # Verbose (if true print summary of each med returned while parsing)
    verbose = True

    # Path to all meds
    med_path = 'medication_tagging.csv'
    
    # Load medications
    xl = pd.read_csv(med_path)
    
    # Base URL for rxNorm classes
    url_base = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.json?rxcui="
    
    '''
    Create dictionary of medication information
        Store id and full names of medicaitons
        lvl indicates drug class moving from less to more specfiic
        There is subsequent ID for each lvl 
    '''

    d = {'med_id': [],
         'med_full': [],
         'lvl_1_name': [],
         'lvl_2_name': [],
         'lvl_3_name': [],
         'lvl_4_name': [],
         'lvl_1_id': [],
         'lvl_2_id': [],
         'lvl_3_id': [],
         'lvl_4_id': []}
    
    # Iterate through each medication
    for ind, ii in enumerate(xl['med_id']):
        
        print('Parsing: {} / {} - {}'.format(ind, xl.shape[0], xl['med'][ind]))
        
        # Get json
        js = get_json(url_base + ii)
        
        # Parse json
        ret_name, ret_id = parse_rxNorm_json(js)
        
        # Check valid JSON was returned from request
        if ret_id == 'slaw':
            
            d['lvl_1_name'].append('NOT_MED')
            d['lvl_2_name'].append('-')
            d['lvl_3_name'].append('-')
            d['lvl_4_name'].append('-')
            d['lvl_1_id'].append('-')
            d['lvl_2_id'].append('-')
            d['lvl_3_id'].append('-')
            d['lvl_4_id'].append('-')
            
        else:
            # Get class structure
            class_tree, class_ids = get_tree_class(ret_id)
            
            # Validate class structure makes sense 
            if class_tree != 'witch':
                d['lvl_1_name'].append(class_tree[3])
                d['lvl_2_name'].append(class_tree[2])
                d['lvl_3_name'].append(class_tree[1])
                d['lvl_4_name'].append(class_tree[0])
                d['lvl_1_id'].append(class_ids[3])
                d['lvl_2_id'].append(class_ids[2])
                d['lvl_3_id'].append(class_ids[1])
                d['lvl_4_id'].append(class_ids[0])

                
            else:
                d['lvl_1_name'].append('NOT_MED')
                d['lvl_2_name'].append('-')
                d['lvl_3_name'].append('-')
                d['lvl_4_name'].append('-')     
                d['lvl_1_id'].append('-')
                d['lvl_2_id'].append('-')
                d['lvl_3_id'].append('-')
                d['lvl_4_id'].append('-')

        # Store full name and ID
        d['med_id'].append(ii)
        d['med_full'].append(xl['med'][ind])
        
        if verbose:
            print('ID: {} ClassID: {} Name: {}'.format(ii, ret_name, ret_id))

        break

    # Write structure to csv
    df = pd.DataFrame(d)
    df.to_csv()
    df.to_csv('abcd_med_class.csv', index = False)