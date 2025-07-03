import csv
import random
import math
import sys
import numpy as np
import os
import openpyxl

# Global array
custom = []
n = 1000
step = 10
results = []
number = 0
customfilepath = ""

def readCustomArray(filepath, no):
    global custom
    global number
    number = no

    absolute_path = filepath
    # Check if file exists
    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"File '{filepath}' not found in application directory")

    # Clear existing custom array
    custom.clear()

    # Handle CSV files
    if absolute_path.endswith(".csv"):
        with open(absolute_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Ensure row is not empty
                    if row[0].isdigit():
                        custom.append(int(row[0]))
                    else:
                        raise ValueError(f"Invalid data '{row[0]}' in CSV file. Expected an integer.")

    # Handle XLSX files
    elif absolute_path.endswith(".xlsx"):
        workbook = openpyxl.load_workbook(absolute_path)
        sheet = workbook.active  # Use the first sheet
        for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
            if row[0] is not None:  # Ensure the cell is not empty
                if isinstance(row[0], int):
                    custom.append(row[0])
                else:
                    raise ValueError(f"Invalid data '{row[0]}' in XLSX file. Expected an integer.")
    else:
        raise ValueError("Unsupported file type. Only .csv and .xlsx are supported.")

    global n
    global customfilepath
    customfilepath = filepath
    n = len(custom)



def sortedRange(n):
    return list(range(1, n + 1))

def reverseSortedRange(n):
    return list(range(n, 0, -1))

def random_arr(n):
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    return arr

    t = 0
    n = len(arr)
    for i in range(1, n):
        t += 1
        key = arr[i]
        t += 1
        j = i - 1
        t += 1
        while j >= 0 and arr[j] > key:
            t += 1
            arr[j + 1] = arr[j]
            t += 1
            j -= 1
            t += 1
        arr[j + 1] = key
        t += 1
    return t

def generate_best_case_array(n):

    def build_best_case(low, high):
        if low > high:
            return []
        mid = (low + high) // 2
        return build_best_case(low, mid - 1) + build_best_case(mid + 1, high) + [mid]
    
    return build_best_case(1, n)

def generate_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["n", "t"])
        writer.writerows(results)
    print(f"CSV file generated successfully: {filename}")

def insertion_sort(arr):
    t = 0
    n = len(arr)
    t += 1
    for i in range(1, n):
        t += 1
        key = arr[i]
        t += 1
        j = i - 1
        t += 1
        while j >= 0 and arr[j] > key:
            t += 1
            arr[j + 1] = arr[j]
            t += 1
            j -= 1
            t += 1
        arr[j + 1] = key
        t += 1
    return t

def merge_sort(arr):
    t = 0

    def merge_sort_helper(arr):
        nonlocal t
        t_local = 1  # Initialize local counter for this call
        if len(arr) <= 1:
            return arr, t_local
        mid = len(arr) // 2
        t_local += 1
        left_half, t_left = merge_sort_helper(arr[:mid])
        t_local += t_left
        right_half, t_right = merge_sort_helper(arr[mid:])
        t_local += t_right
        merged_arr, t_merge = merge(left_half, right_half)
        t_local += t_merge
        return merged_arr, t_local

    def merge(left, right):
        nonlocal t
        t_local = 0  # Initialize local counter for merge operations
        sorted_arr = []
        t_local += 1
        i = j = 0
        t_local += 1
        while i < len(left) and j < len(right):
            t_local += 1
            if left[i] < right[j]:
                t_local += 1
                sorted_arr.append(left[i])
                t_local += 1
                i += 1
                t_local += 1
            else:
                t_local += 1
                sorted_arr.append(right[j])
                t_local += 1
                j += 1
                t_local += 1
        
        while i < len(left):
            t_local += 1
            sorted_arr.append(left[i])
            t_local += 1
            i += 1
            t_local += 1
            
        while j < len(right):
            t_local += 1
            sorted_arr.append(right[j])
            t_local += 1
            j += 1
            t_local += 1

        return sorted_arr, t_local

    _, t_final = merge_sort_helper(arr)
    t = t_final
    arr[:], _ = merge_sort_helper(arr)
    return t

