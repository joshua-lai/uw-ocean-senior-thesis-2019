from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.close()

class Sample:
    def __init__(self,codeName,locationName,locationCoord,locationDepth,time,sampleNum,netNum,depth,volume,sampleVolume,dataDictionary,notes):
        self.codeName       = codeName
        self.locationName   = locationName
        self.locationCoord  = locationCoord
        self.locationDepth  = locationDepth
        self.time           = time
        self.sampleNum      = sampleNum
        self.netNum         = netNum
        self.depth          = depth
        self.volume         = volume #volume of water filtered m^3
        self.sampleVolume   = sampleVolume #percent of sample counted
        if dataDictionary   == None: #initial value
            self.data       = {'epacF':[],'epacM':[],'epacX':[],'trasF':[],'trasM':[],'tspinF':[],'tspinM':[]}
        else:
            self.data       =     dataDictionary
        self.notes          = notes
        self.allData        = []
        

    def filterData(self): #XXX
        
    
        # divides length to be millimeters
        for key in self.data:
            self.data[key] = list(map(lambda x: x/10,self.data[key]))
        
        # transformation, trying to get normal data, currently unsucessful
        # for key in self.data:
            #lambdaVal = 0.255415
            #self.data[key] = list(map(lambda x: (((x**lambdaVal) - 1) / lambdaVal),self.data[key]))
            #self.data[key] = list(map(lambda x: np.arcsin(x/100),self.data[key]))
        
        # sets epac <10 to be unidentified, and remove them from their original sex's group
        for sex in self.data:
            if sex in ['epacF','epacM']:
                self.data['epacX'] += list(filter(lambda x: x<10,self.data[sex]))
                self.data[sex] = list(filter(lambda x: x>=10,self.data[sex]))
        # self.allData is actually only e pac
        for classification in self.data:
            if classification in ['epacF','epacM','epacX']:
                self.allData += self.data[classification]
        
    def stackedHistData(self,nrows,ncols,ind,sharx, lineForTotal = True, meanAsLine = False, stacked = True, legend = False):
        
        epacF = self.data['epacF'],'E. pacifica females','firebrick'
        epacM = self.data['epacM'],'E. pacifica males','cornflowerblue'
        epacX = self.data['epacX'],'E. pacifica juveniles + unknown','darkorchid'
        trasF = self.data['trasF'],'T. raschii females','gold'
        trasM = self.data['trasM'],'T. raschii males','goldenrod'
        tspinF = self.data['tspinF'],'T. spinifera females','yellowgreen'
        tspinM = self.data['tspinM'],'T. spinifera males','olivedrab'
        
        
        
        data=[]
        labels=[]
        colors=[]
        means=[]
        medians=[]

        #LABELS

        try: #the graphs share the x axis, doesn't work the first one though
            ax = plt.subplot(nrows,ncols,ind,sharex=sharx)
        except:
            ax = plt.subplot(nrows,ncols,ind)
        # title
        if ind == 1:
            plt.title('Length distribution at '+self.locationName, fontsize = 30)
        # y label
        if ind == (2,3): 
            plt.ylabel("# of individuals",fontsize = 30)
        elif ind == 3:
            #plt.ylabel("              "+self.locationName+"\n                # of individuals",fontsize = "larger")
            plt.ylabel("                # of individuals",fontsize = 30)
        # x label
        if ind == 4: #if it's the lowest graph
            plt.xlabel('length (mm)',fontsize = 30)
        #else:
        #    plt.xticks=[0]
        
        #how many krill are in each sample, also by male+female
        totalCount = 0
        fCount = 0
        mCount = 0
        # for each classification in a sample
        #for classification in self.data:           # includes t rascii + others
        for classification in ["epacF","epacM","epacX"]:
            count = len(self.data[classification])
            # adds krill to a total overall or by sex
            totalCount += count
            if classification[-1] == 'F':
                fCount += count
            if classification[-1] == 'M':
                mCount += count
        # 
        #plt.text(0.01,0.55,str(self.depth), transform=ax.transAxes)
        
        plt.text(0.01,0.85,str(self.depth), transform=ax.transAxes, fontsize = "larger")
        plt.text(0.01,0.7,'~'+str(  round(((totalCount/self.sampleVolume)/self.volume),2))  +' $krill/m^3$', transform=ax.transAxes)
        
        plt.text(0.01,0.45,str(totalCount) + ' E. pacifica counted', transform=ax.transAxes)
        plt.text(0.01,0.3,str(fCount)+' females, '+str(mCount) + ' males', transform=ax.transAxes)
        
        
        
        
        #
        for catg in [epacF,epacM,epacX,trasF,trasM,tspinF,tspinM]:
            if len(catg[0]) > 0:
                data.append(catg[0])
                labels.append(catg[1])
                colors.append(catg[2])
                catgMean = np.mean(catg[0])
                catgMedian = np.median(catg[0])                
                means.append(catgMean)
                medians.append(catgMedian)
                #plt.ylabel('krill # in net '+str(self.netNum)+'\n between '+self.depth)  #old ylabel
                
               
                # lines for each category
                if not lineForTotal:
                    #for mean
                    if meanAsLine:
                        plt.plot([catgMean,catgMean],[0,10.75],color=catg[2],linestyle='dotted')
                    # for median instead
                    else: # meanAsLine == False
                        plt.plot([catgMedian,catgMedian],[0,10],color=catg[2],linestyle='dotted')
                    
                
                
                
                # overlapping histogram style
                if not stacked:
                    plt.hist(catg[0],bins=np.arange(3,21,0.5),label=catg[1],color=catg[2],alpha=0.75,)
                    plt.hist(catg[0],bins=np.arange(3,30,0.5),label=catg[1],color=catg[2],alpha=0.75,)
        
        
        # stacked histogram style
        if stacked:
            if self.locationName == "Kayak Point":
                plt.hist(data,bins=np.arange(3,30,.5),stacked=True,cumulative=False,label=(labels),color=(colors))
            else:
                plt.hist(data,bins=np.arange(3,21,.5),stacked=True,cumulative=False,label=(labels),color=(colors))                

        
        #legend on top most graph
        if legend:
            if ind == 1:
                plt.legend(loc='upper right')

        
        # mean of whole sample 
        if lineForTotal:
            if meanAsLine:
                print("mean")
                plt.plot([np.mean(self.allData),np.mean(self.allData)],[0,10.75],color='black',linestyle='solid',linewidth = 5.0)
            else: # median as line 
                plt.plot([np.median(self.allData),np.median(self.allData)],[0,10.75],color='black',linestyle='solid',linewidth = 5.0)
        return(data,labels,colors,means,medians,ax)

