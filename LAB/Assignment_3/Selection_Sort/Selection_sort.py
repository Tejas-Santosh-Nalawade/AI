def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):  
        min_value = i;
        for j in range (i+1, n):
            if arr[j] < arr[min_value]:    
                min_value = j
        arr[i], arr[min_value] = arr[min_value] , arr[i]

def print_array(arr):
    for val in arr:
        print(val, end=" ")
    print()

if __name__ == "__main__":
    arr=[54,89,12,17,58]
    print("Original Array: ", end="")

    print_array(arr)

    selection_sort(arr)

    print("Sorted Array: ", end="")

    print_array(arr) 