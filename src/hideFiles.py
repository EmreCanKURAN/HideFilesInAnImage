"""
Emre Can KURAN - Hide Files In An Image v0.1
Last Update:18.03.2021
For any questions:
emrecankuran21@gmail.com
Disclaimer:
This script is created for a tutorial article that is written in terms of security and privacy.
Malicious intents are not encouraged and the author claims that he doesn't take any responsibilities.
"""

import os
from cryptography.fernet import Fernet
from zipfile import ZipFile

"""
Description:Checks if a given file meets determined conditions.
Parameters:entry(the entry object obtained from os.scandir function)
Returns:A boolean value that can be either true or false
"""

def checkConditions(entry):
    return (entry.is_file() and entry.name.endswith(".tiff"))

"""
Description:Returns list of files from selected directory. It is non-recursive and excludes subfolders currently.
Parameters:dirName(location of the directory to get files)
Returns:fileList(a list containing file names)
"""
def getFiles(dirName):
    fileList = []
    for entry in os.scandir(dirName):
#You can change the file type or you can make it recursive such that it includes all the files in the subfolders
        if checkConditions(entry):
            fileList.append(entry.name)
    return fileList

"""
Description:Generates a key file to encrypt and decrypt files
Parameters:keyName(name of the key file to save the key)
Returns:None
"""
def genKey(keyName):
    key = Fernet.generate_key()
    with open(keyName, "wb") as key_file:
        key_file.write(key)

"""
Description:Returns the key from the key file
Parameters:keyName(name of the key file the key has been saved to)
Returns:None
"""
def getKey(keyName):
    return open(keyName, "rb").read()

"""
Description:Encrypts the file
Parameters:fList(list of files to encrypt),keyName(name of key file)
Returns:encFileList(a list containing names of encrypted files)
"""
def encryptFile(fList, keyName):
    encFileList = []
    key = getKey(keyName)
    fernet = Fernet(key)
    for fileName in fList:
            with open(fileName, 'rb') as file: 
                original = file.read()
            encrypted = fernet.encrypt(original)
#Split the file name and add _enc to the end of it
            splittedFName = fileName.rsplit('.',1)
            splittedFName[0] = splittedFName[0] + "_enc"
            newFName = splittedFName[0] + "." + splittedFName[1]
            encFileList.append(newFName)
            with open(newFName, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
    return encFileList

"""
Description:Decrypts the file
Parameters:key(the key used to encrypt/decrypt),folderToDec(folder that contains files to get decrypted)
Returns:None
"""
def decryptFile(key, folderToDec):
    filesToDecrypt = getFiles(folderToDec)
    fernet = Fernet(key)
    for fileName in filesToDecrypt:
        with open(folderToDec + '/' + fileName, 'rb') as enc_file: 
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(folderToDec + '/' + fileName, 'wb') as dec_file:
            dec_file.write(decrypted)

"""
Description:Inserts encrypted files into a .zip file
Parameters:key(the key used to encrypt/decrypt),folderToDec(folder that contains files to get decrypted)
Returns:None
"""
def insertFile(encdFiles, outputName, imFileName):
    zipObj = ZipFile('encrypted.zip', 'w')
    for fileName in encdFiles:
#Append files to the zip
        zipObj.write(fileName)
#close the Zip File
    zipObj.close()
    os.system("copy /b " + imFileName + " + encrypted.zip " + outputName)
    for fileName in encdFiles:
        os.remove(fileName)
    os.remove('encrypted.zip')

"""
Description:Extracts the hidden files from image file
Parameters:folderToDec(folder to extract hidden files),outName(name of the steganographic image that contains hidden files)
Returns:None
"""
def extractFile(folderToExtract, outName):
    os.system("rename " + outName + " encrypted.zip")
#Extract all the contents of zip file in current directory
    path = folderToExtract
#If the folder that is created to extract files exists, show warning
    try:
        os.mkdir(path)
    except OSError as error:
        print("Folder already exists, process continues...")
    with ZipFile('encrypted.zip', 'r') as zipObj:
        zipObj.extractall(folderToExtract)
    os.remove('encrypted.zip')

#Test/drive functions

"""
Run this function if you are using first time
Parameters:keyName(name of the key file),outName(name of the steganographic image that contains hidden files),
imFileName(original image file to use)
Returns:None
"""
def firstTimeRun(keyName, outName, imFileName):
    genKey(keyName)
    encdFiles = encryptFile(getFiles("."), keyName)
    insertFile(encdFiles, outName, imFileName)

"""
Run this function if key file has been already created
Parameters:keyName(name of the key file),outName(name of the steganographic image that contains hidden files),
imFileName(original image file to use)
Returns:None
"""
def normalRun(keyName, outName, imFileName):
    encdFiles = encryptFile(getFiles("."), keyName)
    insertFile(encdFiles, outName, imFileName)

"""
Run this function to extract and decrypt the hidden files
Parameters:keyName(name of the key file),outName(name of the steganographic image that contains hidden files),
imFileName(original image file to use)
Returns:None
"""
def showFiles(folderToShow, outName, keyName):
    extractFile(folderToShow, outName)
    decryptFile(getKey(keyName), folderToShow)

'''
Main function & test
'''
def main():
#key file name
    keyName = 'secret.key'
#output image that contains hidden files
    outName = 'out.jpg'
#folder to extract hidden files
    folderToShow = 'show'
#image to hide in
    imFileName = 'mandrill.jpg'
#
    firstTimeRun(keyName, outName, imFileName)
#uncomment the line below and comment the line above to extract and decrypt files
    #showFiles(folderToShow, outName, keyName)
#uncomment the line below if you created the key already
    #normalRun(keyName, outName, imFileName)

'''
Redirect to main
'''
if __name__ == "__main__":
    main()
