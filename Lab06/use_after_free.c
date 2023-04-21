#include <stdlib.h>

int main() {
    int *x = (int *)malloc(10 * sizeof(int));
    free(x);

    return x[5];
}