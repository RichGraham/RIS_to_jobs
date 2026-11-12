# RIS\_to\_jobs
Frame work to extract roles from RIS exports

## Basic install
### Command line
Consider running tests first (see section below). Make sure you have a ~/bin folder, eg by running

	mkdir ~/bin
	
The ~/bin folder needs to be in your $PATH.

Then cd into the repo folder and run

	./installHelperScripts.sh

### Mac OS X applescripts
For Mac OS X it is possible to replace the commandline with Finder-based applescripts. Complete the command line install above and make sure you have the folder ~/Apps

Then, from the repo folder run

	./compile_applescripts.sh
	
Finally go to ~/Apps in Finder and command-drag each of the App files into the Finder side bar so they can be clicked to run on the current Finder folder with the default input filenames.

## Tests
### Simple run

	./runTests.sh
### Fancier run with sound effects

	./unitTests.sh

### Coverage tests

	./coverageTest.sh
	
# Mac Finder approach
## Checking for names (Steps 1-4)
Navigate the Finder to the working folder, containing a fresh set of downloaded projects. Then run the steps below as many times as required by clicking the app in the Finder side-bar.

### 1_PassA.app
Initial check for errors and that no text has been wrongly identified as a name. If any jobs are incorrectly identified as having a name, then add the full job name to *false_positives.txt* (in the current directory). Repeat command until no false positives are found.

### 2_CheckTitle.app
checks for names in the project title. Here just the name should be removed and what's left should still make reasonable sense. This pass shows identified names. If there are any false positives then add the full project title to *false_positives.txt* (in the current directory). Repeat command until no false positives are found.

Sometimes a name is found but extra works are included, eg 'Bob Jones Chemisty' is indentified as a name. If the remaining title still makes sense then leave this as it is. If the title is too badly mangled then add the full actual name to *real_names.txt* (in the current directory).

If all words are removed from a title then this raises an error - either fix by adding to *false_positives.txt*, *real_names.txt* or by changing the title in the project xlsx file.

### 3_CheckRoles.app
Highlights role names so you can check if any real names have crept through. If any roles contain a name, add the full name to *real_names.txt* (in the current directory).

#### 4_ViewTitles.app
Lists all project titles so you can check for names. If any title contain a name, add the full name (and any surrounding text eg fellowship) to *real_names.txt* (in the current directory) to have it stripped from the title.

## Make Mail Merge File (Step 5)
### 5_MakeMailMerge.app
Takes all files named Pro*.xlsx in current folder and makes the mail merge excel file
The following are moved into a folder named by the current date and time:

* All project files with eligible jobs
* The mail merge file Mail_Merge.xlsx
* A python pickle containing the extracted project and role information
All files with no elligble jobs are deleted.
The master text file with all job emails that have gone out is updated with the RIS ID of those projects that have an email to be sent.

### Carry out mail merge
Use the resulting file Mail_Merge.xlsx in Microsoft Flow to send permission emails to PIs. Wait for response to complete.

## Assemble the PI responses (Step 6)
Navigate into the date-stamped folder where the Mail_Merge.xlsx sits. Add to this folder the following files:
###Flow export file (csv file)
Must be exported from Teams (this can take several hours!!!). Filename is <DateRange>\_Basic.csv. 

### Updated Mail Merge File (xlsx file)
Named Mail\_Merge\_\<DATE\>.xlsx. Contains PI outcomes but might be less reliable than the Flow Export file above. Can found in Teams (Teams> Researcher Transition Support pilot > General > shared (top) - Find file Mail\_Merge_<DATE>.xlsx ).

### 6_CorrectMailMerge.app
Applies the changes in the csv file (above) to the xlsx file, writing to the new file Mail\_Merge\_PI\_Response.xlsx. Also checks all xlsx projects are in the Teams file and that only empty cells are corrected. If the xlsx file has no email approval ID then the response is automaticall taken to be 'Reject'.

### 7_ApplyPiResponse.app

Takes the PI response Excel sheet, applies PI's decision and creates database upload excel sheet (Database_Entries.xlsx).


Continue to work in the date-stamped folder Eg: (Mar-03-2026_18-50)
Assumes that the PI responses are stored in the file **Mail\_Merge\_PI\_Response.xls**. Run by clicking the app in the Finder side-bar.
The database upload excel sheet(Database_Entries.xlsx) is then created.

Also creates a text file **PI\_email\_list.txt** which can by copy/pasted into an email to inform PIs their project has been added to the database.

### 8_Accepted\_and\_Deleted.app
Produces an excel file, ToChange.xlsx, that lists all files in the database snapshot whose status needs to change.

Make a fresh folder (eg Status_Flip\_\<DATE\>). Add the following input files.

* An xml file of accepted grants (downloaded from RIS), must be named FindAcceptedGrants.xml
* An xml file of unsucessful grants (downloaded from RIS), must be named FindUnsuccessfulGrants.xml
* A downloaded snapshot of the database (csv file), must be named 'Researcher Transition Support.csv'

Make sure the current Finder window shows this folder.


Clicking the command in the Finder side bar produces an excel file, ToChange.xlsx, that lists all files in the database snapshot whose status needs to change.
	
# Command line approach

## Pass1
Initial check for errors and that no text has been wrongly identified as a name

	Pass1_Check_For_Names.py Pro*.xlsx

