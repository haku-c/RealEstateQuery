# RealEstateQuery

## About
This is a script to scrape an address's Zillow page for the requisite information. Only meant for small number of requests at a time and not for commercial use. 


## Demo
View a demo [here](https://youtu.be/pCP9KmcB-hs)

## Table of Contents
* [Install](#Install)
* [Features](#Features)
* [Usage](#Usage)

## Install
1. Clone the repo
   ``` Powershell
    git clone git@github.com:haku-c/RealEstateQuery.git

2. pip install dependencies
    ``` Python 
    pip install -r requirements.txt

## Features
  Scrapes Zillow for the given address and returns information about the property and its local schools. 

## Usage
1.  From the command line run
    ``` Python
    python main.py
2. Follow the prompts to input an address
    * Input the address (house and street number) 
    * Input the city
    * Input the state (postal abbreviation, for example input CA for California)

## Troubleshooting/Known Issues
* Zillow sometimes blocks the get request with a 403.
* Certain fields are empty if the Zillow page does not have that data. 
* For apartments, include the room number. 

