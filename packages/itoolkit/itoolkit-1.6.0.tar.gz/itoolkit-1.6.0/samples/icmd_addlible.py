# RTVJOBA can't issue from command line,
# but works with itoolkit
import config
from itoolkit import *
import sys

# modify iToolKit not include row node
itool = iToolKit()

itool.add(iCmd('addlible', 'ADDLIBLE LIB(KADLER)'))

# xmlservice
itool.call(config.itransport)

# output
print(itool.xml_in())
print('-----')
print(itool.xml_out())
sys.exit(1)

rtvjoba = itool.dict_out('rtvjoba')
print (rtvjoba)
if 'error' in rtvjoba:
  print (rtvjoba['error'])
  exit()
else:
  print('USRLIBL = ' + rtvjoba['USRLIBL'])
  print('SYSLIBL = ' + rtvjoba['SYSLIBL'])
  print('CCSID   = ' + rtvjoba['CCSID'])
  print('OUTQ    = ' + rtvjoba['OUTQ'])

