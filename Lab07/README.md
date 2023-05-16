# Lab07 Fuzz Testing  
### 311554046 林愉修  

## PoC: the file that can trigger the vulnerability  
Lab07/out/crashes/id:000000,sig:06,src:000000,op:flip1,pos:18  

## The commands (steps) that you used in this lab  
$ afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp  

## Screenshot of AFL running (with triggered crash)  
![AFL running](https://i.imgur.com/y3UErj7.png)  

## Screenshot of crash detail (with ASAN error report)  
![Crash detail](https://i.imgur.com/mLGpepg.png)  