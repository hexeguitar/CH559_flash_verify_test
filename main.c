typedef unsigned char *PUINT8;
typedef unsigned char __xdata *PUINT8X;
typedef const unsigned char __code *PUINT8C;
typedef unsigned char __xdata UINT8X;
typedef unsigned char  __data             UINT8D;

#ifndef FREQ_SYS
#define	FREQ_SYS	48000000
#endif 

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "CH559.h"
#include "rndata.h"

void initClock();
void delayUs(unsigned short n);
void delay(unsigned short n);
void initUART0(unsigned long baud, int alt);
int putchar(int c);
int getchar();

typedef void(* __data FunctionReference)();
FunctionReference runBootloader = (FunctionReference)0xF400;

void main()
{
    initClock();
    initUART0(115200, 1);
    
    printf("CH559 test\r\n");
    uint16_t data_l = sizeof(data);
    uint8_t i;
    for (i=0; i<8; i++)
    {
        uint16_t idx = data_l - i -1 ;
        printf("rndata[%d] = %d\r\n", idx, data[idx]);
    }

    delay(100);
    runBootloader();


    while(1)
    {
    }
}

void initClock()
{
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;

	CLOCK_CFG &= ~MASK_SYS_CK_DIV;
	CLOCK_CFG |= 6; 															  
	PLL_CFG = ((24 << 0) | (6 << 5)) & 255;

    SAFE_MOD = 0xFF;

	delay(7);
}

int putchar(int c)
{
    while (!TI);
    TI = 0;
    SBUF = c & 0xFF;
    return c;
}

int getchar() 
{
    while(!RI);
    RI = 0;
    return SBUF;
}


void initUART0(unsigned long baud, int alt)
{
	unsigned long x;
	if(alt)
	{
		PORT_CFG |= bP0_OC;
		P0_DIR |= bTXD_;
		P0_PU |= bTXD_ | bRXD_;
		PIN_FUNC |= bUART0_PIN_X;
	}

 	SM0 = 0;
	SM1 = 1;
	SM2 = 0;
	REN = 1;
   //RCLK = 0;
    //TCLK = 0;
    PCON |= SMOD;
    x = (((unsigned long)FREQ_SYS / 8) / baud + 1) / 2;

    TMOD = TMOD & ~ bT1_GATE & ~ bT1_CT & ~ MASK_T1_MOD | bT1_M1;
    T2MOD = T2MOD | bTMR_CLK | bT1_CLK;
    TH1 = (256 - x) & 255;
    TR1 = 1;
	TI = 1;
}


/*******************************************************************************
* Function Name  : delayUs(UNIT16 n)
* Description    : us
* Input          : UNIT16 n
* Output         : None
* Return         : None
*******************************************************************************/ 
void	delayUs(unsigned short n)
{
	while (n) 
	{  // total = 12~13 Fsys cycles, 1uS @Fsys=12MHz
		++ SAFE_MOD;  // 2 Fsys cycles, for higher Fsys, add operation here
#ifdef	FREQ_SYS
#if		FREQ_SYS >= 14000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 16000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 18000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 20000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 22000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 24000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 26000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 28000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 30000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 32000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 34000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 36000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 38000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 40000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 42000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 44000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 46000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 48000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 50000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 52000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 54000000
		++ SAFE_MOD;
#endif
#if		FREQ_SYS >= 56000000
		++ SAFE_MOD;
#endif
#endif
		--n;
	}
}

/*******************************************************************************
* Function Name  : delay(UNIT16 n)
* Description    : ms
* Input          : UNIT16 n
* Output         : None
* Return         : None
*******************************************************************************/
void delay(unsigned short n)
{
	while (n) 
	{
		delayUs(1000);
		--n;
	}
}
