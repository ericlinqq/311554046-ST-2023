#include <stdlib.h>

int *x;

void foo() {
    int stack_buffer[10];
    x = &stack_buffer[5];
}

int main() {
    foo();
    *x = 123;

    return 0;    
}