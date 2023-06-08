# Majura Timestation Reports

## Purpose

Reports generated from timestation require some processing to be easily consumable by a spreadsheet.  

While they are generated as CSV files, they need to be merged as each activity for a team member (sign in, sign out) is a separate record and there is no easy way of linking them.

For example:
```
"Date","Employee ID","Name","Department","Device","Time","Activity","Punch Method","IP Address","Notes"
"01/12/2022","","A Member","Training - M","MAJSES","18:37","Punch In","PIN","",""
"01/12/2022","","B Member","Training - M","MAJSES","18:38","Punch In","PIN","",""
"01/12/2022","","C Member","Training - M","MAJSES","18:39","Punch In","PIN","",""
"01/12/2022","","B Member","Training - M","MAJSES","20:21","Punch Out","PIN","",""
"01/12/2022","","A Member","Training - M","MAJSES","20:29","Punch Out","PIN","",""
"01/12/2022","","C Member","Training - M","MAJSES","21:00","Punch Out","PIN","",""
```

Need to match Punch In with Punch Out for a given member on a given day (or over a day boundary)

This Python script does this and generates output that can be cut/pasted into a spreadsheet.

**Note:** There would be better ways of doing this via the API but my TimeStation account is not authorised to use the API.

## Instructions

From Timestation, generate a an **Employee Summary** report for the required reporting period.

Download the result as a CSV and then execute the script:

`$ ./gen-timestation-report.py ~/Downloads/TimeStation_Report_20230424_0908.csv `

Copy the output you want into sheets in a spreadhseet (eg: A Google Sheet on the Majura IT Drive) and format as required.
