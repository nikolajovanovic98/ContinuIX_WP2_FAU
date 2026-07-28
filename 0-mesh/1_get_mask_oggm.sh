# !/bin/bash 

# Activate your conda env in case it's not 
conda activate igm 

# Path to .json file
json_file="params.json" 

# RGI prompt and glacier name prompt 
read -p "Enter RGI: " rgi

# Glacier name 
read -p "Enter glacier name: " name 

# Update the json file
jq --arg oggm_RGI_ID "$rgi" '.oggm_RGI_ID = $oggm_RGI_ID' "$json_file" > tmp.json && mv tmp.json "$json_file"

# Get glacier outline and 
echo "JSON file updated successfully!" 

# Run igm and get outlines
echo "Running igm" 
igm_run 

# check if the directory already exists
if [[ -d "$name" ]]; then
    echo "Directory '$name' already exists."
else
    # make directory for the new glacier
    mkdir "$name"
    echo "Directory '$name' created."
fi

mv input_saved.nc $name/

# clean up 
. clean.sh
