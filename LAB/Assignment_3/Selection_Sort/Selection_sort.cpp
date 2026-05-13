#include<bits/stdc++.h>
using namespace std;


void selection_sort(vector<int>&arr){
    int n = arr.size();
    for(int i=0; i<n-1; i++){
        int min_val = i;
        for(int j=i+1; j<n; j++){
            if(arr[j] < arr[min_val]){
                min_val = j;
            }
        }
        swap(arr[i], arr[min_val]);
    }
}


void print_array(vector<int> arr){
    for(int i=0; i<arr.size(); i++){
        cout<<arr[i]<<" ";
    }
    cout<<"\n";
}

int main(){

    vector<int> arr = {64, 25, 12, 22, 11};
    cout<<"Original Array: "<<"\n";
    print_array(arr);

    selection_sort(arr);
    cout<<"Sorted Array"<<"\n";
    print_array(arr);


    return 0;
}