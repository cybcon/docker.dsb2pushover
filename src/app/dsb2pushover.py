# -*- coding: utf-8 -*-
""" ***************************************************************************
dsb2push.py - is a small script that reads the DSB database, filters the
information and sends relevant information as a pushover message
seeAlso: https://github.com/nerrixDE/DSBApi
Author: Michael Oberdorf
Datum: 2021-04-21
*************************************************************************** """
import os
import sys
import datetime
import pandas as pd
import dsbapi
import logging
from packaging import version

VERSION='1.0.10'

dsbapi_min_version = '0.0.14'
if version.parse(dsbapi.__version__) < version.parse(dsbapi_min_version):
  print('ERROR: DSBApi library version ' + dsbapi.__version__ + ' found but require minimum version ' + dsbapi_min_version)
  sys.exit(1)


"""
###############################################################################
# F U N C T I O N S
###############################################################################
"""
def parse_dsb_data(dsb_entries, filter_class=None, filter_date=None):
    """
    parse the result from dsbclient.fetch_entries() and return a data frame
    @param dsb_entries: list(), result from dsbclient.fetch_entries()
    @param filter_class: string, an optional filter on class column (default: None)
    @param filter_date: string, an optional filter on date column (default: None)
    @return pandas.DataFrame()
    """
    # loop over the dsb result and create a data frame
    DF = list()
    for slice in dsb_entries:
        log.debug(slice)
        DF.append(pd.DataFrame.from_dict(slice, orient='columns'))
    df = pd.concat(DF,ignore_index=False, sort=False).reset_index(drop=True) #.replace('---',np.NaN)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None): log.debug(df)

    # set data types
    #df[['date', 'updated']] = df[['date', 'updated']].astype('datetime64[ns]')
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df['updated'] = pd.to_datetime(df['updated'], format='%d.%m.%Y %H:%M')
    df[['day', 'subject', 'new_subject', 'class']] = df[['day', 'subject', 'new_subject', 'class']].astype("category")

    # filter relevant school class
    if filter_class and 'class' in df.columns:
        log.debug('  filter for school class: ' + filter_class)
        #df = df[df['class'] == filter_class]
        df = df[df['class'].str.match(r'(' + str(filter_class) + ')')==True]
        df.drop(axis=1, columns=['class'], inplace=True)

    ## filter relevant date
    if filter_date and 'date' in df.columns:
        log.debug('  filter for date: ' + filter_date.strftime("%Y-%m-%d"))
        df = df[df['date'] == pd.Timestamp(filter_date)]
        df.drop(axis=1, columns=['date', 'day'], inplace=True)

    log.debug(df.columns)
    log.debug(df.info())
    with pd.option_context('display.max_rows', None, 'display.max_columns', None): log.debug(df.head())
    return(df)

def render_payload(df):
    """
    parse the pandas dataframe and render the payload for the pushover message
    @param df: pandas.DataFrame(), the data frame with the entries from DSB
    @return string, the rendered payload
    """
    data=[]

    for index, row in df.iterrows():
        #if DEBUG: print(row)
        entry = ''
        if 'class' in row:
            entry = 'Klasse ' + row['class'] + ', '
        entry += row['type'] + ' in Stunde ' + row['lesson'] + ', Fach ' + row['subject']
        if row['subject'] != row['new_subject']:
            entry += ' --> ' + row['new_subject']
        if row['room'] != '---':
            entry += ', in Raum ' + row['room']
        if row['new_teacher'] != '---':
            entry += ', Lehrer ' + row['new_teacher']
        if row['text'] != '---':
            entry += ', ' + row['text']
        log.debug(entry)
        data.append(entry)

    return("\n".join(data))

def send_pushover_message(userkey, apikey, title, message):
    """
    Send the given message via pushover services
    @param userkey: string,
    @param apikey: string,
    @param title: string,
    @param message: string,
    """
    import http.client, urllib
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
      "token": apikey,
      "user": userkey,
      "title": title,
      "message": message,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

"""
###############################################################################
# M A I N
###############################################################################
"""
log = logging.getLogger()
log_handler = logging.StreamHandler(sys.stdout)
if not 'LOGLEVEL' in os.environ:
    log.setLevel(logging.INFO)
    log_handler.setLevel(logging.INFO)
