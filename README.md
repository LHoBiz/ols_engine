# ols_engine
Generate obstacle limitation surfaces given parameters that describe airport data.

# usage
- enter airport data in the AirportData.csv data file
- In command prompt, call:
    - > python ols_engine.py
- Type the name of the airport as entered in AirportData.csv
- Select a number corresponding to the runway of interest
- Choose a grid size in m2 (e.g. '100' or '200')
- Find the file opened in Google Earth

# requirements
- The program uses the following import:
`from osgeo import osr`
so the python environment should have gdal installed.
- Google Earth Pro must be installed. https://www.google.com.au/intl/en_uk/earth/download/gep/agree.html
- I recommend either osgeo4w or conda.
- I've used gdal330 python38 in a conda environment
- I've also used python3 available via running osgeo4w.bat shell
- I noticed a PY_PROJ error, but did not impact the result. You can simply remove the existing path in system's environment variables, likely because postgis was installed?

# note
- I wrote this in late 2015 / early 2016, at a time when I first stumble across coding. At the time, I was just learning about loops and I had no idea what a class was or how to use them. So please forgive the horrible structure and lack of conventions as you look through the files. Dispite it being a mess, the code does produce functional OLS models quickly to a fairly high degree of accuracy assuming the input params are right and the grid size is set to something reasonable (e.g. 200 m). I'll get around to cleaning it up and making it better, perhaps add more functionality. 
- I hope this will be of use for others. And I hope that others may be able to contribute to this project!
- Reach out to be if you have any questions.
