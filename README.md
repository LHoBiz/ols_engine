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
- I recommend either osgeo4w or conda.
- I've used gdal330 python38 in a conda environment
- I've also used python3 available via running osgeo4w.bat shell
- I noticed a PY_PROJ error, but did not impact the result. You can simply remove the existing path in system's environment variables, likely because postgis was installed?