#FOR MAP
def getLatLon(objectList):
    """ takes in objects
    returns a list of tuples of the latitude and longitudes"""
    latLonList = []
    # for each dataset, gets the lat and lon
    for objectt in objectList:
        string = objectt.locationCoord
        lat = float(string[0:3])+float(string[4:11])/60
        lon = float(string[13:17])-float(string[18:25])/60
        # puts lat and lon into a tuple
        latLon  = lat,lon
        latLonList.append(latLon)
    return(latLonList)
#FOR MAP
def plotPoints(coordList, labelList, figsize=(20,10), figTitle = 'a graph', res = '10m', cmap = 'rainbow', region = 'PS'):
    """ takes in a list of coordinates as tuples 
    and optional parameters for figure size, resolution, coloration, title, and region
    plots a PlateCarree map with points colored 
    """
    plt.close
    plt.figure(figsize = figsize)
    # sets map projection and extent
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_title(figTitle)
    if region == 'PS':
        ax.set_extent([-123.5,-121.5,47,48.5])    
    else:
        ax.set_extent([-180,180,-90,90])
    # adds coastlines and land
    ax.coastlines(resolution = res)
    #land = cfeature.NaturalEarthFeature('physical','land', res, facecolor = 'lightGreen')
    #ax.add_feature(land)
    # translate colormap into a list of colors
    colors = eval('plt.cm.' + cmap + "(np.linspace(0,1,len(coordList)))")
    # plots points onto map with the corresponding colors
    for coord in enumerate(coordList):
        plt.scatter(coord[1][1],coord[1][0], color = colors[coord[0]], label = str(labelList[coord[0]]))
        plt.annotate(str(labelList[coord[0]]),(coord[1][1],coord[1][0]), size = 18)
    plt.legend()
    plt.show()
    
    



