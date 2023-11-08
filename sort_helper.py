import csv
import pandas as pd


def li_csv_sort(csv_file, sort_key='Age', sort_reverse=False):
    """Linked In CSV File Sortint
        li_csv_sort('filename.csv', [sort_key='Age', sort_reverse=False])
        - 'filename.csv': name of the csv file do sort
        - sort_key: name of the base key to sort the file - Age(by date, DEFAULT VALUE); Title; Company
        - sort_reverse: reverse sort order, DEFAULT=False"""
    
    # declare listings variable
    listed_entries = []

    # check for a valid csv file, return error otherwise
    filename = csv_file.split(".")
    if filename[1] != "csv":
        raise ValueError("Not a .csv File")
    
    # read through the file to sort and fill the listings list with clean data
    with open(csv_file, 'r') as File:
        reader = csv.DictReader(File)
        for row in reader:
            row["Post Date"] = row["Post Date"].lstrip("b'").rstrip("'")
            row["Title"] = row["Title"].lstrip("b'").rstrip("'")
            row["Company"] = row["Company"].lstrip("b'").rstrip("'")
            row["Location"] = row["Location"].lstrip('"b').rstrip('"')
            row["Apply"] = row["Apply"].lstrip('b')

            # manage the 'Post Date' data to allow sorting
            date = row["Post Date"].split(" ")
           
            if date[1] not in ["day", "days"]:
                if date[1] in ["month", "months"]:
                    date[0] = int(date[0])*30
                    row["Post Date"] = f"More than {date[0]} days ago"
                elif date[1] in ["week", "weeks"]:
                    date[0] = int(date[0])*7
                    row["Post Date"] = f"More than {date[0]} days ago"

            row["Time"] = int(date[0])

            listed_entries.append({"Title": row["Title"], "Company": row["Company"], "Location": row["Location"], "Apply": row["Apply"], "Date": row["Post Date"], "Age": row["Time"]})

    # delete the Age field used for date sorting
    listed_entries = sorted(listed_entries, key=lambda row: row[sort_key], reverse=sort_reverse)
    for row in listed_entries:
        del row["Age"]

    # write data to new csv file
    with open('sortedCSV.csv', 'a') as sorted_csv:
        fieldnames = ["Title", "Company", "Location", "Apply", "Date"]
        writer = csv.DictWriter(sorted_csv, fieldnames=fieldnames) 
        writer.writeheader()
        for row in listed_entries:
            writer.writerow(row)
            

def main():
    li_csv_sort('linkedin-jobs.csv', 'Company', True)


if __name__ == "__main__":
    main()