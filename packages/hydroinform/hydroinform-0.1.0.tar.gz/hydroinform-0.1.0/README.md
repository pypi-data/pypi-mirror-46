# hydroinform
This package contains a steady-state stream model and some tools to access .dfs-files from DHI

# Usage
Write a pump extraction file to be used with MikeZero:
```sh
#Import DFS from HydroInform
from hydroinform import DFS

#The number of Items (In this case number of pumping wells)
numberofitems = 5;

#Now create the file.
_tso = DFS.DFS0.new_file(r'c:\temp\extraction.dfs0'), numberofitems);

#Loop the items and set the units etc.
for itemCount in range (0, numberofitems):
    _tso.items[itemCount].value_type = DFS.DataValueType.MeanStepBackward
    _tso.items[itemCount].eum_item = DFS.EumItem.eumIPumpingRate
    _tso.items[itemCount].eum_unit = DFS.EumUnit.eumUm3PerYear
    _tso.items[itemCount].name = "Item number: " + str(itemCount)
      
#Loop the years where you have pumping data
tscount = 0;
for year in range(2010, 2016):
    #For every year append a new timestep
    _tso.append_timestep(datetime.datetime(year, 12, 31, 12))
    #Loop the items and set a value for this timestep
    for itemCount in range (0, numberofitems):
        #Sets the data. Note that timesteps count from 0 and Items count from 1
        _tso.set_data(tscount, itemCount+1, year * itemCount)
    tscount+=1
#Call dispose which will save and close the file.
_tso.dispose();
```