#include<stdio.h>
 int count = 0;
  void toh(int n, char from, char to, char aux){
    if (n == 1) { 
        // printf("Movefrom %c to %c using aux %c\n", from, to, aux);
         count++; 
         } else{ 
            toh(n-1, from, aux, to);
             toh(1,from, to, aux);
toh(n - 1, aux, to, from);
}
}
int main()
{
    int n;
    printf("Enter number of rings - \n");
    scanf("%d", &n);
    toh(n, 'A', 'C', 'B');
    printf("count - %d", count);
}