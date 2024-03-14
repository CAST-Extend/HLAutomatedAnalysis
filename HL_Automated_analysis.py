import os
import validators
import subprocess
import threading
import logging
import csv
from datetime import datetime

# Mapping dictionary for return codes and their corresponding messages
return_code_messages = {
    0: "Error Code-0 : Ok",
    1: "Error Code-1 : Command Line general failure",
    2: "Error Code-2 : Command Line options parse error",
    3: "Error Code-3 : Command Line techno discovery error",
    4: "Error Code-4 : Command Line analysis error",
    5: "Error Code-5 : Command Line result upload error",
    6: "Error Code-6 : Command Line source dir or output dir validation error",
    7: "Error Code-7 : Command Line result saving to zip file error",
    8: "Error Code-8 : Command Line upload from zip file error",
    9: "Error Code-9 : Command Line unziping jars or zip error"
}

def read_properties_file(filename):
    properties = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                key, value = line.split('=', 1)
                properties[key.strip()] = value.strip()
    return properties

def validate_config(properties):
    required_params = ['PERL', 'ANALYZER_DIR', 'SOURCES', 'IGNORED_DIR', 'IGNORED_PATHS', 'IGNORED_FILES',
                       'URL', 'HIGHLIGHT_EXE', 'LOG_FOLDER', 'COMPANY_ID', 'TOKEN', 'CONFIG', 'RESULTS',
                       'APPLICATIONS_FILE_PATH', 'BATCH_SIZE', 'OUTPUT_FOLDER']
    for key, value in properties.items():
        if key =='PERL' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists!")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists!")
        
        if key =='ANALYZER_DIR' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists.")
        
        if key =='SOURCES' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists.")
        
        if key =='HIGHLIGHT_EXE' and not os.path.isfile(value):
            print(f"Program stopped bacause {key} File -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} File -> {value} does not exists.")
        
        if key =='LOG_FOLDER' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists.")
        
        if key =='CONFIG' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists.")
        
        if key =='RESULTS' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists.")
        
        if key =='APPLICATIONS_FILE_PATH' and not os.path.isfile(value):
            print((f"Program stopped bacause {key} File -> {value} does not exists."))
            raise ValueError(f"Program stopped bacause {key} File -> {value} does not exists.")
        
        if key =='OUTPUT_FOLDER' and not os.path.exists(value):
            print(f"Program stopped bacause {key} Folder -> {value} does not exists.")
            raise ValueError(f"Program stopped bacause {key} Folder -> {value} does not exists.")
        
        if key =='URL':
            if not value.endswith(".com") or not validators.url(value):
                print(f"Program stopped bacause The URL '{value}' is not valid.")
                raise ValueError(f"Program stopped bacause The URL '{value}' is not valid.")
        
    missing_params = [param for param in required_params if param not in properties]
    if missing_params:
        print(f"Program stopped bacause required parameters not in the config.properties: {', '.join(missing_params)}")
        raise ValueError(f"Program stopped bacause required parameters not in the config.properties: {', '.join(missing_params)}")

def check_duplicate_app_ids(applications):
    seen_ids = set()
    duplicates = []

    for item in applications:
        app_id = item[1]
        if app_id in seen_ids:
            duplicates.append(app_id)
        else:
            seen_ids.add(app_id)

    return duplicates

def create_fixed_batches(applications, num_batches):
    batch_size = len(applications) // num_batches
    remaining_apps = len(applications) % num_batches
    batches = []
    start = 0
    
    for i in range(num_batches):
        batch_end = start + batch_size + (1 if i < remaining_apps else 0)
        batches.append(applications[start:batch_end])
        start = batch_end
    
    return batches

def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

