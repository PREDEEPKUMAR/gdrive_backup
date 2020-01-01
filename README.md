**_TERMINAL COMMANDS:_**

    pip freeze > requirements.txt --> Helps to create the Requirement File
    python -m venv <name>  --> creates the virtual environment in pycharm
    
_**NOTES:**_
    
    1. SUPPORTED FILE TYPES
    
    'xls', 'xlsx', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'ppt', 'pptx', 'zip', 'gz', 'rar',  'xlsm ', 'xltx', 'xltm', 'xlt'
    
    2. GDRIVE ENABLEMENT 
        Create two Folders on any directory
        1. ToDO 
            a. Set the Environament Variable --> Key: "GDrive_TODO", Value: "Full Folder of ToDO"
        2. Done --> Enable the GDrive for this Folder
            a. Set the Environament Variable --> Key: "GDrive", Value: "Full Folder of Done"
        The Program will execute only when you set these two variables on the environment.
    
    3. BACKUP FOLDER: 
        BACKUP_FOLDER = ['Desktop', 'Downloads', 'Documents', 'Pictures']
        Generally this process looks for the files on the C drive listed above
    
    4. CHECKS:
        Check for "HOMEDRIVE" and "HOMEPATH" is set correctly on the environmental variables
        Usually HomeDrive has to be C and Homepath has to be C:\Users\<Username>
        
    5. Default Execution Mode:
        Running From : PC
        Days for Backup : 5 days Back
        User Type: ADMIN
        
    6. Security Users:
        Availale on users.json File. 
           