else:
  if os.environ['LOGLEVEL'].lower() == 'debug':
      log.setLevel(logging.DEBUG)
      log_handler.setLevel(logging.DEBUG)
  elif os.environ['LOGLEVEL'].lower() == 'info':
      log.setLevel(logging.INFO)
      log_handler.setLevel(logging.INFO)
  elif os.environ['LOGLEVEL'].lower() == 'warning':
      log.setLevel(logging.WARN)
      log_handler.setLevel(logging.WARN)
  elif os.environ['LOGLEVEL'].lower() == 'error':
      log.setLevel(logging.ERROR)
      log_handler.setLevel(logging.ERROR)
  else:
      log.setLevel(logging.INFO)
      log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

log.info('DSB to Pushover version ' + VERSION + ' started')

# Read environment variables
log.debug('Validate environment variables')
if not 'DSB_USERNAME' in os.environ:
    log.error('Environment variable DSB_USERNAME not defined')
    raise Exception('Environment variable DSB_USERNAME not defined')
if not 'DSB_PASSWORD' in os.environ:
    log.error('Environment variable DSB_PASSWORD not defined')
    raise Exception('Environment variable DSB_PASSWORD not defined')
if not 'PUSHOVER_USER_KEY' in os.environ:
    log.error('Environment variable PUSHOVER_USER_KEY not defined')
    raise Exception('Environment variable PUSHOVER_USER_KEY not defined')
if not 'PUSHOVER_API_KEY' in os.environ:
    log.error('Environment variable PUSHOVER_API_KEY not defined')
    raise Exception('Environment variable PUSHOVER_API_KEY not defined')
filter_date   = None
filter_date   = datetime.date.today() + datetime.timedelta(days=1)
filter_schoolclass = None
if not 'FILTER_SCHOOLCLASS' in os.environ:
    log.info('Environment variable FILTER_SCHOOLCLASS not defined')
else:
    filter_schoolclass = os.environ['FILTER_SCHOOLCLASS']
if not 'DSB_TABLE_FIELDS' in os.environ:
    tablemapper=['type','class','lesson','subject','room','new_subject','new_teacher','teacher']
else:
    tablemapper=os.environ['DSB_TABLE_FIELDS'].replace(" ", "").split(',')
log.debug('Use following DSBMonile table fileds: ' + ",".join(tablemapper))

# Get data from DSB
log.debug('Request data from DSB service')
dsbclient = dsbapi.DSBApi(os.environ['DSB_USERNAME'], os.environ['DSB_PASSWORD'], tablemapper=tablemapper)

entries = dsbclient.fetch_entries() # Rückgabe einer JSON Liste an Arrays

# Parse DSB data
log.debug('Parse received data')
df = parse_dsb_data(entries, filter_class=filter_schoolclass, filter_date=filter_date) # parse the data
if len(df.index) <= 0:
    log.info('Keine Einträge gefunden')
    log.info('DSB to Pushover version ' + VERSION + ' ended')
    sys.exit()
else:
    log.info(str(len(df.index)) + ' Einträge gefunden')

# extract the timestamp when the last update was made
updated = df['updated'].max()
df.drop(axis=1, columns=['updated'], inplace=True)

# render the subject of the pushover message
log.debug('Render pushover message')
SUBJECT  = 'Vertretungsplan '
if filter_schoolclass:
    SUBJECT += 'für die Klasse ' + filter_schoolclass + ' '
if filter_date:
    SUBJECT += 'für den ' + filter_date.strftime("%d.%m.%Y")
PAYLOAD  = 'Stand: ' + updated.strftime("%d.%m.%Y %H:%M") + "\n"
PAYLOAD += render_payload(df) # render the payload from DSB entries

log.debug('Send data to Pushover service:')
log.debug(SUBJECT)
log.debug(PAYLOAD)

send_pushover_message(userkey=os.environ['PUSHOVER_USER_KEY'], apikey=os.environ['PUSHOVER_API_KEY'], title=SUBJECT, message=PAYLOAD)

log.info('DSB to Pushover version ' + VERSION + ' ended')
sys.exit()
