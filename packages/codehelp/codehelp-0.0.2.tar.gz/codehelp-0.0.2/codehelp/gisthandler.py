
"""
    Functions to retrieve Gists 

"""

import requests
import json


def get_gist(url):
    """ Get gist contents from gist url. 
        Note the gist url display the raw gist instead of usual gist page.
        Args:
            url (str) : url containing the raw gist instead of usual gist page.
        Returns:
            (str): output gist str.
            
    """
    r = requests.get(url)
    assert r.status_code==200, "Failed Page query code {}".format(r.status_code)
    
    return r.text

def get_config_fr_gist(url):
    
    """ Get config as dict from gist url (specific json file format) 
        Args:
            url (str) : url containing the json format string.
        Returns:
            (dict) : dict derived from json file.
            
    """
    json_str = get_gist(url)
    
    return json.loads(json_str)
    