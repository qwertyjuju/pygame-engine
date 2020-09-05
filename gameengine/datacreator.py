import os, inspect, pickle, sys
import pygame as pg


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
print(parentdir)

showdata = 0
createdata = 1


selectedmode = 0

dataloc = '\\data\\butterflies\\'

indatadict = {
    '_img': [
        'butterflie1',
        'butterflie2',
        'butterflie3',
        'butterflie4',
        'butterflie5',
        'butterflie6',
        'butterflie7',
        'butterflie8',
        'butterflie9',
        'butterflie10',
        'butterflie11',
        'butterflie12',
    ]
}



filename = 'butterflies.data'

outdatadict = {}

def main():
    pg.init()
    if showdata:
        pass
    else:
        createdata(indatadict)
        
        
def createdata(indatadict):
    for datakey, data in indatadict.items():
        try:
            functiondict[datakey]
        except KeyError:
            outdatadict[datakey] = data
        else:
            functiondict[datakey](data)
    savefile(filename)
    
def createsurface(data):
    imglist = []
    for img in data:
        print(parentdir+dataloc+img+'.jpg')
        surf = pg.image.load(parentdir+dataloc+img+'.jpg')
        size = surf.get_size()
        surfstr = pg.image.tostring(surf,'RGBA')
        imglist.append((surfstr, size))
    outdatadict['img'] = imglist

def savefile(filename):
    with open(filename,'xb') as file:
            pickle.dump(outdatadict, file)


functiondict = {
    '_img': createsurface
}

if __name__ =='__main__':
    main()