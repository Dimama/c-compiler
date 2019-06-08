int arr[8] = {10, 10, 8, 9, 1, 2, 3, 0};
int n = 8;

void swap(int* a, int* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int partition (int low, int high)
{
    int pivot = arr[high];
    int i = (low - 1);

    int j = 0;
    for (j = low; j <= high- 1; j=j+1)
    {
        if (arr[j] <= pivot)
        {
            i=i+1;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}


void quickSort(int low, int high)
{
    if (low < high)
    {
	    int pi = 0;
        pi = partition(low, high);

        quickSort(low, pi - 1);
        quickSort(pi + 1, high);
    }
}

/* print array */
void printArray()
{
    int i;
    for (i=0; i < n; i=i+1)
    {
        print_int(arr[i]);
	    printstr(" ");
    }
    printstr("\n");
}

int main()
{
    printstr("Array: ");
    printArray();
    quickSort(0, n-1);
    printstr("Sorted array: ");
    printArray();
    return 0;
}

void print_int(int a){
	asm("li $v0 1");
	asm("syscall");
}