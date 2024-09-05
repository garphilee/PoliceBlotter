import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
import time
import os


'''
1. Scrape incidents, titles, links from blotter site, create dataframe(? or just create csv from there?)
1.1 Check csv if incident has previously been recorded, skip if it has.
2. visit each incident, check location details (and even incident type)
3. map and visualize incidents
'''
#--------------------------

def initialGetIncidents():
    mainURL = 'https://pittsburghpa.gov/publicsafety/blotterview.html'

    r = s.get(mainURL, verify=False).text
    soup = BeautifulSoup(r,'html.parser')
    blotter = soup.find('div', {'id':'blotter'}).find('div',{'id':'blotlist'})
    incidents = blotter.find_all('a', {'id':'public-safety-blotter'})

    blotDict = { # incidentNumber : (link, title)        
    }

    for incident in incidents:
        blotTitle = incident.find('span').text.strip()
        blotNum = incident['href'].split('/')[-1].strip()
        blotLink = incident['href'].strip()
        blotDict[blotNum] = (blotLink, blotTitle)

    # Incident Report Template Details (Date, Incident Type, Zone, etc)
    # Date:\s+([A-Z][a-z]+ \d{1,2}, \d{4})
    # Incident\s+Type:\s+([A-Za-z\s]+)
    # Location:\s*(.*?)\s*Summary:



    df = pd.DataFrame.from_dict(blotDict,orient='index', columns = ['link','title'])

    print(df.loc['11']['link']) # test

    locationPatterns = [
        r'\b[A-Z][a-z]+\s+St\.?\s+at\s+[A-Z][a-z]+\s+Ave\.?\b',   # Intersection pattern
        r'\b\d{1,5}\s+block\s+of\s+[A-Z][a-z]+(?:\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Drive|Dr\.?|Lane|Ln\.?|Court|Ct\.?|Terrace|Ter\.?|Place|Pl\.?|of\s+the\s+[A-Z][a-z]+))?\b'
        # Block number pattern
        #'I-376 West',
        #'I-376 East',

        #r'\b(?:Zone\s+\d|East\s+Hills|Homewood|[A-Z][a-z]+\s+[A-Z][a-z]+)\b'  # Named areas or zones
    ]

    sampleReport = '''
    Pittsburgh Police from Zone 6 were dispatched just after 10:00 p.m. to the 600 block of Sherwood Avenue in Sheraden for three ShotSpotter alerts totaling seventeen rounds.

    Arriving officers located an adult male victim lying in the grass with gunshot wounds to his chest and leg.

    Pittsburgh EMS provided treatment to the victim on scene and transported him in grave condition to a local hospital. He was pronounced deceased at the hospital a short time later.

    The Mobile Crime Unit was called to process all evidence at the scene, including recovered shell casings and video footage.

    Violent Crime Unit detectives are investigating. The investigation is ongoing.

    '''

    for pattern in locationPatterns:
        match = re.search(pattern, sampleReport)
        if match:
            locations = match.group()
            break
        else:
            None    

    print(locations)
    csvOutput = os.path.join(os.path.dirname(__file__),'incidents.csv')
    print('csvOutput:', csvOutput)
    df.to_csv(csvOutput)



'''def getExisting(_dir, user):
    try:
        existingFiles = [file for file in os.listdir(f'{_dir}/{user}')]
    except:
        print(f'No existing files found for \'{user}\'.')
        existingFiles = []
    # ignore any extensions in title
    existingFiles = [file.split('.')[0] for file in existingFiles]
    return existingFiles'''

if __name__ == '__main__':
    s = requests.Session()
    dirPath = os.path.dirname(os.path.join(os.path.dirname(__file__),'PoliceBlotter.csv'))
    print(dirPath)
    initialGetIncidents()
    
    