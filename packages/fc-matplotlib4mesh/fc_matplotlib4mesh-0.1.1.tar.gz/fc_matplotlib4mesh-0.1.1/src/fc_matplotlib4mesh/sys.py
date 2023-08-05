
def getDataPath():
  import os
  fullname=os.path.dirname(os.path.abspath(__file__))
  #fulldir=fullname[:fullname.rfind(os.sep)]
  return fullname+os.sep+'data'