#!/usr/bin/python3
########################################################################################
#
# python script to read in a CSV export from mytimestation.com and process it so 
# that SES reports can be generated.
#
# Timestation report type: Employee Summary
#
########################################################################################
import sys
import csv
import datetime
import pandas

# Import parameter is the name of the CSV file exported from mytimestation.com
if len(sys.argv) != 2:
        print("Argument required!")
        print("The name of the CSV file exported from mytimestation.com 'Employee Summary' report")
        sys.exit(1)
else:
        import_file = sys.argv[1]

# Read and process the input CSV storing it in a list of dictionaries for later combination
ts_data = []
with open(import_file) as import_data:
    csv_reader = csv.DictReader(import_data)
    for row in csv_reader:
        # Combine separate date & time fields into a datetime
        date_parts = row["Date"].split("/")
        time_parts = row["Time"].split(":")
        timestamp = datetime.datetime(year=int(date_parts[2]),month=int(date_parts[1]),day=int(date_parts[0]),hour=int(time_parts[0]),minute=int(time_parts[1]))
        #print(row["Date"], row["Time"], timestamp)
        ts_data.append({"timestamp": timestamp, "name": row["Name"],"task": row["Department"], "activity": row["Activity"]})

# Need to combine the punch in and punch out rows to determine the elapsed time for each member's entry
# Sort the dictionary to facilitate this
ts_data = sorted(ts_data, key=lambda k: "%s %s %s %s" % (k["name"], k["task"], k["timestamp"], k["activity"]))

processed = []
name = None
timestamp = None
task = None
activity = None

# Process the sorted dictionary and combine entries
for entry in ts_data:
  #print(entry)
  
  if entry['activity'] == "Punch In":
    # Save details from the punch in to compare and combine
    if activity == entry['activity'] and name == entry['name']:
      # The name and the task should match the previous punch in event
      print("DUPLICATE Punch In: ",entry)
    name = entry['name']
    timestamp = entry['timestamp']
    task = entry['task']
    activity = entry['activity']
  elif entry['activity'] == "Punch Out":
    if name != entry['name'] or task != entry['task']:
      # The name and the task should match the previous punch in event
      print("ERROR on: ",entry," != saved values: ",name,task)
    else:
      # Calculate the elapsed time
      elapsed = entry['timestamp'] - timestamp
          # Add the combined entry to the processed list
          #processed.append({'timestamp': timestamp, 'name': name, 'task': task, 'elapsed': elapsed.total_seconds()})
      # Drop the timestamp as it is not required for the aggregations
      processed.append({'name': name, 'task': task, 'elapsed': elapsed.total_seconds()})
      elapsed = None
      activity = entry['activity']

    # Sort the list by timestamp for reporting purposes
    #processed = pandas.DataFrame(sorted(processed, key=lambda k: "%s %s %s" % (k['timestamp'], k['name'], k['task'])))
    #processed = pandas.DataFrame(sorted(processed, key=lambda k: "%s %s" % (k['name'], k['task'])))
    #for row in processed:
    #  print(row)    
  
# Generate the reports, does python do pivot tables?
# Or do I just generate them manually?
# Or do I stick them in a google sheet and extract from there?

# TBD

# Convert the list of dictionaries to a pandas DataFrame for aggregation purposes
processed = pandas.DataFrame(processed)

# Display the total time for each task
print("======================================================")
print("Total time by task")
print("======================================================")
      
print(processed.groupby(['task'])['elapsed'].agg(['sum'])/3600)

#print("DEBUG ZERO\n",processed)

# Display the top 10 performers for each task type
task_types = {"Administration - M", "Community Engagement - M", "Meeting - M", "Operations - M", "Other - M", "Training - M"}
for task_type in task_types:
    print("")
    print(task_type)
    print("======================================================")

    # Select only the rows where the task is the one we want
    tasks = processed.loc[(processed.task == task_type,["name", "elapsed"])]
    #print("DEBUG ONE\n",tasks)

    # group by the member name
    tasks = tasks.groupby("name")["elapsed"].agg(sum)
    #print("DEBUG TWO\n",tasks)
    # convert the aggregated results back to a dictionary and sort it
    # as it seems to be impossible to sort the data frame by the aggregated sum
    sorted_set = sorted(tasks.to_dict().items(), key=lambda x:x[1], reverse=True)
    #print("DEBUG THREE\n",sorted_set)
    count = 0
    for item in sorted_set:
        print(item[0],",",round(item[1]/3600,1))
        count += 1
        #if count == 10:
        #    break