def calculate_execution_time(log_file_path):
    try:
        with open(log_file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            
            start_time = parse_timestamp(lines[0][:23])  # Extracting timestamp from the first line
            
            end_time = parse_timestamp(lines[-1][:23])  # Extracting timestamp from the last line
            
            execution_time = end_time - start_time
            
            return str(start_time)[:-4], str(end_time)[:-4], round((execution_time.total_seconds() / 60) ,2)  # Convert to minutes
    except Exception as e:
        print(f"Error reading log file {log_file_path}: {str(e)}")
        logging.error(f"Error reading log file {log_file_path}: {str(e)}")
        return None

def process_application(app_name, app_id, log_file, output_txt_file, output_csv_file):
    try:
        if os.path.exists(log_file):
            os.remove(log_file)

        source_path = os.path.join(SOURCES, f'{app_name}')
        def check_files(source_path):
            for file in os.listdir(source_path):
                return True
            return False

        if os.path.exists(source_path) and check_files(source_path):
            logging.info(f'Analysing Application: {app_name} ......')
            print(f'Analysing Application: {app_name} .....')
            completed_process = subprocess.run([
                'java', '-jar', HIGHLIGHT_EXE,
                '--workingDir=' + os.path.join(RESULTS, f'{app_name}'),
                '--sourceDir=' + source_path,
                '--analyzerDir=' + ANALYZER_DIR,
                '--perlInstallDir=' + PERL,
                '--serverUrl=' + URL,
                '--tokenAuth=' + TOKEN,
                '--applicationId=' + app_id,
                '--companyId=' + COMPANY_ID,
                '--ignoreDirectories=' + IGNORED_DIR,
                '--ignorePaths=' + IGNORED_PATHS,
                '--ignoreFiles=' + IGNORED_FILES
            ], check=True, capture_output=True, text=True)

            if completed_process.returncode == 0:
                status = "Passed"
                reason = "Application processed successfully"
                logging.info(f'Analysed Application: {app_name}.\n')
                print(f'Analysed Application: {app_name}.\n')
                start_time, end_time, execution_time = calculate_execution_time(log_file)
            else:
                status = "Failed"
                reason = return_code_messages.get(completed_process.returncode, f"Unknown return code: {completed_process.returncode}")
                logging.error(f'Analysis for the Application: {app_name} is failed with the reason -> {reason}.\n')
                print(f'Analysis for the Application: {app_name} is failed with the reason -> {reason}.\n')
                start_time, end_time, execution_time = calculate_execution_time(log_file)
            # logging.info(f'Return code: {completed_process.returncode}')
        else:
            status = "Failed"
            reason = "Source code not present"
            logging.error(f'Analysis for the Application: {app_name} is failed because source code not present.\n')
            print(f'Analysis for the Application: {app_name} is failed because source code not present.\n')
            start_time, end_time, execution_time = 'N/A', 'N/A', 'N/A'

    except subprocess.CalledProcessError as e:
        status = "Failed"
        reason = return_code_messages.get(e.returncode, f"Unknown return code: {e.returncode}")
        logging.error(f'Error processing application: {app_name} - {reason}.\n')
        print(f'Error processing application: {app_name} - {reason}.\n')
        # logging.error('Application processing failed.')
        start_time, end_time, execution_time = calculate_execution_time(log_file)

    # Write output data to CSV
    with open(output_csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([app_name, status, reason, log_file, start_time, end_time, execution_time])

    # Write output data to txt
    with open(output_txt_file, 'a', newline='') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerow([app_name, status, reason, log_file, start_time, end_time, execution_time])

def process_batch(batch, thread_id, output_txt_file, output_csv_file):
    thread_log_file = f"thread_{thread_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(filename=thread_log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f'Thread {thread_id} started.')
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f'Thread {thread_id} start time: {start_time}')
    logging.info(f'Thread {thread_id} processing applications: {batch}')

    for app_name, app_id in batch:
        #log_file = os.path.join(LOG_FOLDER, f'HLAutomation_{app_name}.log')
        log_file = os.path.join(RESULTS, f'{app_name}\HLAutomation.log')
        process_application(app_name, app_id, log_file, output_txt_file, output_csv_file)

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f'Thread {thread_id} end time: {end_time}')
    logging.info(f'Thread {thread_id} finished.')

# def txt_to_csv(input_file, output_file, delimiter='\t'):
#     with open(input_file, 'r') as txtfile:
#         # Read the lines from the text file
#         lines = txtfile.readlines()
        
#         # Open the CSV file for writing
#         with open(output_file, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile, delimiter=delimiter)
            
#             # Write each line as a row in the CSV file
#             for line in lines:
#                 writer.writerow(line.strip().split(delimiter))

