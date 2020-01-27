#ifndef _VSCODE_SDCC_H
#define _VSCODE_SDCC_H
/*
    There is currently no support for sdcc syntax (Intellisense) in VScode.
    These defines will limit the number of reported errors due to undecognized
    sdcc keywords like __code, __at etc.
    The trick is, when editing the code in VScode, the SDCC is not defined, 
    it happens only at compile time. So we can use the "#ifndef SDCC" condition
    to redefine the sdcc keywords as empty and make the errors go away.
    When compiling, the SDCC is defined and the below redefinitions will not be
    included.

    Required only when working in VScode. 
*/
#ifndef SDCC
    #define __code
    #define __xdata
    #define __data
    #define __pdata
    #define __idata
    #define __at(x)
    #define __sbit
    #define __asm
    #define __endasm
    #define __interrupt
    #define __using
    #define bool uint8_t    // with no SDCC defined, compiler.h will need bool 
#endif

#endif // _VSCODE_SDCC_H