#stationdepth
# 48*6.4718N,122*28.150W to 48*5.9113N,122*27.040W
# T182919
mabA1 = Sample('mabA1', 'Mabana Point',' 48°06.2911N,-122°27.7559W',125,'2019,01,18,12:45',1,1,'82-77 m', 21,    1,None,None)
mabA2 = Sample('mabA2', 'Mabana Point',' 48°06.264 N,-122°27.705 W',125,'2019,01,18,12:46',1,2,'77-72 m', 29,    1,None,None)
mabA3 = Sample('mabA3', 'Mabana Point',' 48°06.230 N,-122°28.640 W',125,'2019,01,18,12:47',1,3,'72-67 m', 69,  1/4,None,'net paused at 70m or a while due to currents')
mabA4 = Sample('mabA4', 'Mabana Point',' 48°06.157 N,-122°28.468 W',125,'2019,01,18,12:51',1,4,'67-62 m', 24,    1,None,None)
mabA5 = Sample('mabA5', 'Mabana Point',' 48°06.132 N,-122°28.412 W',125,'2019,01,18,12:52',1,5,'62-00 m',187, None,None,None)

#48*6.685N,122*28.7706
# T215934
mabB1 = Sample('mabB1', 'Mabana Point',' 48°06.4322N,-122°28.0094W',120,'2019,01,18,14:08',2,1,'87-82 m',211,    1,None,None)
mabB2 = Sample('mabB2', 'Mabana Point',' 48°06.295 N,-122°27.746 W',120,'2019,01,18,14:13',2,2,'82-77 m', 29,  1/4,None,None)
mabB3 = Sample('mabB3', 'Mabana Point',' 48°06.259 N,-122°27.669 W',120,'2019,01,18,14:14',2,3,'77-72 m',124, 1/16,None,None)
mabB4 = Sample('mabB4', 'Mabana Point',' 48°06.254 N,-122°27.444 W',120,'2019,01,18,14:17',2,4,'72-67 m', 87,    1,None,None)
mabB5 = Sample('mabB5', 'Mabana Point',' 48°06.094 N,-122°27.340 W',120,'2019,01,18,14:19',2,5,'67-00 m',155, None,None,None)


#48*7.000N,122*22.876W to 48*6.039N,122*22.038W
# TS182613 ping 2480 - 2881
kp1   = Sample(  'kp1',  'Kayak Point',' 48°06.7000N,-122°22.876 W',120,'2019,01,19,11:02',1,1,'77-72 m',131,    1,None,'dropped to 97, held for a while at 95 before rising back')
kp2   = Sample(  'kp2',  'Kayak Point',' 48°06.695 N,-122°22.705 W',120,'2019,01,19,11:07',1,2,'72-67 m', 35,    1,None,None)
kp3   = Sample(  'kp3',  'Kayak Point',' 48°06.6285N,-122°22.7103W',120,'2019,01,19,11:08',1,3,'67-62 m', 96,    1,None,None)
kp4   = Sample(  'kp4',  'Kayak Point',' 48°06.4205N,-122°22.6332W',120,'2019,01,19,11:12',1,4,'62-57 m', 52,    1,None,None)
kp5   = Sample(  'kp5',  'Kayak Point',' 48°06.2815N,-122°22.5308W',120,'2019,01,19,11:14',1,5,'57-00 m',143, None,None,None)


# 12:33 net in, 47*59.694N,122*20.632W net may have missed the layer out 12:41, net out 12:55
# TS201822 ping 88 - 1734   
ged1  = Sample( 'ged1','Gedney Island',' 48°00.2834N,-122°20.6681W',162,'2019,01,19,12:41',1,1,'82-77 m',111,    1,None,'dropped to 87')
ged2  = Sample( 'ged2','Gedney Island',' 48°00.4402N,-122°20.6712W',162,'2019,01,19,12:44',1,2,'77-72 m', 21,    1,None,None)
ged3  = Sample( 'ged3','Gedney Island',' 48°00.5046N,-122°20.6747W',162,'2019,01,19,12:45',1,3,'72-67 m', 43,    1,None,None)
ged4  = Sample( 'ged4','Gedney Island',' 48°00.5812N,-122°20.6868W',162,'2019,01,19,12:46',1,4,'67-62 m', 41,    1,None,None)
ged5  = Sample( 'ged5','Gedney Island',' 48°00.6489N,-122°20.6894W',162,'2019,01,19,12:47',1,5,'62-00 m',208, None,None,None)


