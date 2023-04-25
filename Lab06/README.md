# Lab 06 Program Security Detect  
### 311554046 林愉修  

## Compiler Version  
```
$ gcc --version
gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```  

## Part I.  
> 下面是常見的記憶體操作問題，請分別寫出有下列記憶體操作問題的簡單程式，並說明 Valgrind 和 ASan 能否找的出來  
Heap out-of-bounds read/write
Stack out-of-bounds read/write
Global out-of-bounds read/write
Use-after-free
Use-after-return

### Heap out-of-bounds read/write  
#### Code  
```c
int main() {
    int *x = (int *)malloc(5 * sizeof(int));
    x[5] = 1;
    printf("%d\n", x[5]);
    free(x);

    return 0;
}
```
#### ASan report  
```
$ gcc heap_oob.c -fsanitize=address
$ ./a.out
=================================================================
==91926==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000000054 at pc 0x5625471712a2 bp 0x7ffec9fd9c40 sp 0x7ffec9fd9c30
WRITE of size 4 at 0x603000000054 thread T0
    #0 0x5625471712a1 in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x12a1)
    #1 0x7f7585a29d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f7585a29e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x562547171184 in _start (/home/eric/311554046-ST-2023/Lab06/a.out+0x1184)

0x603000000054 is located 0 bytes to the right of 20-byte region [0x603000000040,0x603000000054)
allocated by thread T0 here:
    #0 0x7f7585eb4867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x56254717125e in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x125e)
    #2 0x7f7585a29d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/eric/311554046-ST-2023/Lab06/a.out+0x12a1) in main
Shadow bytes around the buggy address:
  0x0c067fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c067fff8000: fa fa 00 00 00 fa fa fa 00 00[04]fa fa fa fa fa
  0x0c067fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==91926==ABORTING
```  
#### Valgrind report
```
$ gcc heap_oob.c
$ valgrind ./a.out
==92394== Memcheck, a memory error detector
==92394== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==92394== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==92394== Command: ./a.out
==92394== 
==92394== Invalid write of size 4
==92394==    at 0x1091AB: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==92394==  Address 0x4a9f054 is 0 bytes after a block of size 20 alloc'd
==92394==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==92394==    by 0x10919E: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==92394== 
==92394== Invalid read of size 4
==92394==    at 0x1091B9: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==92394==  Address 0x4a9f054 is 0 bytes after a block of size 20 alloc'd
==92394==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==92394==    by 0x10919E: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==92394== 
1
==92394== 
==92394== HEAP SUMMARY:
==92394==     in use at exit: 0 bytes in 0 blocks
==92394==   total heap usage: 2 allocs, 2 frees, 1,044 bytes allocated
==92394== 
==92394== All heap blocks were freed -- no leaks are possible
==92394== 
==92394== For lists of detected and suppressed errors, rerun with: -s
==92394== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```  

ASan 能, Valgrind 能  

