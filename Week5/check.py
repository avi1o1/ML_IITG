import csv

# Read the first file
with open('Week5/check1.csv', 'r') as file:
    reader = csv.reader(file)
    file1 = [row for row in reader]

# Read the second file
with open('Week5/check2.csv', 'r') as file:
    reader = csv.reader(file)
    file2 = [row for row in reader]

# Read the third file
with open('Week5/check3.csv', 'r') as file:
    reader = csv.reader(file)
    file3 = [row for row in reader]

# Compare the files and store mismatch indices
mismatch_indices = [i for i, (row1, row2, row3) in enumerate(zip(file1, file2, file3)) if row1 != row2 or row1 != row3 or row2 != row3]

# Print the count of mismatches
print(len(mismatch_indices))

# Print the mismatch indices
print(mismatch_indices)