#12:14 net in, 47*41.4398N,122*45.4398W good layer, but net dropped midway to mix samples.
# T201126 ping 334 - 1776
hpA1  = Sample( 'hpA1',  'Hazel Point',' 47°41.4398N,-122°46.0194W', 90,'2019,01,20,12:30',1,1,'73-67 m', 85, 1/16,None,'originally intended a different range but dropped into 73')
hpA2  = Sample( 'hpA2',  'Hazel Point',' 47°42.1312N,-122°45.8913W', 90,'2019,01,20,12:33',1,2,'67-57 m', 44, 1/16,None,'forgot to open net')
hpA3  = Sample( 'hpA3',  'Hazel Point',' 47°42.3466N,-122°45.8600W', 90,'2019,01,20,12:34',1,3,'57-52 m', 61, 1/32,None,'forgot to open net')
hpA4  = Sample( 'hpA4',  'Hazel Point',' 47°42.7227N,-122°45.7966W', 90,'2019,01,20,12:36',1,4,'52-00 m',160, 9999,None,None)


#13:07 net in, 47*41.7615N,122*45.9470W to 47*42.6079N,122*45.8140W, net out 13:24
# T201126 ping 3686 - 4139
hpB1  = Sample( 'hpB1',  'Hazel Point',' 47°42.0032N,-122°45.9076W',162,'2019,01,19,13:14',2,1,'72-67 m', 80,3/128,None,None)
hpB2  = Sample( 'hpB2',  'Hazel Point',' 47°42.1432N,-122°45.8843W',162,'2019,01,19,13:16',2,2,'67-62 m', 69, 1/32,None,None)
hpB3  = Sample( 'hpB3',  'Hazel Point',' 47°42.2557N,-122°45.8704W',162,'2019,01,19,13:18',2,3,'62-57 m', 44, 1/16,None,None)
hpB4  = Sample( 'hpB4',  'Hazel Point',' 47°42.3274N,-122°45.8574W',162,'2019,01,19,13:19',2,4,'57-52 m', 40,  1/8,None,None)
hpB5  = Sample( 'hpB5',  'Hazel Point',' 47°42.3940N,-122°45.8467W',162,'2019,01,19,13:21',2,5,'52-00 m',148, None,None,None)


#data entry:
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabA1.data['epacF'] = [ #55,                                     # broken
                        94, 84, 78, 74, 77, 80,111, 84, 96, 81,
                       133, 86,135,155,128,111, 79,115, 88,137,
                        71, 73, 81,107,103, 86,126,114,102,183,
                       124,120,129]
mabA1.data['epacM'] = [104,133,132,113,125,129,120,132]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabA2.data['epacF'] = [ #75,                                     # broken
                       131, 96, 79, 71, 93,115, 52, 74, 70, 69,
                        97, 76,110, 73, 80, 72, 84,143, 82, 80,
                        58,140, 85,112, 73, 73, 62,120,122, 68,
                       121, 87, 79, 83, 78,110,109,144,143, 98,
                        60, 75, 77, 56, 73, 83, 74, 64, 75, 72,
                        72,103, 63, 87, 93, 72, 95, 88, 78, 74,
                       136, 94,137,157, 91,109, 71, 78, 71, 66,
                        61, 65, 59,126, 56, 73, 92,108, 76,106,
                        65, 67, 75, 97, 88,106, 75, 73, 81,104,
                        97, 80, 80, 64, 51, 71, 88, 79, 87,155]
mabA2.data['epacM'] = [118,137,123,148, 96,129,132,135,146,125,
                       128]
mabA2.data['epacX'] = [65]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabA3.data['epacF'] = [ 57, 87, 75, 68, 80, 93,124, 87, 88, 93,
                        82, 68, 81, 75, 79, 62, 78,106, 71, 74,
                        99,101, 70, 68, 80,146,105, 73, 73, 75,
                        76, 81, 82, 84, 81,103, 77, 78, 86, 93,
                        67,118, 81, 82,124, 83, 60, 90,110, 81,
                       107, 74,115, 93, 69,123, 79, 87, 79, 79,
                        78, 80, 80, 98, 74, 82, 73, 96,101, 79,
                        82, 86, 79, 59, 79, 87,103,120]
mabA3.data['epacM'] = [121,117,133,119,140,117,103,148,132,138,
                        96]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabA4.data['epacF'] = [ #90,                                     # broken
                        72, 82, 73, 79, 70, 79, 79, 74, 69, 78,
                        78, 96, 62, 82, 70, 82, 91,117]
