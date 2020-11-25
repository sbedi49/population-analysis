# Population Analysis
Python script for ArcGIS 

The tool is designed to streamline the process of editing census data files to be imported into ArcGIS, the application takes in a raw census CSV file and edits the fieldnames by removing special characters and extracts county names into a new ‘County’ field. It then allows the user to customize the CSV file, by allowing them to sort through columns based on gender and by rows based on the counties they select. The tool then joins the customized CSV with a census tract shapefile, where the summary statistics and resulting map image are output into an HTML file.
