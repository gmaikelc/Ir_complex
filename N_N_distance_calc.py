#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Gerardo Casanola, 17 November 2023 for The Rasulev Research Lab 
# Group at North Dakota State University

#MIT License

#Copyright (c) 2023 Gerardo Casanola

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE. 



import os
import csv
import numpy as np
from tkinter import Tk, filedialog

def calculate_distance(coord1, coord2):
    return np.linalg.norm(coord1 - coord2)

def read_xyz_file(file_path):
    with open(file_path, 'r') as xyz_file:
        lines = xyz_file.readlines()[2:]  # Skip the first two lines (number of atoms and comment)

    coordinates = []
    elements = []

    for line in lines:
        data = line.split()
        elements.append(data[0])
        coordinates.append([float(val) for val in data[1:]])

    return np.array(elements), np.array(coordinates)

def find_nitrogen_indices(elements):
    return [i for i, element in enumerate(elements) if element.upper() == 'N']

def process_xyz_files(folder_path):
    data = []

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xyz"):
            file_path = os.path.join(folder_path, file_name)

            # Read XYZ file
            elements, coordinates = read_xyz_file(file_path)

            # Find indices of nitrogen atoms
            nitrogen_indices = find_nitrogen_indices(elements)

            if len(nitrogen_indices) >= 2:
                # Calculate the Euclidean distance between all N-N pairs
                n_n_distances = []
                for i in range(len(nitrogen_indices)):
                    for j in range(i + 1, len(nitrogen_indices)):
                        distance = calculate_distance(coordinates[nitrogen_indices[i]], coordinates[nitrogen_indices[j]])
                        n_n_distances.append(distance)

                # Select the lowest N-N distance
                lowest_distance = min(n_n_distances)
                data.append((file_name, lowest_distance))

    return data

def write_to_csv(data, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['XYZ_File', 'Lowest_N-N_Distance'])

        for row in data:
            csv_writer.writerow(row)

def main():
    # Create a Tkinter root window (it will be hidden)
    root = Tk()
    root.withdraw()

    # Ask the user to select a folder containing XYZ files
    folder_path = filedialog.askdirectory(title="Select Folder with XYZ Files")

    if not folder_path:
        print("Folder selection canceled.")
        return

    # Process XYZ files in the specified folder
    data = process_xyz_files(folder_path)

    if not data:
        print("No XYZ files found in the specified folder.")
        return

    # Ask the user to specify the output CSV file name
    output_csv_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save CSV As")

    if not output_csv_file:
        print("CSV file selection canceled.")
        return

    # Write the data to a CSV file
    write_to_csv(data, output_csv_file)
    print(f"CSV file '{output_csv_file}' generated successfully.")

if __name__ == "__main__":
    main()

