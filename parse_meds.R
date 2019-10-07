##########################################################
# Gareth Harman
# 10/07/2019
# 
# Script to parse unqiue medications in an ABCD Rds file
# File must contain relevant medication columns
##########################################################


library(dplyr)
library(tidyr)


# Issues with masking from other libraries
select <- dplyr::select
filter <- dplyr::filter

# Path to Rds file containing med related columns
# USER MUST PROVIDE THE CORRECT PATH
df_dir = 'path_to/data.Rds'

df = readRDS(df_dir, stringsasfactors = FALSE)

# Find indices of all rows with known medication prefixes in name
var_inds = c(which(grepl('medinv_plus_rxnorm_med', names(df))),
             which(grepl('medinv_plus_otc_med', names(df))),
             which(grepl('devhx_9_med', names(df))))

# Create med_df of only med info
df_meds = df[, var_inds]

# Get all unique med entries
uniq_meds = as.character(unique(unlist(df_meds)))

# Remove NAs or empty strings
uniq_meds = uniq_meds[-c(which(is.na(uniq_meds)),
                         which(uniq_meds == ''))]


####################################################
# Function to split medication based on ID and name
####################################################

split_med <- function(x, out){
  val <- strsplit(x, ' ')
  
  if(out == 0){out_val <- val[[1]][[1]]}
  else {out_val <-c()
        for (ii in 2:length(val[[1]])){
          out_val[length(out_val)+1] <- val[[1]][[ii]]
        }
        out_val <- paste0(out_val, collapse = ' ')
  }
  
  return(out_val)

}

####################################################


# Get medication ID and name separately
med_id <- as.character(sapply(uniq_meds, split_med, 0))
med_nm <- as.character(sapply(uniq_meds, split_med, 1))

# Create a dataframe of all information
out_med <- data.frame(med = med,
                      med_id = med_id,
                      med_name = med_nm)

# Write this dataframe out
write.csv(out_med, 'medication_tagging.csv')


