#ifndef _GPIO_H
#define _GPIO_H

/**
 *  CH559 GPIO settings 
 *  An acrobatic macro way to generate functions to setup
 *  and access pins on Port0 to Port3.
 *  Not the most flash-wise efficient way, but convinient.
 *  Usage example:
 *  Let make a LED_1 on P10:
 *  PORT_PIN(LED_1, 1, 0)
 * 
 *  set the pin to output:
 *  pin_LED_1_out();
 * 
 *  control the pin:
 *  LED_1 = 1;
 *  LED_1 = 0;
 * 
 *  (c) 01-2020 by Piotr Zapart / hexefx.com
 */

#define PORT0_ADDR  0x80
#define PORT1_ADDR  0x90
#define PORT2_ADDR  0xA0
#define PORT3_ADDR  0xB0

#define PASTER(pinname, portaddr, bitnum) SBIT(pinname, portaddr, bitnum);
#define EVALUATOR(pinname, portnum, bitnum) PASTER(pinname, portnum, bitnum)
#define CREATE_SBIT(pinname, portnum, bitnum)   EVALUATOR(pinname, PORT##portnum##_ADDR, bitnum)

#define PORT_PIN(name, port, pin)                       \
    CREATE_SBIT(name, port, pin)                        \
    static inline void pin_##name##_in(void)            \
    {                                                   \
        PORT_CFG &= ~bP##port##_OC;                     \
        P##port##_DIR &= ~(1 << pin);                   \
        P##port##_PU &= ~(1 << pin);                    \
        (void)pin_##name##_in;                          \
    }                                                   \
    static inline void pin_##name##_in_pu(void)         \
    {                                                   \
        PORT_CFG &= ~bP##port##_OC;                     \
        P##port##_DIR &= ~(1 << pin);                   \
        P##port##_PU |= 1 << pin;                       \
        (void)pin_##name##_in_pu;                       \
    }                                                   \
    static inline void pin_##name##_out(void)           \
    {                                                   \
        PORT_CFG &= ~bP##port##_OC;                     \
        P##port##_DIR |= 1 << pin;                      \
        (void)pin_##name##_out;                         \
    }                                                   \
    static inline void pin_##name##_out_od(void)        \
    {                                                   \
        PORT_CFG |= bP##port##_OC;                      \
        P##port##_DIR &= ~(1 << pin);                   \
        P##port##_PU &= ~(1 << pin);                    \
        (void)pin_##name##_out_od;                      \
    }                                                   \
    static inline void pin_##name##_out_od2(void)       \
    {                                                   \
        PORT_CFG |= bP##port##_OC;                      \
        P##port##_DIR |= 1 << pin;                      \
        P##port##_PU &= ~(1 << pin);                    \
        (void)pin_##name##_out_od2;                     \
    }                                                   \
    static inline void pin_##name##_inout_pu(void)      \
    {                                                   \
        PORT_CFG |= bP##port##_OC;                      \
        P##port##_DIR &= ~(1 << pin);                   \
        P##port##_PU |= 1 << pin;                       \
        (void)pin_##name##_inout_pu;                    \
    }                                                   \
    static inline void pin_##name##_inout_pu2(void)     \
    {                                                   \
        PORT_CFG |= bP##port##_OC;                      \
        P##port##_DIR |= 1 << pin;                      \
        P##port##_PU |= 1 << pin;                       \
        (void)pin_##name##_inout_pu2;                   \
    }                                                   \

#endif // _GPIO_H
