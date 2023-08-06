#!/usr/bin/env python
from os.path import expanduser
import os
import sys
import cli
import errno
import configparser
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.file import FileService

class cag():
    def __init__(self):
        self.azure_dir = os.path.expanduser('~') + '/.azure'
        self.private_credentials_file_path = self.azure_dir + '/credentials'
        self.load_env()
        self.create_blob_service()


    def create_blob_service(self):
        storage_name, storage_key = os.getenv('AZURE_PRIVATE_STORAGE_NAME',''), os.getenv('AZURE_PRIVATE_STORAGE_KEY', '')
        if len(storage_name) == 0 or len(storage_key) == 0 :
            storage_name, storage_key = os.getenv('AZURE_STORAGE_NAME', ''), os.getenv(
                'AZURE_STORAGE_KEY', '')
        if len(storage_name) > 0 or len(storage_key) > 0:
            self.block_blob_service = BlockBlobService(
                account_name=storage_name, account_key=storage_key)
        else:
            print("Warning: AZURE_STORAGE_NAME and AZURE_STORAGE_KEY env vars not present. \
                  Please export this vars and run script again for storage functionalities to work.")
            self.block_blob_service = None

    def get_credentials_file(self):
        if os.path.isfile("/bootflash/azure/decodedCustomData"):
            decodedFile = "/bootflash/azure/decodedCustomData"
        elif os.path.isfile("/bootflash/azure/decodedCustomData.txt"):
            decodedFile = "/bootflash/azure/decodedCustomData.txt"
        else:
            return False

        is_tvnet_csr = False
        with open(decodedFile) as f:
            for line in f:
                if 'section' in line and 'AzureTransitVnet' in line:
                    is_tvnet_csr = True

        if is_tvnet_csr == False:
            print("Section: AzureTransitVnet is not found in customdata. Returning.")
            return False

        with open(decodedFile) as f:
            for line in f:
                if 'privatestrgacctname' in line:
                    self.private_storage_acct_name = line.split()[1]
                if 'privatestrgacckey' in line:
                    self.private_storage_acct_key = line.split()[1]
                if 'strgacctname' in line:
                    self.storage_acct_name = line.split()[1]
                if 'strgacckey' in line:
                    self.storage_acct_key = line.split()[1]
                if 'transitvnetname' in line:
                    self.share_name = line.split()[1]
                if 'cloud' in line:
                    self.cloud = line.split()[1]


        self.mkdir_p(expanduser("~") + '/.azure/')
        self.get_file_to_path(self.share_name, 'AutoScaler', 'credentials', self.private_credentials_file_path)

    def mkdir_p(self, path):
        try:
            os.makedirs(path, exist_ok=True)  # Python>3.2
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

    def get_file_to_path(self, share_name, directory_name, file_name, file_path):
        '''
        Download a file to a local file path
        '''
        try:
            storage_name, storage_key = '', ''
            if self.private_storage_acct_name and self.private_storage_acct_key:
                storage_name, storage_key = self.private_storage_acct_name, self.private_storage_acct_key
            else:
                storage_name, storage_key = self.storage_acct_name, self.storage_acct_key

            if storage_key == "":
                print("Storage account key is not provided. Download file api may fail.")
            if storage_name == "":
                print("Storage account name is not provided. Download file api may fail.")

            storage_name, storage_key = storage_name.strip("'"), storage_key.strip("'")
            self.azure_file_service = FileService(account_name=storage_name, account_key=storage_key)
            self.azure_file_service.get_file_to_path(
                share_name,  # share name
                directory_name,  # directory path
                file_name,  # source file name
                file_path)
            return file_path
        except Exception as e:
            print ("Exception downloading file %s" % str(e))
            return None

    def load_env(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        home = expanduser("~")
        credential_file = home + '/.azure/credentials'
        config.read(credential_file)
        if not os.path.isfile(credential_file):
            print ("Warning: ~/.azure/credentials file not present.")
            print("Info: Try to get azure credentials file if storage info present in customdata.")
            if not self.get_credentials_file():
                print("Warning: Failed to retrieve credentials file.")
                return

        if os.path.isfile(credential_file):
            for key in config['default']:
                value = config.get('default', key).strip("'")
                os.environ[key] = str(value)


    def does_container_exist(self, containername):
        containers = self.block_blob_service.list_containers()

        for c in containers:
            if containername is c.name:
                return True

        return False

    def create_container_if_doesnt_exist(self, containername):
        if self.does_container_exist(containername) is False:
            self.block_blob_service.create_container(containername)

    def download_file(self, containername, filename, directory="/bootflash/"):
        try:
            self.block_blob_service.get_blob_to_path(
                containername, filename, directory + filename)
        except Exception as e:
            print "Config File Download Failed.  Error: %s" % (e)
            return False
        print "\nDownload Complete"
        return True

    def upload_file(self, containername, filename, directory="/bootflash/"):
        try:
            self.block_blob_service.create_blob_from_path(
                containername,
                filename,
                directory + filename,
                content_settings=ContentSettings(
                    content_encoding='UTF-8', content_language='en')
            )
        except Exception as e:
            print "Uploading %s Failed.  Error: %s" % (filename, e)
            sys.exit(1)

        print "Upload Complete to container %s" % (containername)

    def save_cmd_output(self, cmdlist, filename, container=None, directory="/bootflash/", print_output=False):

        with open(directory + filename, 'w') as f:
            for command in cmdlist:
                cmd_output = cli.execute(command)
                col_space = (80 - (len(command))) / 2
                if print_output is True:
                    print "\n%s %s %s" % ('=' * col_space, command, '=' * col_space)
                    print "%s \n%s" % (cmd_output, '=' * 80)

                f.write("\n%s %s %s\n" %
                        ('=' * col_space, command, '=' * col_space))
                f.write("%s \n%s\n" % (cmd_output, '=' * 80))
        if container is not None:
            self.upload_file(container, filename)
