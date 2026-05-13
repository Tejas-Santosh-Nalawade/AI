import java.util.Arrays;

class Selection_sort{
    static void Selection_sort(int [] arr){
        int n = arr.length;
        for(int i=0; i<n; i++){
            int min_val = i;

            for(int j= i+ 1; j<n; j++){
                if(arr[j] < arr[min_val]){
                    min_val = j;
                }
            }
            int temp = arr[i];
            arr[i] = arr[min_val];
            arr[min_val] = temp;
        }

    } 

    static void print_array(int [] arr){
        for(int val:arr){
            System.out.println(val + " ");
        }
        System.out.println();
    }

    public static void main (String[] args){
        int [] arg = {25,89,17,57,69};
        System.out.println("Original Array: ");
        print_array(arg);
        System.out.print("Sorted Array: ");
        Selection_sort(arg);
        print_array(arg);
    }
}