# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:02:56 2024

This is a test script to test the read-write the config file for the 
Bella Board. A dummy server is created to see to test this script. 

@author: Abin Jacob
         Carl von Ossietzky University Oldenburg
         abin.jacob@uni-oldenburg.de
"""

# libraries 
import paramiko 

# cofig remote file path
configfile = '/root/Bella/projects/your_project/config.txt'

# function to read the remote file
def readFile(sshClient, filepath):
    # open sftp connection
    sftpClient = sshClient.open_sftp()
    # read the file in read mode
    remotefile = sftpClient.file(filepath, 'r')
    filedata = remotefile.read()    
    # close the file & connection
    remotefile.close()
    sftpClient.close()
    # return the file data
    return filedata

# function to write to the remote file
def writeFile(sshClient, filepath, newfiledata):
    # open sftp connection
    sftpClient = sshClient.open_sftp()
    # read the file in write mode
    remotefile = sftpClient.file(filepath, 'w')
    # write data to update 
    remotefile.write(newfiledata)
    # close the file & connection
    remotefile.close()
    sftpClient.close()
    
# function to update config file 
def updateFile(filedata):
    # initialise empty list
    newdata = []
    # reading each line 
    for line in filedata.split('\n'):
        # checking if line starts with 'threshold'
        if line.startswith('threshold'):
            # adding new line wih the new content
            newdata.append('threshold 45')
        else:
            # appended the line without any change
            newdata.append(line)
    # returning the list seperated by newline
    return '\n'.join(newdata)

def main():
    hostname = 'FK6P-1008590'
    username = 'togo2120'
    password = 'egac73*onmn'
    
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.connect(hostname, username= username, password= password)
    
    try:
        filedata =  readFile(sshClient, configfile)
        newfiledata = updateFile(filedata)
        writeFile(sshClient, configfile, newfiledata)
        
    finally:
        sshClient.close()

if __name__=='__main__':
    main()

        
        
        
    

    










