#include "CH559.h"
#include "util.h"

FunctionReference runBootloader = (FunctionReference)0xF400;

#ifndef FREQ_SYS
#define	FREQ_SYS	48000000
#endif 

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
