import arcpy, sys, os

# User inputs
basename = arcpy.GetParameterAsText(0)
input= arcpy.GetParameterAsText(1)
gender = arcpy.GetParameterAsText(2)
get_countyList = arcpy.GetParameterAsText(3)
shapefile = arcpy.GetParameterAsText(4)
mapDoc = arcpy.GetParameterAsText(5)
output=arcpy.GetParameterAsText(6) +'\\' + basename
removeFiles = arcpy.GetParameterAsText(7)
output2 = output + '.csv'

# Convert unicode obtained from county parameter and convert to string
user_county = [i[1:-1].decode("utf-8").encode("utf-8").lstrip() for i in get_countyList.split(";")]

# Dictionary for Repairing Field Names (15 or Less)
headersDict = {'and':'',
               'AND':"",
               'AGE':"",
               'Number;':"",
               'SEX':"",  
               '-':"",
               'Total':"T",
               'Female':"F",
               'Male':"M",
               'to':'_',
               'population':"pop",
               'Median':"Med",
               'Under':"U",
               'over':"ovr",
               }

with open(input,'r') as unedited_csv:
    with open(output + 'Full.csv','w') as edited_csv:
        # Read and Delete First Line
        delLines = unedited_csv.readline()
        del delLines
        # Store headers in a list to be repaired
        headersList = unedited_csv.readline().split()
        # Replace headers with values in dictionary
        for i,v in enumerate(headersList):
            for k in headersDict:
                if k in v:
                    headersList[i] = v.replace(k,headersDict[k])
                     # Remove Special Cases and Spaces
                    headersList = [x.replace('(years)','yrs') for x in headersList]
                    list = ''.join(headersList).split(',')
                    fieldnames = [x.replace(' ','') for x in list]
        # Append County to Fieldnames List
        fieldnames.append('County\n')
        fieldnames = ','.join(fieldnames)
        # Write fieldnames in the first row
        line = 0
        for row in unedited_csv:
            rows = row.split(',')
            if line == 0:
                edited_csv.write(fieldnames)
                line +=1
        # Extract County names from 'Geography' and write names to County Field
            else:
                counties = rows[2].split(';')[1]
                update = [x.rstrip() for x in rows]
                update.append(counties + '\n')
                county = ','.join(update)
                edited_csv.write(county)                 
                        
arcpy.AddMessage('Editing Field Names Complete!')

# Dictionary for User Input
mydict = {'Male':'Mpop',
          'Female':'Fpop',
          'Total':'Tpop'}
columns=[]
rows=[]
index = []

# Write edited csv according to user input
with open(output + 'Full.csv','r') as read_csv:
    with open(output2,'w') as user_out:
        for line in read_csv:
            data = line.split(',')
             # Check to see if user selected gender matches value in mydict
            for i,v in enumerate(data):
                v = v.rstrip()
                for key,value in mydict.items():
                    if key == gender:
                        val = mydict.get(key)
                # Append the columns needed to be written to outfile for selected gender
                if val in v or v == 'County' or v == 'Id':
                    index.append(i)
                    columns.append(v)
                    index.sort()
                # Get the rows specified by user for the counties selected
                for county in user_county:
                # Strip any escape characters when checking for county and append the rows to list
                    if county == v.rstrip().lstrip():
                        for i in index:
                            rows.append(data[i])
                                
    # Write user specified rows to output file
        r = 0
        if r == 0:
            column = ','.join(columns)
            user_out.write(column)
            r += 1
            if r == 1:
                user_out.write('\n')
                for row in rows:
                    row = row.rstrip().lstrip()
                    user_out.write(row + ',')
                    if row.endswith('County'):
                        user_out.write('\n')
                        
arcpy.AddMessage('Customized CSV file Complete!')

# Set environment Settings
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames=False
try:  
    #Make feature layer from input shapefile
    flayer = output + 'layer'
    arcpy.MakeFeatureLayer_management(shapefile,flayer)
    # Join Feature Layer and Copy Layer into Memory
    joined=arcpy.AddJoin_management(flayer,'GEO_ID',output2,'Id','KEEP_COMMON')
    joinOutput = output + '.shp'
    arcpy.CopyFeatures_management(joined,joinOutput)
    arcpy.AddMessage("Joined Shapefile created in {0}".format(joinOutput))
except arcpy.ExecuteError:    
    arcpy.AddError(arcpy.GetMessages(2)) 

class Report(object):
    '''Class created to calculate table of reports for joined shapefile
           Sum, Mean, Max and Min are functions that can be called'''
    
    def __init__(self,fc,output):
        '''Initialize parameters: input feature class and output location required'''
        self.fc = fc
        self.output = output

    def Sum(self):
        '''Creates a table of sum values for the selected gender and counties'''
        stats =[]
        fields = arcpy.ListFields(self.fc)
        for field in fields:
            if 'pop' in field.name:
                stats.append([field.name,"SUM"])
        arcpy.Statistics_analysis(self.fc,self.output,stats)
        print "Sum Calculated"

    def Mean(self):
        '''Creates a table of mean values for the selected gender and counties'''
        stats =[]
        fields = arcpy.ListFields(self.fc)
        for field in fields:
            if 'pop' in field.name:
                stats.append([field.name,"MEAN"])
        arcpy.Statistics_analysis(self.fc,self.output,stats)
        print "Average Calculated"

    def Max(self):
        '''Creates a table of max values for the selected gender and counties'''
        stats =[]
        fields = arcpy.ListFields(self.fc)
        for field in fields:
            if 'pop' in field.name:
                stats.append([field.name,"MAX"])
        arcpy.Statistics_analysis(self.fc,self.output,stats)
        print "Max Calculated"

    def Min(self):
        '''Creates a table of min values for the selected gender and counties'''
        stats =[]
        fields = arcpy.ListFields(self.fc)
        for field in fields:
            if 'pop' in field.name:
                stats.append([field.name,"Min"])
        arcpy.Statistics_analysis(self.fc,self.output,stats)
        print "Min Calculated"
        
