from __future__ import division
import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d

def lazy_property(fn):
    '''Decorator that makes a property lazy-evaluated.
    '''
    attr_name = '_lazy_' + fn.__name__



    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


class HydroTs(object):
    def __init__(self, TimeSeries):
        self.TimeSeries= TimeSeries


    def EventFreq(self, Comparer):
        EventCount = {}
        EventLength = {}
        currentyear = self.TimeSeries.index[0].year
        NumberOfEvents = 0;
        CurrentEventLengt = []
        InEvent = False

        for k,v in self.TimeSeries.items():
            #We got a new year. Store data
            if (k.year != currentyear):
                EventCount[currentyear]= NumberOfEvents
                EventLength[currentyear]= CurrentEventLengt
                currentyear = k.year;
                NumberOfEvents = 0;
                CurrentEventLengt = [];
                CurrentEventLengt.append(0);
    
            if (Comparer(v)):
            #This is a new event
                if not InEvent:
                    NumberOfEvents+=1
                    InEvent = True
                    CurrentEventLengt.append(0)
            #Increase number of days in event
                CurrentEventLengt[len(CurrentEventLengt) - 1]+=1
            else:
                InEvent = False
    
        if not currentyear in EventCount:
            EventCount[currentyear] = NumberOfEvents
            EventLength[currentyear] = CurrentEventLengt
        #First average the length on years, then average the averages
        #Average length on years:
        ayear=np.mean([v for k,v in EventCount.items()])
        lengthMoreThenZero=[v for k,v in EventLength.items() if len(v)>0]
        if len(lengthMoreThenZero)== 0:
            return [ayear, 0]
        return [ayear, np.mean([np.mean(v) for v in lengthMoreThenZero])]   

    def Q95(self):
        return self.TimeSeries.quantile(0.05, interpolation='linear')

    def Q75(self):
        return self.TimeSeries.quantile(0.25, interpolation='linear')

    @lazy_property
    def Q50(self):
        Q50 =self.TimeSeries.median()
        return Q50

    def Q25(self):
        return self.TimeSeries.quantile(0.75, interpolation='linear')

    def fre25(self):
        q25 = self.Q25();
        return self.EventFreq(lambda v : v > q25)[0]

    def fre75(self):
        q75 = self.Q75();
        return self.EventFreq(lambda v : v > q75)[0]

    def fre1(self):
        q50 = self.Q50;
        return self.EventFreq(lambda v : v > q50)[0]

    def fre3(self):
        q50 = self.Q50;
        return self.EventFreq(lambda v : v > 3*q50)[0]

    def fre7(self):
        q50 = self.Q50;
        return self.EventFreq(lambda v : v > 7*q50)[0]

    """
    Calculates the average number of timesteps where the value is above a threshold
    """
    def duration(self, Threshold):
        Durations = []
        Durations.append(0)

        for k,v in self.TimeSeries.items():
            if (v > Threshold):
                Durations[-1]+=1
            elif v <= Threshold and Durations[-1] > 0:
                Durations.append(0)
    
        if Durations[-1] == 0:
            del Durations[-1]
        if (len(Durations) == 0):
            return 0
        return np.mean(Durations)

    def values_above(self, Threshold):
        Durations = []
        Durations.append([])

        for k,v in self.TimeSeries.items():
            if (v > Threshold):
                Durations[-1].append(v)
            elif v <= Threshold and len(Durations[-1]) > 0:
                Durations.append([])
    
        if len(Durations[-1]) == 0:
            del Durations[-1]
        return Durations




    """
    Calculates the average number of timesteps where the value is below a threshold
    """
    def DurationBelow(self, Threshold):
        Durations = []
        Durations.append(0)

        for k,v in self.TimeSeries.items():
            if (v < Threshold):
                Durations[-1]+=1
            elif v >= Threshold and Durations[-1] > 0:
                Durations.append(0)
    
        if Durations[-1] == 0:
            del Durations[-1]
        if (len(Durations) == 0):
            return 0
        return np.mean(Durations)


    def DVFIEQR(self, sin = 2):
          p10p50 = self.TimeSeries.quantile([0.1, 0.5]);
          Q90 = p10p50[0.1]/p10p50[0.5];

          return 0.217+ 0.103*sin + 0.02 * Q90 * self.EventFreq(lambda v : v > p10p50[0.5])[0];


    def DVPIEQR(self):
        return 0.546 + 0.02 * self.fre25() - 0.019 * self.dur3() - 0.025 * self.fre75()


    def DFFV_EQR(self, sin = 2):
        p25 = self.Q75();
        p75 = self.Q25();
        return 0.811 * self.BaseFlowIndex() + 0.058 * sin + 0.05 * self.EventFreq(lambda v : v >= p75)[0] - 0.319 - 0.0413 * self.EventFreq(lambda v : v <= p25)[0];
    
    
    def medianmin(self):
        return self.TimeSeries.resample("A").min().median()

    def medianmax(self):
        return self.TimeSeries.resample("A").max().median()

    def medmin(self):
        return self.medianmin()/self.Q50

    def medmax(self):
        return self.medianmax()/self.Q50

    def mamin(self):
        return self.TimeSeries.resample("A").min().mean()/self.Q50

    def mamax(self):
        return self.TimeSeries.resample("A").max().mean()/self.Q50

    def mamax7(self):
        return self.__mamax( 7)

    def mamax30(self):
        return self.__mamax( 30)

    def fremedmin(self):
        val =self.medmin()
        return self.EventFreq( lambda v : v < val)[0]

    def mf(self):
        return self.TimeSeries.mean()

    def cv(self):
        return self.TimeSeries.var()

    def q1(self):
        return self.TimeSeries.quantile(0.01, interpolation='linear')/self.Q50

    def q10(self):
        return self.TimeSeries.quantile(0.1, interpolation='linear')/self.Q50

    def q25(self):
        return self.TimeSeries.quantile(0.25, interpolation='linear')/self.Q50

    def q75(self):
        return self.TimeSeries.quantile(0.75, interpolation='linear')/self.Q50

    def q90(self):
        return self.TimeSeries.quantile(0.90, interpolation='linear')/self.Q50

    def durmedmin(self):
        val =medmin(self.TimeSeries)
        return Duration(self.TimeSeries, val)

    def dur75(self):
        val =self.Q75()
        return self.DurationBelow( val)

    def dur1(self):
        val =self.Q50
        return self.duration( val)

    def dur3(self):
        val =self.Q50
        return self.duration( 3*val)

    def dur7(self):
        val =self.Q50
        return self.duration( 7*val)

    def dur25(self):
        val =Q25(self.TimeSeries)
        return Duration(self.TimeSeries, val)

    def pea1(self):
        val = self.Q50
        events = self.values_above( val)
        return np.mean([np.mean(t) for t in events])/val

    def pea3(self):
        val =self.Q50
        return np.mean([t for t in self.TimeSeries if t>3*val])/val

    def pea7(self):
        val =self.Q50
        return np.mean([t for t in self.TimeSeries if t>7*val])/val

    def pea25(self):
        val =Q25(self.TimeSeries)
        return np.mean([t for t in self.TimeSeries if t>val])/val

    def norises(self):
        toreturn =0
        for i in range(0,len(self.TimeSeries)-1):
            if(self.TimeSeries.values[i]<self.TimeSeries.values[i+1]):
                toreturn+=1
        return toreturn/len(self.TimeSeries)

    def nofalls(self):
        toreturn =0
        for i in range(0,len(self.TimeSeries)-1):
            if(self.TimeSeries.values[i]>self.TimeSeries.values[i+1]):
                toreturn+=1
        return toreturn/len(self.TimeSeries)


    def EQR_DFFV(self):
        return 0.38 - 0.01 * self.dur75() + 0.12 * self.pea1() - 0.1*self.dur7()

    def EQR_DFFV2(self):
        return 2.85 +1.531*self.mamin() - 0.031* self.fremedmin() - 9.206*self.norises()


    def __mamax(self, windowsize):
        maximums=[]
        for year in range(self.TimeSeries.index[0].year,self.TimeSeries.index[-1].year+1):
            maximums.append(self.TimeSeries[str(year)].rolling(windowsize, win_type='triang').sum().max())
        maximums =[max for max in maximums if not math.isnan(max)]
        return np.mean(maximums)/self.Q50


    """
    /// Calculates the Base flow Index(BFI) from http://nora.nerc.ac.uk/6050/1/IH_108.pdf
    /// The self.TimeSeries must contain daily values
    """
    def BaseFlowIndex(self):
        if len(self.TimeSeries) == 0:
            return -1;

        nDays = 5

        localcount = 0
        nDaysMin = []
        locallist = [];
        for i in range(0, len(self.TimeSeries)):
            if (localcount == nDays):
                min1 = min(locallist)
                nDaysMin.append([ i - nDays + locallist.index(min1) , min1])
                locallist = []
                localcount = 0
            locallist.append(self.TimeSeries[i]);
            localcount+=1
    

        Ordinates = []
        nDaysMin09 =[l[1]*0.9 for l in nDaysMin]
        for i in range(0, len(nDaysMin) - 2):
            centralvalue = nDaysMin09[i + 1];
            if centralvalue < nDaysMin[i][1]  and centralvalue < nDaysMin[i + 2][1]:
                Ordinates.append(nDaysMin[i + 1])
    

        interpolated = []

        if len(Ordinates) < 2:
            return 0

        l = interp1d([o[0] for o in Ordinates], [o[1] for o in Ordinates])

        i1 = Ordinates[0][0]
        i2 = Ordinates[-1][0]

        for i in range(i1, i2):
            idx =  math.floor( i / nDays);
            interpolated.append(l(i))


        Vb = sum(interpolated)
        vals = self.TimeSeries[i1:i2 - i1+1]
        Va = sum(vals)

        vv = 0;
        for i in range(1,len(vals)):
            vv += (vals[i] + vals[i -1]) / 2;
    
        vvb = 0;
        for i in range (0,len(Ordinates)-1):
            vvb += (Ordinates[i][1] + Ordinates[i + 1][1]) / 2 * (Ordinates[i + 1][0] - Ordinates[i][0]);

        return Vb / Va;
