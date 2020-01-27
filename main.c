#ifndef FREQ_SYS
#define	FREQ_SYS	48000000
#endif 

#include <string.h>
#include <stdio.h>
#include "sdcc_int.h"
#include <stdint.h>
#include "vscode_sdcc.h"
#include "CH559.h"
#include "gpio.h"
#include "rndata.h"
// 4 leds on the electrodragon board, P14-P17
#define USE_EDRG_LEDS   

const uint8_t clrscr[]="\x1b[2J";

void initClock();

void delayUs(unsigned short n);
void delay(unsigned short n);
void initUART0(unsigned long baud, int alt);
void printStr(const uint8_t txt[]);

typedef void(* __data FunctionReference)();
FunctionReference runBootloader = (FunctionReference)0xF400;

#ifdef USE_EDRG_LEDS
    PORT_PIN(LED_1, 1, 4)
    PORT_PIN(LED_2, 1, 5)
    PORT_PIN(LED_3, 1, 6)
    PORT_PIN(LED_4, 1, 7)
    void initLeds();
    void setLeds(uint8_t value);
#endif

// -------------------------------------------------------------
void main()
{
    char buf[32];

    initClock();
#ifdef USE_EDRG_LEDS
        initLeds();
#endif 
    initUART0(115200, 0);   // TX on P3.1
    delay(10);
    printf(clrscr);

    uint16_t data_l = sizeof(data);

    printf("array size = %d bytes\r\n", data_l);
    const uint8_t txt[] = "1. printf(const uint8_t[]); // works! \r\n";
    printStr(txt);
    sprintf(buf, "%s", "2. sprintf works!\r\n");    
    printf(buf);
    printf("3. printf(\"string\"); // works!\r\n");

    uint8_t i;
    printf("\r\nlast 8 bytes of the data array:\r\n");
    for (i=0; i<8; i++)
    {
        uint16_t idx = data_l-8+i;
        printf("rndata[%d] = %d\r\n", idx, data[idx]);
    }

    delay(100);

    runBootloader();    // just go back to bootloader

    while(1)
    {
        if(!(P4_IN & (1 << 6)))
            runBootloader();
#ifdef USE_EDRG_LEDS
        setLeds(i++);
#endif 
        delay(1000);
    }
}
// -------------------------------------------------------------
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
// -------------------------------------------------------------
#ifdef USE_EDRG_LEDS
void initLeds()
{
    pin_LED_1_out();
    pin_LED_2_out();
    pin_LED_3_out();
    pin_LED_4_out();

    LED_1 = 0;
    LED_2 = 0;
    LED_3 = 0;
    LED_4 = 0;
}

void setLeds(uint8_t value)
{
    LED_1 = value & (1<<0);
    LED_2 = value & (1<<1);
    LED_3 = value & (1<<2);
    LED_4 = value & (1<<3);
}
#endif
// -------------------------------------------------------------
int putchar(int c)
{
    LED_1 = 1;
    while (!TI);
    TI = 0;
    SBUF = c & 0xFF;
    return c;
}
// -------------------------------------------------------------
int getchar() 
{
    while(!RI);
    RI = 0;
    return SBUF;
}
// -------------------------------------------------------------
/**
 * Initialize UART0 port with given boud rate
 * pins: tx = P3.1 rx = P3.0
 * alt != 0 pins: tx = P0.2 rx = P0.3
 */
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
// -------------------------------------------------------------
void printStr(const uint8_t string[])
{
    uint16_t bufIndex = 0u;
    while(string[bufIndex] != (uint8_t) 0)
    {
        putchar((uint8_t)string[bufIndex]);
        bufIndex++;
    }
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
