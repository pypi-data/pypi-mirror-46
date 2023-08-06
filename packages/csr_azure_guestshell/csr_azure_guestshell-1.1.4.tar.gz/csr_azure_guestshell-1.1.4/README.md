# Scripts for guestshell on Cisco CSR1000V on AZURE

## Release History

Date	   Version	Description
11/17/17   1.0.0	Linux agent installation and reading metadata


## Introduction

This repository contains a library (csr_azure_guestshell) that contains 
a number of services and tools useful on the Azure cloud:
 - a Linux agent (waagent) used to download extensions and interact with the 
   Azure Security Center
 - a script to read and display the metadata for the virtual machine
 - example scripts to make script writing a bit easier for AZURE.

## Installation 

To enable guestshell on CSR on AZURE:
```
ios-prompt#  guestshell enable

Please wait for completion
ios-prompt# guestshell

```

To install csr_azure_guestshell:

```
[guestshell@guestshell ~]$ sudo pip install csr_azure_guestshell
```
Alternatively, you can install to your user directory:
```
[guestshell@guestshell ~]$ pip install --user csr_azure_guestshell
```

## Running scripts 

Scripts will be copied to the guestshell $PATH where they can then be run.  

List of scripts to be installed:
* [```get-metadata.py```](bin/get-metadata.py) -- retrieves instance metadata and prints to stdout


## Example output from running via IOS shell:

```
ip-172-31-52-111#guestshell run get-metadata.py
csr1kv3-csr#g run get-metadata.py
{
  "compute": {
    "sku": "", 
    "publisher": "", 
    "name": "my-vm-name", 
    "offer": "", 
    "vmSize": "Standard_D2_v2", 
    "vmId": "abcdefgh-abcd-1234-ab12-abcd1234abcd", 
    "platformUpdateDomain": "0", 
    "platformFaultDomain": "0", 
    "version": "", 
    "location": "eastus", 
    "osType": "Linux"
  }, 
  "network": {
    "interface": [
      {
        "mac": "0000ABCD1234", 
        "ipv4": {
          "subnet": [
            {
              "prefix": "24", 
              "dnsservers": [], 
              "address": "12.0.0.0"
            }
          ], 
          "ipaddress": [
            {
              "publicip": "13.0.0.1", 
              "ipaddress": "12.0.0.12"
            }
          ]
        }, 
        "ipv6": {
          "ipaddress": []
        }
      }, 

     ... <snip> ...

```

## Example output from running via guestshell prompt:

```
[guestshell@guestshell ~]$ get-metadata.py
{
  "compute": {
    "sku": "", 
    "publisher": "", 
    "name": "my-vm-name", 
    "offer": "", 
    "vmSize": "Standard_D2_v2", 
    "vmId": "abcdefgh-abcd-1234-ab12-abcd1234abcd", 
    "platformUpdateDomain": "0", 
    "platformFaultDomain": "0", 
    "version": "", 
    "location": "eastus", 
    "osType": "Linux"
  }, 
  "network": {
    "interface": [
      {
        "mac": "0000ABCD1234", 
        "ipv4": {
          "subnet": [
            {
              "prefix": "24", 
              "dnsservers": [], 
              "address": "12.0.0.0"
            }
          ], 
          "ipaddress": [
            {
              "publicip": "13.0.0.1", 
              "ipaddress": "12.0.0.12"
            }
          ]
        }, 
        "ipv6": {
          "ipaddress": []
        }
      }, 


     ... <snip> ...
```