mabA4.data['epacM'] = [120,158]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabB1.data['epacF'] = [105,110,89,109]
mabB1.data['epacM'] = [108,66,114,127]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabB2.data['epacF'] = [124,123, 96, 85, 91,147,133,133,110,109, #subsample 1/8
                        82, 89,121, 72, 87,142, 62,107,137, 92,
                       102, 81,
                        84, 96,131,177,133, 88,131, 93, 82, 59, #subsample 1/8
                       111, 73,163,144,114, 96, 83, 73,124,113,
                       108,103, 90,111,124,195,140,111,125, 79,
                       139, 83,142, 89,102]
mabB2.data['epacM'] = [137,168, 87,115,181,135,123,116,127,165,
                       130,130,
                       117,152,117,142,130,139,142,112,122,134,
                       118,151,144,119,138,129,113,128,126,123,
                       135]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabB3.data['epacF'] = [ 72,116,100, 83, 88, 62, 64, 83,103,102,
                        72, 63,137, 93, 94,102,103, 79,105,112,
                       119,112, 72, 78,114,157,112,114,105, 90,
                        85, 81,131,114,104, 92,113, 72, 72, 84,
                        98, 77, 91, 89, 94,106, 66, 84,169, 69,
                        83,108, 69,151,145]
mabB3.data['epacM'] = [117,127,142,119,124,142,133,109, 92,130,
                       119,123]
mabB3.data['epacX'] = [109]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mabB4.data['epacF'] = [ 83,106, 71, 65,122, 86, 78, 75, 70, 92,
                       111, 76, 81, 81, 60, 67, 75, 63, 61, 69,
                        70, 85,112, 65, 69, 66, 78, 83, 64,114,
                        93, 69, 73, 79, 89, 86, 70, 73, 60, 53,
                        83]
mabB4.data['epacX'] = [ 65, 72, 64, 68, 52]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
kp1.data['epacF']   = [162,167,109,160,120,116, 93,132,188,156,
                        86,113,124,161,148, 94]
kp1.data['epacM']   = [159,151,149,134,142,161,151]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
kp2.data['epacF']   = [125]
kp2.data['epacM']   = [152]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
kp3.data['epacF']   = [135,143,146,180,126]
kp3.data['epacM']   = [207,210,220,246]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
kp4.data['epacF']   = [122,130, 81,178,143,102]
kp4.data['tspinF']  = [277,216,219,227,232,212]
kp4.data['tspinM']  = [186]
kp4.data['trasF']   = [ 99]
kp4.data['trasM']   = [123]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ged1.data['epacF']  = [ 69,128,145, 80,112,127, 79, 66, 91, 96,
                       173,142,176,114,131,108,117,120,145, 77,
                        65, 75,149,132,142,107,114,141,142,163,
                       113, 77, 92, 65, 96,116,127,108,127,127,
                       141,158,156,187]
ged1.data['epacM']  = [161,152,120,156,133,122,129,130,155,160,
                       121,145,146,152,163]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ged2.data['epacF']  = [ 71,103, 81,106, 52, 65, 62, 80, 88,122,
                       114,130,169]
ged2.data['epacM']  = [114,163]
ged2.data['epacX']  = [ 66]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ged3.data['epacF']  = [ 61, 62,103, 84, 62, 87,116, 77, 74, 67,
                        69, 67, 74, 68, 82, 52, 54, 71, 66, 99,
                       110, 55, 93, 99,106,128,130,132,153]
ged3.data['epacM']  = [ 98,103,110,129,148]
ged3.data['epacX']  = [ 59]
ged3.data['trasF']  = [120]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ged4.data['epacF']  = [ #65, 70,                                 #broken
                       126, 64, 97,129, 77,139,111,163,101, 75,
                       101,114, 84, 91, 97, 86,109, 82, 87, 78,
                        62, 75, 80, 80, 72, 73, 72,104, 95,150,
                        88, 93, 75, 74, 80, 75, 91,109, 70, 66,
                        52, 84, 81, 80, 66]
ged4.data['epacM']  = [108,175,178,122,112,117, 97,126]
ged4.data['epacX']  = [ 74, 88, 67, 79, 69, 78, 65,124]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpA1.data['epacF']  = [154, 91,132,160, 81, 81,166, 76, 71, 96, #subsample 1/32
                       187,153,146, 93, 68,171, 86,161,155,159,
                        82,120,168,161,185,174,147,166,178, 58,
                       176,153,142,147,171, 67, 58,132,160,157, 
                        76, 30, 79, 82, 38, 95, 82, 73, 87, 68, #subsample 1/32
                       162, 90, 68, 63, 72, 88,111, 66,125,109,
                       141,132,155,162,176,159,171,176,195,165,
                       187,183,168,185,188]
