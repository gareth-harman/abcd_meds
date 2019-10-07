# ABCD Medication Parsing

This tool provides logic and scripts for parsing classes of medications within the ABCD Dataset

### Steps:

1) One must have the ABCD Rds file which contains appropriate columns for medications prefixes listed below. **User must edit path to provide path to their own .Rds file** 

Medication Prefixes of column names
- medinv_plus_rxnorm_med  
- medinv_plus_otc_med  
- medinv_plus_otc_med  

2) Run the parse_meds.R script to output a .csv of all unique medications listed in the ABCD data release  

3) Run restful_get_rxnorm.py.  

`parse_meds.R`  
- Requires an .Rds file that contains relevant medication columns from the ABCD data release
- Outputs "medication_tagging.csv" a file containing all unique medication IDs that exist within this .Rds file

`restful_get_rxnorm.py`  
- Calls the rxNorm REST API to grab information from the NLM/NIH rxNorm database to obtain classes of medications
- Requires "medication_tagging.csv", generated from `parse_meds.R`

### Notes:  

- The logic for this medication parsing is consistent with that of an in development tool created by Hauke Bartsch
- Thanks to Hauke for his help in working with the rxNorm database
- For questions email me (Gareth) @ harmang (at) ohsu (dot) edu
- The structure of levels in the output 

### Structure

- The medication levels are organized as follows 

| Level        | Ex.           | Ex.  |
| ------------- |:-------------:| -----:|
| 1      | Broadest category | RESPIRATORY SYSTEM |
| 2      | ...      | DRUGS FOR OBSTRUCTIVE AIRWAY DISEASES |
| 3      | ...     | ADRENERGICS, INHALANTS |
| 4 | Finest category      | Selective beta-2-adrenoreceptor agonists |

