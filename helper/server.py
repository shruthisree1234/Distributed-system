from csv import unregister_dialect
from xmlrpc.server import SimpleXMLRPCServer
server = SimpleXMLRPCServer(("localhost", 9090))

import ftplib
from genericpath import exists
import os

FTP_Host_ID = 'localhost'
FTP_Port_ID = 21
User_name = 'VS1297'
password = '1297'
Local_File_Path = 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\client'
serverFilePath= 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\server'
remoteFolder = "/"

def getFtpFilenames(FTP_Host_ID, FTP_Port_ID, User_name, password, Remote_Directory):
    ftp = ftplib.FTP(timeout=30)
    ftp.connect(FTP_Host_ID, FTP_Port_ID)
    ftp.login(User_name, password)
    if not (Remote_Directory == None or Remote_Directory.strip() == ""):
        _ = ftp.cwd(Remote_Directory)
    fnames = []
    try:
        fnames = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            fnames = []
        else:
            raise
    ftp.quit()
    return fnames

def uploadFileToFtp(Local_File_Path,i, FTP_Host_ID, FTP_Port_ID, User_name, password, Remote_Directory):
    Local_File_Path=Local_File_Path+i
    isUploadSuccess: bool = False
    _, targetFilename = os.path_name.split(Local_File_Path)
    ftp = ftplib.FTP(timeout=30)
    ftp.connect(FTP_Host_ID, FTP_Port_ID)
    ftp.login(User_name, password)
    if not (Remote_Directory == None or Remote_Directory.strip() == ""):
        _ = ftp.cwd(Remote_Directory)
    with open(Local_File_Path, "rb") as file:
        retCode = ftp.storbinary(f"STOR {targetFilename}", file, blocksize=1024*1024)
    ftp.quit()
    if retCode.startswith('226'):
        isUploadSuccess = True
    return isUploadSuccess

def rename(old_file_name,new_file_name):
    ftp=ftplib.FTP(timeout=30)
    ftp.connect(FTP_Host_ID, FTP_Port_ID)
    ftp.login(User_name, password)
    ftp.cwd("/")
    ftp.rename(old_file_name,new_file_name)
    #ftp.mkd("test")
    ftp.quit()

def delete(name):
    ftp=ftplib.FTP(timeout=30)
    ftp.connect(FTP_Host_ID, FTP_Port_ID)
    ftp.login(User_name, password)
    ftp.cwd("/")
    ftp.delete(name)
    ftp.quit()

def file_sync():        
    # uploading
    fnames = getFtpFilenames(FTP_Host_ID, FTP_Port_ID, User_name, password, remoteFolder)
    print("files in server", fnames)
    path_name = 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\server'
    directory_list = os.listdir(path_name)
    print("Files in local server",directory_list)
    path_name = 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\client'
    directory_list = os.listdir(path_name)
    print("Files in client",directory_list)
    #uploading files (not in server)
    if(fnames!=directory_list):
        for i in directory_list:
            #print(i)
            isUploadSuccess = uploadFileToFtp(Local_File_Path,i, FTP_Host_ID, FTP_Port_ID, User_name, password, remoteFolder)
            print("upload status = {0}".format(isUploadSuccess)) 
   
    #deleting
    if(fnames!=directory_list):
        for i in fnames:
            if(i not in directory_list):
                delete(i)

def get_details():
    print("after sync")
    fnames = getFtpFilenames(FTP_Host_ID, FTP_Port_ID, User_name, password, remoteFolder)
    print("files in server", fnames)
    path_name = 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\client'
    directory_list = os.listdir(path_name)
    print("Files in client",directory_list)
    path_name = 'C:\\Users\\shruthi sree\\Downloads\\Project1_T_V\\HELPER\\server'
    directory_list = os.listdir(path_name)
    print("file in local server",directory_list)

# renaming
def rename_file():
    fnames = getFtpFilenames(FTP_Host_ID, FTP_Port_ID, User_name, password, remoteFolder)
    print("files in server", fnames)
    old_file_name=input("file name to change")
    new_file_name=input("enter new file name")
    rename(old_file_name,new_file_name) 

server.register_function(get_details, "get_details")
server.register_function(rename_file, "rename_file")
server.register_function(file_sync, "file_sync")
server.serve_forever()