hpA1.data['epacM']  = [164,118,150,162,166,149,155,162,157,142,
                       158,149,
                       165,124,145,152,140,162,170,156,155,179,
                       158,175,165]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpA2.data['epacF']  = [144, 69, 89, 72,106,136, 71, 69, 89, 80,
                        80, 85, 63, 68, 65, 79,101, 58, 58, 60,
                       100, 85, 78, 79, 70, 77, 92, 87, 79, 79,
                        70, 61, 89, 80, 87, 96,102, 75, 99,157,
                        66, 34,180, 90,104, 86, 86,160, 96,109,
                        84, 97,131,104, 57, 79,143,130,119,134,
                       148,146,126,134,155,162,161,152,174]
hpA2.data['epacM']  = [117,132, 97,148,142,108,117,142,149,143,
                       165,149,132,122,110,133,137,148,129,132,
                       146,150,136,150,147,145,158,142,162,166,
                       167]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpA3.data['epacF']  = [ 86, 77, 41, 46, 35, 64, 36, 74, 95, 43,
                        73,114, 36, 66, 75, 80, 70, 62, 84, 99,
                        86, 66, 64, 72, 37, 42, 75, 72, 69, 75,
                        49, 73, 82, 44, 82, 56, 82, 76, 92, 90,
                        70, 78,102, 59, 82, 82, 75,106, 91, 92,
                        86, 82, 75, 91, 84, 55, 93, 60, 65, 80,
                        60, 86, 90, 84, 77, 72, 90, 93, 91, 75,
                        84, 69, 79, 84, 94, 92, 95, 98, 87, 89,
                        95, 94,123,114,117, 96,135]
hpA3.data['epacM']  = [112,121,106,106,130,142,107,125,133,136]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpA4.data['epacX']  = [1] #fake, just so a thing graphs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpB1.data['epacF']  = [ 81, 77,149, 62,207,176,198,174,171,187,
                       194, 92, 87, 61, 94, 79,181,141,140, 67,
                       145,155,176,160,171,148,170,168,136,182,
                       142, 88,122,162,177,143, 76,162,179,168,
                       154, 98,167,160,179,132,168, 68, 61,124,
                       179,166,155]
hpB1.data['epacM']  = [147,131,125,128,122,123,153,177,
                       166,157]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpB2.data['epacF']  = [ 72,111,145,172,114,131,163,165,166,127,
                       128,144,154,162,158,151,118,156,158,142,
                        84, 89, 94,106,112,137, 89,110,179,148,
                       180,147,192,140,154,145,164, 98, 62,105,
                       151]
hpB2.data['epacM']  = [147,136,112,146,120,142,103,113,147,131,
                       141,137,157,165,161,162,145,153,125,160,
                       144,127,147,134,131,136,145,150,154,158,
                       115,121]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpB3.data['epacF']  = [ 51, 55, 62, 61, 73, 68,163,122, 76,135,
                       128, 89,122,107,133,183,112, 70,132,129,
                       146,119,116,143,100,138,162,156,118,142,
                        88,129, 83,200, 87, 72,151,153,172,128,
                       123,129, 98,140, 76,116,151,155,171]
hpB3.data['epacM']  = [ 79,143,156,148,125,127,148,142,123,114,
                       115,138,141,120,114,123,126,134,154,144,
                       131,103,116,132,140,132,123,126]
hpB3.data['epacX']  = [ 84, 60]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hpB4.data['epacF']  = [ 67, 90, 99, 73, 41, 88, 99, 58, 75,116,
                        58, 81,111, 80, 83, 56, 61, 65,101, 69,
                        84, 66, 50, 84, 76,132, 60, 70, 56, 45,
                        77, 60, 87, 93,155, 74, 62, 87, 78, 53,
                        84, 75, 37, 73,103, 64, 95, 74, 83,112,
                        66, 74, 69, 85, 89, 69,100, 77, 73, 72,
                       108, 44, 37, 76, 87, 79, 69, 65, 86, 82,
                        84, 94]
hpB4.data['epacM']  = [ 71,103, 98, 87,133,126,150,122,104,139,
                       110,125, 87,102,127, 95,157,134, 96,146]
hpB4.data['epacX']  = [ 94, 82,100, 69, 89, 79, 67]
hpB4.data['trasM']  = [109]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#XXX