### Stack out-of-bounds read/write  
#### Code  
```c
int main() {
    int x[3];
    x[3] = 3;
    printf("%d\n", x[3]);

    return 0;
}
```  
#### ASan report  
```
$ gcc stack_oob.c -fsanitize=address
$ ./a.out
=================================================================
==68055==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffd9786681c at pc 0x555dc3c272e7 bp 0x7ffd978667e0 sp 0x7ffd978667d0
WRITE of size 4 at 0x7ffd9786681c thread T0
    #0 0x555dc3c272e6 in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x12e6)
    #1 0x7f0777a29d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f0777a29e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x555dc3c27164 in _start (/home/eric/311554046-ST-2023/Lab06/a.out+0x1164)

Address 0x7ffd9786681c is located in stack of thread T0 at offset 44 in frame
    #0 0x555dc3c27238 in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x1238)

  This frame has 1 object(s):
    [32, 44) 'x' (line 5) <== Memory access at offset 44 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/eric/311554046-ST-2023/Lab06/a.out+0x12e6) in main
Shadow bytes around the buggy address:
  0x100032f04cb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0x100032f04cc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04cd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04ce0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04cf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1
=>0x100032f04d00: f1 f1 00[04]f3 f3 00 00 00 00 00 00 00 00 00 00
  0x100032f04d10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04d20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04d30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04d40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100032f04d50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==68055==ABORTING
```  
#### Valgrind report  
```
$ gcc stack_oob.c
$ valgrind ./a.out
==84446== Memcheck, a memory error detector
==84446== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==84446== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==84446== Command: ./a.out
==84446== 
*** stack smashing detected ***: terminated
==84446== 
==84446== Process terminating with default action of signal 6 (SIGABRT)
==84446==    at 0x490AA7C: __pthread_kill_implementation (pthread_kill.c:44)
==84446==    by 0x490AA7C: __pthread_kill_internal (pthread_kill.c:78)
==84446==    by 0x490AA7C: pthread_kill@@GLIBC_2.34 (pthread_kill.c:89)
==84446==    by 0x48B6475: raise (raise.c:26)
==84446==    by 0x489C7F2: abort (abort.c:79)
==84446==    by 0x48FD6F5: __libc_message (libc_fatal.c:155)
==84446==    by 0x49AA769: __fortify_fail (fortify_fail.c:26)
==84446==    by 0x49AA735: __stack_chk_fail (stack_chk_fail.c:24)
==84446==    by 0x1091BC: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==84446== 
==84446== HEAP SUMMARY:
==84446==     in use at exit: 1,024 bytes in 1 blocks
==84446==   total heap usage: 1 allocs, 0 frees, 1,024 bytes allocated
==84446== 
==84446== LEAK SUMMARY:
==84446==    definitely lost: 0 bytes in 0 blocks
==84446==    indirectly lost: 0 bytes in 0 blocks
==84446==      possibly lost: 0 bytes in 0 blocks
==84446==    still reachable: 1,024 bytes in 1 blocks
==84446==         suppressed: 0 bytes in 0 blocks
==84446== Rerun with --leak-check=full to see details of leaked memory
==84446== 
==84446== For lists of detected and suppressed errors, rerun with: -s
==84446== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
[1]    84446 IOT instruction (core dumped)  valgrind ./a.out
```  

ASan 能, Valgrind 不能  

### Global out-of-bounds read/write  
#### Code  
```c
int x[10];
int main() {
    x[10] = 1;
    printf("%d\n", x[10]);

    return 0;
}
```  
#### ASan report  
```
$ gcc global_oob.c -fsanitize=address
$ ./a.out
=================================================================
==88195==ERROR: AddressSanitizer: global-buffer-overflow on address 0x55a00a5bc108 at pc 0x55a00a5b9223 bp 0x7fff3255b7a0 sp 0x7fff3255b790
WRITE of size 4 at 0x55a00a5bc108 thread T0
    #0 0x55a00a5b9222 in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x1222)
    #1 0x7f808a429d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f808a429e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55a00a5b9124 in _start (/home/eric/311554046-ST-2023/Lab06/a.out+0x1124)

0x55a00a5bc108 is located 0 bytes to the right of global variable 'x' defined in 'global_oob.c:4:5' (0x55a00a5bc0e0) of size 40
SUMMARY: AddressSanitizer: global-buffer-overflow (/home/eric/311554046-ST-2023/Lab06/a.out+0x1222) in main
Shadow bytes around the buggy address:
  0x0ab4814af7d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af7e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af7f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af800: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9
  0x0ab4814af810: f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
=>0x0ab4814af820: 00[f9]f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x0ab4814af830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab4814af870: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==88195==ABORTING
```  
#### Valgrind report  
```
$ gcc global_oob.c
$ valgrind ./a.out
==89781== Memcheck, a memory error detector
==89781== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==89781== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==89781== Command: ./a.out
==89781== 
1==89781== 
==89781== HEAP SUMMARY:
==89781==     in use at exit: 0 bytes in 0 blocks
==89781==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==89781== 
==89781== All heap blocks were freed -- no leaks are possible
==89781== 
==89781== For lists of detected and suppressed errors, rerun with: -s
==89781== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```  

ASan 能, Valgrind 不能  

