import logging
import datetime
from requests import ReadTimeout
from web3.exceptions import BlockNotFound

'''
This is a wrapper to scan block by timestamp.
It uses bisection search to look for a block based on timestamp with cuttoffs of areas.
'''