labelList =  ['Hazel point','Gedney point','Kayak point','Mabana','Green Point']
coordList = getLatLon([hpA1,ged1,kp1,mabB1])
coordList.append((47.28,-122.712))



def stackedHistogram(name):
    #plt.close()
    #plt.tight_layout()
    plt.figure(figsize = (10.5,5.25))
    #plt.subplots_adjust(top=0.99,bottom=0.155,left=0.135,right=0.995,hspace=0.001,wspace=0.2)
    plt.subplots_adjust(top=0.935,bottom=0.09,left=0.055,right=0.99,hspace=0.0,wspace=0.0)
   

    for num in range(1,5):
        eval(name+str(num)).filterData()

    if name == "hpA":
        data,labels,colors,means,medians,ax = eval(name+'3').stackedHistData(4,1,1,'??')
        eval(name+'2').stackedHistData(4,1,(2,3),ax)
        eval(name+'1').stackedHistData(4,1,4,ax)
    else:
        data,labels,colors,means,medians,ax = eval(name+'4').stackedHistData(4,1,1,'??')
        eval(name+'3').stackedHistData(4,1,2,ax)
        eval(name+'2').stackedHistData(4,1,3,ax)
        eval(name+'1').stackedHistData(4,1,4,ax)    
    
    plt.show()