### Use-after-free  
#### Code  
```c
int main() {
    int *x = (int *)malloc(10 * sizeof(int));
    free(x);

    return x[5];
}
```  
#### ASan report   
```
$ gcc user_after_free.c -fsanitize=address
$ ./a.out
=================================================================
==93486==ERROR: AddressSanitizer: heap-use-after-free on address 0x604000000024 at pc 0x5606c56e322a bp 0x7fffa03cb000 sp 0x7fffa03caff0
READ of size 4 at 0x604000000024 thread T0
    #0 0x5606c56e3229 in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x1229)
    #1 0x7f2341629d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f2341629e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x5606c56e3104 in _start (/home/eric/311554046-ST-2023/Lab06/a.out+0x1104)

0x604000000024 is located 20 bytes inside of 40-byte region [0x604000000010,0x604000000038)
freed by thread T0 here:
    #0 0x7f2341ab4517 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x5606c56e31ee in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x11ee)
    #2 0x7f2341629d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

previously allocated by thread T0 here:
    #0 0x7f2341ab4867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x5606c56e31de in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x11de)
    #2 0x7f2341629d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-use-after-free (/home/eric/311554046-ST-2023/Lab06/a.out+0x1229) in main
Shadow bytes around the buggy address:
  0x0c087fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c087fff8000: fa fa fd fd[fd]fd fd fa fa fa fa fa fa fa fa fa
  0x0c087fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==93486==ABORTING
```  
#### Valgrind report  
```
$ gcc use_after_free.c
$ valgrind --track_origins=yes ./a.out
==102744== Memcheck, a memory error detector
==102744== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==102744== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==102744== Command: ./a.out
==102744== 
==102744== Invalid read of size 4
==102744==    at 0x109193: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==102744==  Address 0x4a9f054 is 20 bytes inside a block of size 40 free'd
==102744==    at 0x484B27F: free (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==102744==    by 0x10918E: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==102744==  Block was alloc'd at
==102744==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==102744==    by 0x10917E: main (in /home/eric/311554046-ST-2023/Lab06/a.out)
==102744== 
==102744== 
==102744== HEAP SUMMARY:
==102744==     in use at exit: 0 bytes in 0 blocks
==102744==   total heap usage: 1 allocs, 1 frees, 40 bytes allocated
==102744== 
==102744== All heap blocks were freed -- no leaks are possible
==102744== 
==102744== For lists of detected and suppressed errors, rerun with: -s
==102744== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```  

ASan 能, Valgrind 能  

### Use-after-return  
#### Code  
```c
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
```  
#### ASan report  
```
$ gcc use_after_return.c -fsanitize=address
$ ASAN_OPTIONS=detect_stack_use_after_return=1 ./a.out
=================================================================
==99962==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f30b02ae044 at pc 0x55f30a50a372 bp 0x7ffd7ededaf0 sp 0x7ffd7ededae0
WRITE of size 4 at 0x7f30b02ae044 thread T0
    #0 0x55f30a50a371 in main (/home/eric/311554046-ST-2023/Lab06/a.out+0x1371)
    #1 0x7f30b3829d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f30b3829e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55f30a50a144 in _start (/home/eric/311554046-ST-2023/Lab06/a.out+0x1144)

Address 0x7f30b02ae044 is located in stack of thread T0 at offset 68 in frame
    #0 0x55f30a50a218 in foo (/home/eric/311554046-ST-2023/Lab06/a.out+0x1218)

  This frame has 1 object(s):
    [48, 88) 'stack_buffer' (line 6) <== Memory access at offset 68 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return (/home/eric/311554046-ST-2023/Lab06/a.out+0x1371) in main
Shadow bytes around the buggy address:
  0x0fe69604dbb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dbc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dbd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dbe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dbf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe69604dc00: f5 f5 f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5
  0x0fe69604dc10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dc20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dc30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dc40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe69604dc50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==99962==ABORTING
```  
#### Valgrind report  
```
$ gcc use_after_return.c
$ valgrind ./a.out
==100450== Memcheck, a memory error detector
==100450== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==100450== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==100450== Command: ./a.out
==100450== 
==100450== 
==100450== HEAP SUMMARY:
==100450==     in use at exit: 0 bytes in 0 blocks
==100450==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==100450== 
==100450== All heap blocks were freed -- no leaks are possible
==100450== 
==100450== For lists of detected and suppressed errors, rerun with: -s
==100450== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```  

ASan 能, Valgrind 不能  

|                      |Valgrind|  ASan  |
|        :----:        | :----: | :----: |
| Heap out-of-bounds   |   O    |   O    |
| Stack out-of-bounds  |   X    |   O    |
| Global out-of-bounds |   X    |   O    |
| Use-after-free       |   O    |   O    |
| Use-after-return     |   X    |   O    |  


## Part II.
>  寫一個簡單程式 with ASan，Stack buffer overflow 剛好越過 redzone(並沒有對 redzone 做讀寫)，並說明 ASan 能否找的出來？  

### Code  
```c
int main() {
    int a[8];
    int b[8];

    a[16] = 123;
    printf("%d\n", b[0]);

    return 0;
}
```  
#### ASan report  
```
$ gcc across_redzone.c -fsanitize=address
$ ./a.out
123
```
明顯看到ASan是無法找出來的。
