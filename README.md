### **CAST Highlight - Automated Application Analysis Script**

####  **Purpose:**
The purpose of the script is to automate the analysis of multiple applications using CAST Highlight. It streamlines the process of analyzing source code files for various applications, allowing users to specify configurations, define source paths, and customize analysis parameters through a configuration file.

#### **Key objectives and functionalities of the script include:**
1.	**Automation**: The script automates the process of analyzing multiple applications by interfacing with the CAST Highlight via command-line execution. It eliminates the need for manual intervention in initiating and monitoring the analysis process for each application.
2.	**Batch Processing**: Applications are grouped into batches, and each batch is processed concurrently, leveraging multi-threading to improve efficiency. This enables faster analysis of a large number of applications, enhancing overall productivity.
3.	**Configurability**: Users can customize various parameters such as source paths, ignored directories/files, server URLs, authentication tokens, and batch sizes through the config.properties file. This allows flexibility in adapting the script to different environments and analysis requirements.
4.	**Error Handling**: The script incorporates error handling mechanisms to detect and handle issues during the analysis process. It logs detailed error messages, including return codes from the HighLight Analyzer tool, facilitating troubleshooting and debugging.
5.	**Output Generation**: Upon completion of analysis for each application, the script generates a summary CSV file containing the status, reasons for success or failure, and paths to log files. Additionally, detailed log files are created for each thread, providing comprehensive insights into the analysis execution.
Overall, the script aims to streamline and automate the process of application analysis, improving efficiency, accuracy, and ease of management for software development and quality assurance teams. By abstracting the complexities of manual analysis tasks and providing a configurable and scalable solution, it empowers users to perform thorough and consistent analysis across multiple applications with minimal effort.
 
#### **Prerequisites:**
1.	**Java Development Kit (JDK**): Ensure that JDK is installed and configured properly on the system.
2.	**Python**: Install Python programming language (version 3.x) on the system.
3.	**Perl**: Make sure Perl is installed and its path is properly set as specified in the configuration.
4.	**HighLight Analyzer**: Obtain the HighLight Analyzer tool and ensure its executable file is accessible.
5.	**Internet Connectivity**: Ensure the system has internet connectivity for accessing URLs specified in the configuration.
6.	**Configuration File**: Prepare a configuration file named config.properties with necessary parameters (details in the Configuration section).

#### **Installation:**
1.	**Clone Repository**: Clone the repository containing the script to the local system.
2.	**Setup Environment**: Set up the Python environment and install required libraries using pip install -r requirements.txt.
3.	**Configuration**: Configure the config.properties file with relevant paths and parameters (details in the Configuration section).
4.	**Prepare Input Data**: Prepare a file containing the list of applications to be analyzed, with each entry in the format ApplicationName;ApplicationID.

#### **Usage:**
1.	**Execute Script**: Run the script by executing python automated_analysis_script.py.
2.	**Monitor Progress**: Monitor the console for progress updates on application analysis.
3.	**Review Logs**: Check the log files generated in the specified log folder for detailed information about the analysis process.

#### **Configuration:**
Ensure the config.properties file is correctly configured with the following parameters:
•	**PERL**: Path to the Perl installation directory.
•	**ANALYZER_DIR**: Path to the directory containing the HighLight Analyzer tool.
•	**SOURCES**: Path to the directory containing the source files of the applications to be analyzed.
•	**IGNORED_DIR**: Directories to be ignored during analysis.
•	**IGNORED_PATHS**: Specific paths to be ignored during analysis.
•	**IGNORED_FILES**: File names to be ignored during analysis.
•	**URL**: URL for server communication.
•	**HIGHLIGHT_EXE**: Path to the HighLight Analyzer executable file.
•	**LOG_FOLDER**: Path to the folder where log files will be stored.
•	**COMPANY_ID**: Identifier for the company.
•	**TOKEN:** Authentication token for server communication.
•	**CONFIG**: Configuration folder path.
•	**RESULTS**: Path to the folder where analysis results will be stored.
•	**APPLICATIONS_FILE_PATH**: Path to the file containing the list of applications.
•	**BATCH_SIZE**: Number of applications to be processed concurrently (default is 1).
•	**OUTPUT_FOLDER**: Path to the folder where output files will be stored.
•	**MAX_BATCHES**: Maximum number of batches to process.

#### **Output:**
1.	**Summary CSV File**: A CSV file containing the summary of the analysis results.
2.	**Log Files**: Detailed log files are generated for each thread and stored in the specified log folder.
3.	**Console Output**: Progress updates and error messages are displayed in the console during script execution.

#### **Sample Usage:**
Copy code
python automated_analysis_script.py

#### **Troubleshooting:**
•	Ensure all paths specified in the configuration file are correct and accessible.
•	Check internet connectivity if accessing external URLs.
•	Review log files for detailed error messages and troubleshooting steps.

#### **Notes:**
•	This script supports multi-threading for efficient processing of application batches.
•	Ensure proper permissions are set for accessing directories and executing files specified in the configuration.
