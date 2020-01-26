#ifndef __UTIL_H__
#define __UTIL_H__
#include <stdio.h>
#if 1
#define DEBUG_OUT(...) printf(__VA_ARGS__);
#else
#define DEBUG_OUT(...) (void)0;
#endif

void initClock();
void delayUs(unsigned short n);
void delay(unsigned short n);

typedef void(* __data FunctionReference)();
extern FunctionReference runBootloader;

#endif