if __name__ == "__main__":


    try:
        # Read properties from the config file
        properties = read_properties_file('config\config.properties')

        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Set up logging
        log_file = os.path.join("HLAutomationLOG", f"script_log_{datetime_now}.log")
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Validate config properties
        validate_config(properties)

        # Extract properties
        PERL = properties.get('PERL')
        ANALYZER_DIR = properties.get('ANALYZER_DIR')
        SOURCES = properties.get('SOURCES')
        IGNORED_DIR = properties.get('IGNORED_DIR')
        IGNORED_PATHS = properties.get('IGNORED_PATHS')
        IGNORED_FILES = properties.get('IGNORED_FILES')
        URL = properties.get('URL')
        HIGHLIGHT_EXE = properties.get('HIGHLIGHT_EXE')
        LOG_FOLDER = properties.get('LOG_FOLDER')
        COMPANY_ID = properties.get('COMPANY_ID')
        TOKEN = properties.get('TOKEN')
        CONFIG = properties.get('CONFIG')
        RESULTS = properties.get('RESULTS')
        APPLICATIONS_FILE_PATH = properties.get('APPLICATIONS_FILE_PATH')
        BATCH_SIZE = int(properties.get('BATCH_SIZE', 1))  # Default batch size is 1
        OUTPUT_FOLDER = properties.get('OUTPUT_FOLDER')
        MAX_BATCHES = properties.get('MAX_BATCHES')

        # Check if the APPLICATIONS_FILE_PATH is specified
        if APPLICATIONS_FILE_PATH is None:
            print("Program stopped Because 'APPLICATIONS_FILE_PATH' is not specified in config.properties")
            raise ValueError("Program stopped Because 'APPLICATIONS_FILE_PATH' is not specified in config.properties")

        # Check if the OUTPUT_FOLDER is specified
        if OUTPUT_FOLDER is None:
            logging.error("Program stopped Because 'OUTPUT_FOLDER' is not specified in config.properties")
            raise ValueError("Program stopped Because 'OUTPUT_FOLDER' is not specified in config.properties")

        logging.info('------------------------------------------------')
        logging.info(f'APPLICATIONS CONFIG PATH: {APPLICATIONS_FILE_PATH}')
        logging.info('------------------------------------------------')

        # Create the output csv file
        output_csv_file = os.path.join(OUTPUT_FOLDER, f'summary_{datetime_now}.csv')
        with open(output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Application Name', 'Status', 'Reason', 'Log File Path', 'Start Time', 'End Time', 'Total Time in Minutes'])

        # Create the output txt file
        output_txt_file = os.path.join(OUTPUT_FOLDER, f'summary_{datetime_now}.txt')
        with open(output_txt_file, 'w', newline='') as txtfile:
            writer = csv.writer(txtfile)
            writer.writerow(['Application Name', 'Status', 'Reason', 'Log File Path', 'Start Time', 'End Time', 'Total Time in Minutes'])

        # Read applications from the file
        with open(APPLICATIONS_FILE_PATH, 'r') as file:
            applications = [line.strip().split(';') for line in file]
            applications = applications[1:]
            # print(applications)

            duplicates = check_duplicate_app_ids(applications)
            if duplicates:
                logging.error(f'Duplicate Application IDs Found......')
                print(f'Duplicate Application IDs Found......')
                for app_id in duplicates:
                    logging.error(f'Duplicate Application ID - {app_id}')
                    print(f'Duplicate Application ID - {app_id}')
                print("Program stopped Because Duplicate Application IDs Found!")
                raise ValueError("Program stopped Because Duplicate Application IDs Found!")

        # Record start time
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'Start Time: {start_time}')

        num_threads = BATCH_SIZE
        num_batches = (len(applications) + num_threads - 1) // num_threads

        # Divide applications into batches
        if (MAX_BATCHES != None) and (MAX_BATCHES != '') and (num_batches > int(MAX_BATCHES)):
            num_batches = int(MAX_BATCHES)
            batches = create_fixed_batches(applications, num_batches)
            for i, batch in enumerate(batches):
                print(f"Batch {i+1}: {batch}\n")           
        else:
            num_threads = BATCH_SIZE
            num_batches = (len(applications) + num_threads - 1) // num_threads
            batches = [applications[i * num_threads:min((i + 1) * num_threads, len(applications))] for i in range(num_batches)]
            for i, batch in enumerate(batches):
                print(f"Batch {i+1}: {batch}\n") 

        # Process batches using multi-threading
        threads = []
        for i, batch in enumerate(batches, start=1):
            thread = threading.Thread(target=process_batch, args=(batch, i, output_txt_file, output_csv_file))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Record end time
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'End Time: {end_time}')

    except Exception as e:
        logging.error(f'{e}')
