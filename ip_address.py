#!/bin/env python
from parse_rest.connection import register
from parse_rest.datatypes import Object
import threading


class IP(Object):
	pass

def get_ip_address_5():
    #Use ip route list
    import subprocess
    arg='ip route list'    
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    sdata = data[0].split()
    ipaddr = sdata[ sdata.index('src')+1 ]
    netdev = sdata[ sdata.index('dev')+1 ]
    return (ipaddr,netdev)


def f():
    register("Dna2zMDf9AiehDaa3hJ50OeJMOkOiK4eqrIj2SS1", "V3bTQXDjNIipmilZlUkatdGiCIroV56RL4CTCBMI", master_key="rasXRUPEANifhLB7Evh68N5MKnUmnGu6dbtMF5dR")
    ip = IP(address=get_ip_address_5()[0])
    ip.save()
    # call f() again in 60 seconds
    threading.Timer(180, f).start()

# start calling f now and every 60 sec thereafter
f()
