# Population Analysis Project
Python script for ArcGIS 
# Description
The tool is designed to streamline the process of editing census data files to be imported into ArcGIS, the application takes in a raw census CSV file and edits the fieldnames by removing special characters and extracts county names into a new ‘County’ field. It then allows the user to customize the CSV file, by allowing them to sort through columns based on gender and by rows based on the counties they select. The tool then joins the customized CSV with a census tract shapefile, where the summary statistics and resulting map image are output into an HTML file.
# Requirements
To use this tool you must have/include:
<ul>
  <li>ArcGIS Desktop/ArcCatalog</li>
  <li>CSV file for conversion</li>
  <li>Census Tract Shapefile</li>
  <li>ArcMap Document Path</li>
  <li>Output Folder path</li>
</ul>

# Instructions using Sample Data
<ol>
  <li> Download the <i>Population Analysis.tbx</i> and add to ArcCatalog </li>
  <li> Download sample input CSV and sample shapefile from <i>Sample Inputs.zip</i> and extract files to <b>C:\</b> </li>
  <li>Download <i>My</i> folder onto <b>C:\</b>  (the folder contains a <i>test.mxd</i> file where the map will be drawn)  </li>
 <i>**If you want to extract files elsewhere make sure you also change the default relative paths in the GUI</i>
  <li> Run the script from ArcGIS Desktop and input GUI prompts (the default paramaters should work if paths werent changed)</li>
</ol>

# GUI

<img src="https://github.com/sbedi49/population-analysis/blob/main/GUI.png?raw=true" alt="GUI" />
