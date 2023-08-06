# Insert your code here.
import numpy as np
def load_data(path=None):
  with open("address_features.csv", 'r') as f:
    lines = f.readlines()
    
    n = len(lines)
    m = len(lines[0].strip().split(','))-1
    
    x = np.empty([n,m], 'int')
    y = np.empty([n,1], 'int')
    
    for i in range(len(lines)):
      line = lines[i].strip().split(',')
      x[i] = line[:-1]
      y[i] = line[-1]
    
    return x,y
