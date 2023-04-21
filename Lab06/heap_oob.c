#include <stdlib.h>
#include <stdio.h>

int main() {
    int *x = (int *)malloc(5 * sizeof(int));
    x[5] = 1;
    printf("%d\n", x[5]);
    free(x);

    return 0;
}