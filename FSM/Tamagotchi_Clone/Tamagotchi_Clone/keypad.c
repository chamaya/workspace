/*
 * keypad.c
 *
 * Created: 5/8/2016 1:26:43 PM
 *  Author: Alejandro Bustelo
 *			Christopher Amaya
 */ 

#include <avr/io.h>
#include "avr.h"
#include "keypad.h"

unsigned char decodedChar[17] = {'Z', '1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D'}; //Z means nothing pressed

unsigned char pressed(unsigned char r, unsigned char c){
	//initialize everything to zero
	DDRC = 0x00; //make all pins to input
	PORTC = 0xF0; //output 1's to all columns

	SET_BIT(DDRC, r); //make row to output
	CLR_BIT(PORTC, r); //make row zero
	
	SET_BIT(PORTC, c+4); //should set c'th column to z
	
	//wait_avr(1);
	
	if (GET_BIT(PINC, c+4)){ //return 1, nothing pressed
		return 0;
		}else{
		return 1;
	}
}

unsigned char get_key(){
	unsigned char r, c; //row, column
	for (r = 0; r < 4; ++r){
		for (c = 0; c < 4; ++c){
			if (pressed(r,c)){
				return ((r*4)+c+1); //reserve 0 for when nothing is pressed, return unique numbers
			}
		}
	}
	return 0;
}

unsigned char get_char(){
	unsigned char pressedChar = get_key();
	return decodedChar[pressedChar];
}