def heap_sort(arr):
    t = 0

    def max_heapify(arr, n, i):
        nonlocal t
        t_local = 0
        largest = i
        t_local += 1
        left = 2 * i + 1
        t_local += 1
        right = 2 * i + 2
        t_local += 1
        if left < n and arr[left] > arr[largest]:
            t_local += 1
            largest = left
            t_local += 1
        if right < n and arr[right] > arr[largest]:
            t_local += 1
            largest = right
            t_local += 1
        if largest != i:
            t_local += 1
            arr[i], arr[largest] = arr[largest], arr[i]
            t_local += 1
            t_local += max_heapify(arr, n, largest)[0]
        return t_local,

    def build_max_heap(arr):
        nonlocal t
        t_local = 0
        n = len(arr)
        t_local += 1
        for i in range(n // 2 - 1, -1, -1):
            t_local += 1
            t_local += max_heapify(arr, n, i)[0]
        return t_local,
    
    t_build_heap, = build_max_heap(arr)
    t += t_build_heap
    n = len(arr)

    for i in range(n - 1, 0, -1):
        t += 1
        arr[i], arr[0] = arr[0], arr[i]
        t += 1
        t_heapify, = max_heapify(arr, i, 0)
        t += t_heapify
    return t

def bubble_sort(arr):
    t = 0
    n = len(arr)
    t += 1
    for i in range(n):
        t += 1
        for j in range(0, n - i - 1):
            t += 1
            if arr[j] > arr[j + 1]:
                t += 1
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                t += 1
    return t

def quick_sort(arr):
    t = 0

    def quick_sort_helper(arr, low, high):
        nonlocal t
        t_local = 0
        t_local += 1
        if low < high:
            t_local += 1
            pivot_index, t_partition = partition(arr, low, high)
            t_local += t_partition
            t_local += quick_sort_helper(arr, low, pivot_index - 1)
            t_local += quick_sort_helper(arr, pivot_index + 1, high)
        return t_local

    def partition(arr, low, high):
        nonlocal t
        t_local = 0
        pivot = arr[high]
        t_local += 1
        i = low - 1
        t_local += 1
        for j in range(low, high):
            t_local += 1
            if arr[j] < pivot:
                t_local += 1
                i += 1
                t_local += 1
                arr[i], arr[j] = arr[j], arr[i]
                t_local += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        t_local += 1
        return i + 1, t_local

    t = quick_sort_helper(arr, 0, len(arr) - 1)
    return t

def counting_sort(arr):
    k = max(arr)
    t = 0
    t += 1
    if len(arr) == 0:
        t += 1
        return t

    count = [0] * (k + 1)
    t += 1
    output = [0] * len(arr)
    t += 1

    for num in arr:
        t += 1
        count[num] += 1
        t += 1

    for i in range(1, len(count)):
        t += 1
        count[i] += count[i - 1]
        t += 1

    for num in reversed(arr):
        t += 1
        output[count[num] - 1] = num
        t += 1
        count[num] -= 1
        t += 1

    for i in range(len(arr)):
        t += 1
        arr[i] = output[i]
        t += 1

    return t

def selection_sort(arr):
    t = 0
    n = len(arr)
    t += 1
    for i in range(n):
        t += 1
        min_index = i
        t += 1
        for j in range(i + 1, n):
            t += 1
            if arr[j] < arr[min_index]:
                t += 1
                min_index = j
                t += 1
        arr[i], arr[min_index] = arr[min_index], arr[i]
        t += 1
    return t

def shell_sort(arr):
    t = 0
    n = len(arr)
    t += 1
    gap = n // 2
    t += 1
    while gap > 0:
        t += 1
        for i in range(gap, n):
            t += 1
            temp = arr[i]
            t += 1
            j = i
            t += 1
            while j >= gap and arr[j - gap] > temp:
                t += 1
                arr[j] = arr[j - gap]
                t += 1
                j -= gap
                t += 1
            arr[j] = temp
            t += 1
        gap //= 2
        t += 1
    return t

def radix_sort(arr):
    t = 0
    t += 1
    if not arr:
        t += 1
        return t

    max_val = max(arr)
    t += 1
    exp = 1
    t += 1
    while max_val // exp > 0:
        t += 1
        t_counting = counting_sort_by_digit(arr, exp)
        t += t_counting
        exp *= 10
        t += 1
    return t

def counting_sort_by_digit(arr, exp):
    t = 0
    n = len(arr)
    t += 1
    output = [0] * n
    t += 1
    count = [0] * 10
    t += 1

    for i in range(n):
        t += 1
        index = (arr[i] // exp) % 10
        t += 1
        count[index] += 1
        t += 1

    for i in range(1, 10):
        t += 1
        count[i] += count[i - 1]
        t += 1

    i = n - 1
    t += 1
    while i >= 0:
        t += 1
        index = (arr[i] // exp) % 10
        t += 1
        output[count[index] - 1] = arr[i]
        t += 1
        count[index] -= 1
        t += 1
        i -= 1
        t += 1

    for i in range(n):
        t += 1
        arr[i] = output[i]
        t += 1
    return t

def bucket_sort(arr):
    t = 0
    t += 1
    if len(arr) == 0:
        t += 1
        return t

    bucket_count = 10
    t += 1
    min_val = min(arr)
    t += 1
    max_val = max(arr)
    t += 1
    bucket_range = (max_val - min_val + 1) / bucket_count
    t += 1

    buckets = [[] for _ in range(bucket_count)]
    t += 1
    for num in arr:
        t += 1
        index = int((num - min_val) // bucket_range)
        t += 1
        buckets[index].append(num)
        t += 1

    arr.clear()
    t += 1
    for bucket in buckets:
        t += 1
        t_insertion = insertion_sort(bucket) # Use a more C-like insertion sort
        t += t_insertion
        arr.extend(bucket)
        t += 1

    return t

# Array of sorting functions (without helper functions)
sorting_functions = [
    insertion_sort,
    merge_sort,
    heap_sort,
    bubble_sort,
    quick_sort,
    counting_sort,
    selection_sort,
    shell_sort,
    radix_sort,
    bucket_sort
]    

data_options = ["Custom Data", "Best Case", "Worst Case", "Random Data"]

growth_functions = ["n", "nlogn", "n^2", "2^n"]

def createGrowthCSV(growth_index):
    global n,step,results   
    values = []
    growth_function = growth_functions[growth_index]
    
    # Create values based on the selected growth function
    for i in range(1, n+1, step):
        if growth_function == "n":
            values.append([i, i])
        elif growth_function == "nlogn":
            values.append([i, i * math.log(i, 2)])
        elif growth_function == "n^2":
            values.append([i, i**2])
        elif growth_function == "2^n":
            values.append([i, 2**i])

    growth_values = np.array(values)
    results_array = np.array(results)
    
    if len(results_array) != len(growth_values):
        raise ValueError(f"The length of results{len(results_array)} and growth_values{len(growth_values)} must match.")
    
    # Calculate scaling factors
    scaling_factors = results_array[1:] / growth_values[1:]
    scaling_factors = scaling_factors[:, 1]

    # Focus on large n values to determine the scaling factor (asymptotic behavior)
    critical_n_start = int(len(scaling_factors) * 0.2)  # Start from the middle of the values
    large_n_scaling_factors = scaling_factors[critical_n_start:]
    
    # Find the minimum and maximum scaling factors (c1 and c2) over large n range
    c1 = np.min(large_n_scaling_factors)  # Lower bound constant
    c2 = np.max(large_n_scaling_factors)  # Upper bound constant

    # Calculate lower and upper bounds for f(n) using c1 and c2
    lower_values = [[i, value * c1] for i, value in values]
    upper_values = [[i, value * c2] for i, value in values]
    
    # Generate CSV files for the lower and upper bounds
    generate_csv(lower_values, f"growth_{growth_function}_lower.csv")
    generate_csv(upper_values, f"growth_{growth_function}_upper.csv")

    # Print the constants c1 and c2 for verification
    print(f"Lower bound constant (c1): {c1}")
    print(f"Upper bound constant (c2): {c2}")
    
    return c1, c2

def calculateTime(function, index):
  global n
  global step
  n_values = list(range(1, n+1, step))  # Different array sizes
  global results
  global number
  results = []
  for n in n_values:
      data_option = data_options[index]

      is_quicksort = (function == quick_sort)

      if data_option == "Custom Data":
            arr = custom.copy()[0:n]      
      elif data_option == "Best Case":
          arr = sortedRange(n) if not is_quicksort else generate_best_case_array(n)
      elif data_option == "Worst Case":
          arr = reverseSortedRange(n) if not is_quicksort else sortedRange(n)
      else:  # data_option == "Random Data"
          arr = random_arr(n)


      exectime = function(arr)

      if n == n_values[len(n_values) - 1] and data_option == "Custom Data":
        global customfilepath
        filename = os.path.basename(customfilepath)
        generate_csv([[i] for i in arr], filename.replace('.csv', f'_sorted.csv').replace('.xlsx', f'_sorted.csv'))
      
      results.append((n, exectime))

  # Generate CSV file
  filename = f"{function.__name__}_{data_option.replace(' ', '_')}.csv"
  if data_option == "Custom Data":
      filename = f"{function.__name__}_{data_option.replace(' ', '_')}_{number}.csv"
  generate_csv(results, filename)
