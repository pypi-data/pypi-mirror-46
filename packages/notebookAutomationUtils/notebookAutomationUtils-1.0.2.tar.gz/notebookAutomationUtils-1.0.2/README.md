# Jupyter Tools

Project contains automated sign off notebook generation tool. Follow the below steps to run the tool (ensure you have splunk csv data files to input data to the tool.)

# Steps for generating sign-off jupyter notebook

1. Open `````config.yaml````` and change config values (ensure you provide correct output path and data folder path as arguments).
2. `````cd````` into _jupyter-tools_ project folder and run  `````python generate_notebook.py`````
3. Look up for _Notebook.ipynb_ in given output path directory
4. Run _Notebook.ipynb_ inline or by opening the notebook:

    - To run inline via command prompt, `````cd````` into output path directory and run below command
    
    `````jupyter nbconvert --execute --inplace Notebook.ipynb`````

    - To open notebook and run, open _Notebook.ipynb_ and run each cell of the notebook

## Config information
`````config.yaml````` contains input values for generating notebook. Edit this file and provide appropriate values for each field.
- **output_path (string):** Location where the generated notebook should be stored
- **platform(str):** Name of the platform, value should be iOS or Android
- **device_name (string):** Name of the device used to generate the EPT data
- **device_version (string):** OS and OS version of the device used to generate the EPT data
- **from_date (string):** Splunk data generation start date
- **to_date (string):** Splunk data generation end date
- **current_release_link (string):** Hockey app link for current release
- **previous_release_link (string):** Hockey app link for previous release
- **current_release_server (string):** Current release number for server
- **previous_release_server (string):** Previous release number for server
- **data_folder_path (string):** Path of the folder which contains splunk csv data files
