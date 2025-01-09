import numpy as np
big_map={}
def to_num(x,mode=float):
  return [mode(i) for i in x]
def sfloat2int(x):
  return [int(float(i)) for i in x]

def map_data(fname):
  big_map={}
  with open(fname) as df:
    for i in df:
      data=i.split(',')
      sensors=sfloat2int(data[:3])
      coords=sfloat2int(data[3:])
      big_map[tuple(sensors)]=tuple(coords)
  return big_map

big_map=map_data('./7-9-21ba-t')

def list_sub(x,y):
  return np.array(x)-np.array(y)

def closest(x,mode='sum',return_min=False):
  diffs=[]
  big_map_list=list(big_map) 
  if mode=='sum':
    func=lambda x: sum(x)   
  else:
    func=lambda x: sum(x)/len(x)
  for i in big_map_list:
    diffs.append(func(abs(list_sub(x,list(i)))))
    
  minimum=min(diffs)
  print(minimum)
  idx=diffs.index(minimum)
  if return_min:
    return big_map[big_map_list[idx]],minimum
  else:
    return big_map[big_map_list[idx]]

def retrieve(x,func=lambda x: 0):
  try:
    return big_map[x]
  except KeyError:
    return func(x)

if __name__=='__main__':
    print(len(big_map),big_map)
    print(retrieve((2,3,5),closest)) #this is the predicted vaule base on the training data