def printStats(objectList):        
    totCount=0
    ftotCount = 0
    mtotCount = 0
    fSep = []
    mSep = []
    aSep = []
    allAcross = []
    for obj in objectList:
        obj.filterData()                        # FILTER THE DATA (currently filters out non epac)
        for locationAllData in obj.allData:     # adds data to an list with every krill from allData
            allAcross.append(locationAllData)
        #fems = len(obj.data["epacF"]) + len(obj.data["trasF"]) + len(obj.data["tspinF"])
        #mals =  len(obj.data["epacM"]) + len(obj.data["trasM"]) + len(obj.data["tspinM"])
        fems = len(obj.data["epacF"])
        mals =  len(obj.data["epacM"])
        adults = fems + mals
        
        totCount += len(obj.allData)
        fSep.append(fems)
        mSep.append(mals)
        aSep.append(adults)
        ftotCount += fems        
        mtotCount += mals        

        # PRINT N = ~~~~~~~
        
        print("n = ", len(obj.allData))
        
        #~~~~~~~~ n = end        

        # SIZE ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        print(obj.codeName)
        sizeMean = round(np.mean(obj.allData),1)
        sizeMedian = round(np.median(obj.allData),1)
        sizeSTD = round(scipy.stats.sem(obj.allData),2)
        print("mean = ",sizeMean,", median = ",sizeMedian,", std = ",sizeSTD)
        
        #~~~~~~~~~~~~~~~~~~~~~~size end
        
        # SEX RATIO ~~~~~~~~~~~~~~~~~~~~~~~
        '''
        try:
            print("adults = ",adults)
            print("   fem = ", fems, "(",round(fems/adults,4),"% )")
            print("   mal = ", mals, "(",round(mals/adults,4), "% )")
        except:
            print("no adults")
        print()
        '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~ sex ratio end
        print()
        
    
    atotCount = ftotCount + mtotCount
    ftotPercent = ftotCount/atotCount
    mtotPercent = mtotCount/atotCount    
    
    # GENERAL SUMMARY~~~~~~~
    
    print("Summary of "+str(list(map(lambda x: x.codeName,objectList))) + ":")
    print("tot =  ", totCount, " adult tot = ",atotCount)
    print("ftot =   ", ftotCount, "%adults = ",round(ftotPercent,5))
    print("mtot =   ", mtotCount, "%adults = ",round(mtotPercent,5))
    print("males= ",mSep,"females=",fSep)
    print()
    
    # ~~~~~~~~~ Summary end
    

    # SEX BINOMIAL TEST ~~~~~~~~~~~~~~~~~~~~~
    '''
    for num in range(len(objectList)):
        p = scipy.stats.binom_test((fSep[num],mSep[num]),p=ftotPercent)
        print(objectList[num].codeName,"f",fSep[num],"m",mSep[num],"Binomial test P = ",p)
    '''
    #~~~~~~~~~~~~~~~~~~~~~~ binom test end
    
    # LOCATION SEX BINOMIAL TEST ~~~~~~~~~~~~~~~
    '''
    pp = scipy.stats.binom_test((ftotCount,mtotCount),p=0.60386)
    print("STATION BINOM:",pp)
    '''
    #~~~~~~~~~~~~~~~~~~~~~loc binom test end
    
    
    #SINGLE LARGE HISTOGRAM ~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    #plt.hist(allAcross,bins=np.arange(3,30,1),stacked=True,color=["k"])
    plt.hist(allAcross,bins=np.arange(0,5,0.1),stacked=True,color=["k"])
    plt.show()
    '''
    #~~~~~~~~~~~~~~~~~~~~~~~~ large histogram end

    # NORMALITY boxcox
    '''
    x = allAcross
    #x = scipy.stats.loggamma.rvs(5, size=500) + 5
    print(type(x),x)
    
    nm_value, nm_p = scipy.stats.normaltest(x)
    jb_value, jb_p = scipy.stats.jarque_bera(x)
    data_rows = [('D’Agostino-Pearson', nm_value, nm_p),
                 ('Jarque-Bera', jb_value, jb_p)]
    t = Table(rows=data_rows, names=('Test name', 'Statistic', 'p-value'), 
              meta={'name': 'normal test table'},
          dtype=('S25', 'f8', 'f8'))
    print(t)
    
    xt, maxlog, interval = scipy.stats.boxcox(x, alpha=0.05)
    print("lambda = {:g}".format(maxlog))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    prob = scipy.stats.boxcox_normplot(x, -5, 5, plot=ax)
    
    _, maxlog = stats.boxcox(x)
    ax.axvline(maxlog, color='r')

    plt.show()
    '''
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ normality end
    
    
    # KOLMOGOROV-SMIRNOV TEST ~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    for i,obj1 in enumerate(objectList):
        for obj2 in objectList[i+1:]:
            stat,p = scipy.stats.ks_2samp(obj1.allData,obj2.allData)
            stat = round(stat,2)
            p = round(p,8)
            print(obj1.codeName,obj2.codeName,'--  ks stat',stat,'p',p)
    print()
    '''
    #~~~~~~~~~~~~~~~~~~~~~ Kolmogorov–Smirnov test end
    
    # ANOVA TEST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    for i,obj1 in enumerate(objectList):
        for obj2 in objectList[i+1:]:
            stat,p = scipy.stats.kruskal(obj1.allData,obj2.allData)
            stat = round(stat,2)
            p = round(p,8)
            print(obj1.codeName,obj2.codeName,'--  h stat',stat,'p',p)
    print()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ anova test end
    
    
    
    
    # CHI SQUARED TEST~~~~~~~~~~~~~~~~~
    '''
    expectedM = list(map(lambda x: x* mtotCount/atotCount,aSep))
    print("Actual males = ", mSep,"   Expected males = ", expectedM)
    chisq,p = scipy.stats.chisquare(mSep,expectedM)
    print("chisq = ",chisq,"  p = ",p)
    print()
    expectedF = list(map(lambda x: x* ftotCount/atotCount,aSep))
    print("Actual females = ", fSep,"   Expected females = ", expectedF)
    chisq,p = scipy.stats.chisquare(mSep,expectedF)
    print("chisq = ",chisq,"  p = ",p)  
    print("\n\n")'''
    # ~~~~~~~~~~~~~~~~ chi squared test end
    
    






def main():
    # MAP
    #plotPoints(coordList, labelList, figTitle = "Puget Sound data locations")
    
    # no hpA4 in object list
    objectList = [kp1,kp2,kp3,kp4,ged1,ged2,ged3,ged4,mabA1,mabA2,mabA3,mabA4,mabB1,mabB2,mabB3,mabB4,hpA1,hpA2,hpA3,hpB1,hpB2,hpB3,hpB4]
    #printStats(objectList)
    
    # HISTOGRAM OPTIONS: hpA,hpB,kp,ged,mabA,mabB
    #stackedHistogram('kp')
    #stackedHistogram('ged')
    #stackedHistogram('hpA')
    #stackedHistogram('hpB')
    #stackedHistogram('mabA')
    #stackedHistogram('mabB')
    
    
    # STATISTICS
    printStats([kp1,kp2,kp3,kp4])
    #printStats([ged1,ged2,ged3,ged4])
    #printStats([hpA1,hpA2,hpA3])
    #printStats([hpB1,hpB2,hpB3,hpB4])
    #printStats([mabA1,mabA2,mabA3,mabA4])
    #printStats([mabB1,mabB2,mabB3,mabB4])
    
    
if __name__ == "__main__":
    main()    