For more information in the output add the -x flag, ie

	Pass1_Check_For_Names.py Pro*.xlsx -x

If any jobs are incorrectly identified as having a name, then add the full job name to *false_positives.txt* (in the current directory). Repeat command until no false positives are found.

### Checking titles
A similar pass to above checks for names in the project title. Here just the name should be removed and what's left should still make reasonable sense. To run the command add the -t flag

	Pass1_Check_For_Names.py -t Pro*.xlsx

This pass shows identified names. If there are any false positives then add the full job title to *false_positives.txt* (in the current directory). Repeat command until no false positives are found.

Sometimes a name is found but extra works are included, eg 'Bob Jones Chemisty' is indentified as a name. If the remaining title still makes sense then leave this as it is. If the title is too badly mangled then add the full actual name to *real_names.txt* (in the current directory).

## Pass2
Highlights role names so you can check if any real names have crept through. Also catches some other errors with the roles

	Pass2_Check_Roles.py Pro*.xlsx

As above an expanded view is available (and also -m to show jobs in markdown view)

	Pass2_Check_Roles.py -x -m Pro*.xlsx

If any roles contain a name, add the full name to *real_names.txt* (in the current directory).


## Pass3
Lists all project titles so you can check for names

	Pass3_Check_Titles.py Project*.xlsx

If any title contain a name, add the full name (and any surrounding text eg fellowship) to *real_names.txt* (in the current directory) to have it stripped from the title.

## Make\_Mail\_Merge_Excel
Takes all files named Pro*.xlsx in current folder and makes the mail merge excel file

	Make_Mail_Merge_Excel.py

The following are moved into a folder named by the current date and time:

* All project files with eligible jobs
* The mail merge file Mail_Merge.xlsx
* A python pickle containing the extracted project and role information
All files with no elligble jobs are deleted.
The master text file with all job emails that have gone out is updated with the RIS ID of those projects that have an email to be sent.

## Checking the updated Mail Merge file

### Flow export file (csv file)
Must be exported from Teams (this can take several hours!!!). Filename is <DateRange>\_Basic.csv. Move this into folder Working Folder/\<DATE\>

### Updated Mail Merge File (xlsx file)
Named Mail_Merge\_\<DATE\>.xlsx. Contains PI outcomes but might be less reliable than the Flow Export file above. Can found in Teams (Teams> Researcher Transition Support pilot > General > shared (top) - Find file Mail_Merge_date.xlsx ) Must be copied to Working Folder/\<DATE\>

### Correct\_Mail\_Merge.py
This command applies the changes in the csv file (above) to the xlsx file, writing to the new file Mail\_Merge\_PI\_Response.xlsx. Also checks all xlsx projects are in the Teams file and that only empty cells are corrected.

	Correct_Mail_Merge.py Mail_Merge_<date>.xlsx <DateRange>_Basic.csv

Adding the -t flag runs the command, with screen output, but doesn't write the file.

### No\_Args\_Correct\_Mail_Merge.py
Same command as Correct\_Mail\_Merge.py but requires no arguments. Instead the command tries to find the two input files in the current folder. It looks for '\*.csv files', if there's only one, it assumes this is the Flow Export File (otherwise I returns an error). It then looks for ''Mail_Merge \*.xlsx' (note space in filename). If there's one matching file it uses this as the Updated Mail Merge excel file, otherwise it returns an error.

## Apply\_PI\_response.py
Takes the PI response Excel sheet, applies PI's decision and creates database upload excel sheet (Database_Entries.xlsx).


Need to change directory into where the Mail Merge file was created. Eg:

	cd Mar-03-2026_18-50
Assumes that the PI responses are stored in the file **Mail\_Merge\_PI\_Response.xls**. To run type:

	Apply_PI_response.py

The database upload excel sheet(Database_Entries.xlsx) is then created.

	
## Upgrade\_To\_Accepted\_List.py
Requires the following input files.

* An xml file of accepted grants (downloaded from RIS), eg FindAcceptedGrants.xml
* A downloaded snapshot of the database (csv file), eg 'Researcher Transition Support.csv'


		Upgrade_To_Accepted_List.py FindAcceptedGrants.xml Researcher\ Transition\ Support.csv
	
The above command produces an excel file, ToBeUpgraded.xlsx, that lists all files in the database snapshot that need to be upgraded to 'Funding Accepted'.

## Accepted\_and\_Deleted.py 
Requires the following input files.

* An xml file of accepted grants (downloaded from RIS), must be named FindAcceptedGrants.xml
* An xml file of unsucessful grants (downloaded from RIS), must be named FindUnsuccessfulGrants.xml
* A downloaded snapshot of the database (csv file), must be named 'Researcher Transition Support.csv'

	Accepted\_and\_Deleted.py 
	
The above command produces an excel file, ToChange.xlsx, that lists all files in the database snapshot whose status needs to change.

## Get\_Named\_Researcher\_Report
Counts named researchers in each batch and creates breakdown report.

Start by moving the working directory to the 'Working folder'. The script needs a file 'folder_list.txt' than contains a list of all batch folders to be included in the analysis. That is the contents should be:

	Folder_1
	Folder_2
	etc....
Avoid spaces at line ends	
Create or update this file as needed.

Then run 

	Get_Named_Researcher_Report.py
	

Code creates a series of excel reports as described in the script output.
