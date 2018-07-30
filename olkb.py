#from json import loads
from time import time
import requests
import re
from pathlib import Path
from os import path
import webbrowser

# Time between checks in seconds.
# Eight hours for this module
CACHE_TIMEOUT=28800
ORDER_NO=<insert order number here>

class Py3status:

    """
    Module to report olkb.com order queue

    @author green-tealeaf
    """

    def kill( self, i3status_output_json, i3status_config ):
        pass

    def on_click( self, i3status_output_json, i3status_config, event ):

        # On a button 1, open Chromium (and wait for it to exit before proceeding).
        if event['button'] == 1:
            
            # Redirect output to /dev/null
            dn = open("/dev/null")
            webbrowser.open_new("https://olkb.com/orders")

            dn.close()
        
    def check_order_pos( self, i3status_output_json, i3status_config ):
    
        # Set the response dictionary
        response = {'name': 'olkb-notifier' }
        response_str_prefix = "olkb: "
        response_str = response_str_prefix + '-'
    
        # My userid
        userid = ORDER_NO 
 
        cache_file = path.join( str(Path.home()), '.i3/py3status/.olkb.cache' )

        # Cached position
        try:
            o = open( cache_file, 'r')
            order_pos = o.readline()
            o.close()
        except IOError:
            o = open( cache_file, 'w')
            o.write( "9999" )
            o.close()

        if( order_pos == "shipped" ):
            response_str = response_str_prefix + "shipped"

        # Read order position from https://olkb.com/orders
        try:
    
            # Get the html page
            url = 'https://raw.githubusercontent.com/olkb/orders/master/README.md'
    
            page = requests.get(url)

            # Process the response
            if page.status_code == 200:
    
                # Decode the html to ascii
                orders = page.text
    
                # Find the relevant entry
                order_pos_match = re.search( '([0-9]+)\. ' + ORDER_NO, orders )
                if( order_pos_match != None ):
                    order_pos_new = order_pos_match.group(1)
                else:
                    # If we have a stored order position, then don't match on
                    # retrieving the site, assume shipped.
                    if( int(order_pos) < 9999 ):
                        response_str = response_str_prefix + "shipped"
                    
                    order_pos_new = None

                # Write the count to the 'full_text' aspect of the response
                if( order_pos_new != None ):
            
                    # Compare the retrieved position to the cached one.
                    # If there is an increase, set the color to 'good'
                    # and write the new order_pos to the cache file.
                    if( int(order_pos) > int(order_pos_new) ):
                        response['color'] = i3status_config['color_degraded']
                        o = open( cache_file, 'w')
                        o.write( order_pos_new )
                        o.close()

                    response_str = response_str_prefix + order_pos_new
        
                    # Check only every CACHE_TIMEOUT seconds
                    response['cached_until'] = time() + CACHE_TIMEOUT

        except Exception as e:
       
            # If there's an error, return a null value, set an error colour, and set the cache timeout 2 seconds from now
            response['color'] = i3status_config['color_bad']
            response['full_text'] = response_str_prefix + '-'
            response['cached_until'] = time() + 2

        response['full_text'] = response_str
    
        return( response )

if __name__ == "__main__":
    """
    This allows the module to be run standalone for testing.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00'
    }
    while True:
        print(x.check_order_pos([], config))
        sleep(1)