# The code in each of the functions above in the Report Class was thanks to:
# https://desktop.arcgis.com/en/arcmap/10.3/tools/analysis-toolbox/summary-statistics.html
# The original code snippet:  for field in arcpy.ListFields(intable):
#                                if field.type in ("Double", "Integer", "Single", "SmallInteger"):
#                                   stats.append([field.name, "Sum"])

def ExtractSummary(table):
    '''Purpose is to extract values from summary reports
            and append to list to be added to HTML Table'''
    sumList=[]
    with open(table,'r') as summary:
        headers=summary.readline()
        del headers
        num = summary.readline().split(',')
        sumList.append(num[2:len(num)])
        for sum in sumList:
            values = [round(float(val),1) for val in sum]
        return values


def Exists(path):
    '''Checks to see if path exists and removes it'''
    if os.path.exists(path):
        os.remove(path)
    else:
        pass
    
# Extract Sum values from each of population fields
# And create report instance
SumOut = output+ "Sum.csv"
Exists(SumOut)
r1=Report(joinOutput,SumOut).Sum()
sum = ExtractSummary(SumOut)

# Extract Mean values from each of population fields
MeanOut = output + "Mean.csv"
Exists(MeanOut)
r2=Report(joinOutput,MeanOut).Mean()
mean=ExtractSummary(MeanOut)

# Extract Max values from each of population fields
MaxOut = output+"Max.csv"
Exists(MaxOut)
r3=Report(joinOutput,MaxOut).Max()
max=ExtractSummary(MaxOut)

# Extract Min values from each of population fields
MinOut = output + "Min.csv"
Exists(MinOut)
r4=Report(joinOutput,MinOut).Min()
min=ExtractSummary(MinOut)

# Check to see if user wants to remove extra files
if removeFiles == 'Yes':
    os.remove(SumOut)
    os.remove(SumOut+'.xml')
    os.remove(MeanOut)
    os.remove(MeanOut + '.xml')
    os.remove(MaxOut)
    os.remove(MaxOut+'.xml')
    os.remove(MinOut)
    os.remove(MinOut+'.xml')
    os.remove(os.path.dirname(output) + '/schema.ini')
else:
    pass

def htmlTable(list):
    '''Creates HTML table output with the summary statistics for each specified field'''

    # Create table headers for each population field
    tableHead = ['<th>' + str(item) + '</th>' for item in list[1:len(list)-1]]
    
    # Creates corresponding rows for each summary statistic value
    tableSum=['<td>' + str(item) + '</td>' for item in sum]
    tableMean=['<td>' + str(item) + '</td>' for item in mean]
    tableMax=['<td>' + str(item) + '</td>' for item in max]
    tableMin=['<td>' + str(item) + '</td>' for item in min]
    
    # Join each row to be added to the table
    headers = '''\n    '''.join(tableHead)
    sumRows = '''\n    '''.join(tableSum)
    meanRows = '''\n    '''.join(tableMean)
    maxRows = '''\n    '''.join(tableMax)
    minRows = '''\n    '''.join(tableMin)
    
    #Create HTML Table
    htmlTable = '''
    <table border="2">
        <tr>
        <th></th>
        {0}
        </tr>
        <tr>
        <td><b>Sum</b></td>
        {1}
        </tr>
        <tr>
        <td><b>Mean</b></td>
        {2}
        </tr>
        <tr>
        <td><b>Max</b></td>
        {3}
        </tr>
        <tr>
        <td><b>Min</b></td>
        {4}
        </tr>
    </table>
    '''.format(headers,sumRows,meanRows,maxRows,minRows)
    return htmlTable

# Use columns list to get user selected columns and pass into htmlTable
table = htmlTable(columns)

# Automatically Display Map
try:
    mxd = arcpy.mapping.MapDocument('CURRENT')
    dfs = arcpy.mapping.ListDataFrames(mxd)
    df = dfs[0]
    layerObj = arcpy.mapping.Layer(joinOutput)
    arcpy.mapping.AddLayer(df,layerObj)
except:
    arcpy.AddMessage('Error Displaying Map')
    
# Create map from user specified MXD and Export PNG to be added to HTML output
mxd = arcpy.mapping.MapDocument(mapDoc)
dfs = arcpy.mapping.ListDataFrames(mxd)
df = dfs[0]
layerObj = arcpy.mapping.Layer(joinOutput)
arcpy.mapping.AddLayer(df,layerObj)
copyName = output + '.mxd'
mxd.saveACopy(copyName)
imageOut = output + '.png'
arcpy.mapping.ExportToPNG(mxd,imageOut)
del mxd
arcpy.AddMessage('PNG image created in {0}'.format(imageOut))

# Create HTML Report Output 
with open(output+'Report.html','w') as html:
     head =  '''<!DOCTYPE html>
         <html>
         <body> '''
     title = '''<h1>Population Analysis by Gender for:</h1>
                <h3>{0}</h3>'''.format(user_county[0:len(user_county)])
     
     image = '''<img src="{0}" alt='Map' width=600 height=600 /img> '''.format(imageOut)
     footer = '''</body>
         </html> '''
     html.write(head)
     html.write(title)
     html.write(table)
     html.write(image)
     html.write(footer)

arcpy.AddMessage('HTML Summary Report Created!')
