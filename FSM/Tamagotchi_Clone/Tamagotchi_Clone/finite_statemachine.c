#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>
#include "avr.h"
#include "lcd.h"
#include "keypad.h"
/*
Hi Doug. The idea behind this is the tamagotchi runs like a normal 
game, where we have a refresh rate, and make decisions based on data 
in a frame. This code is what I sent to a partner before we worked 
together and finished the whole thing. So, it is basically the skeleton
of the project, before we implemented all the games. You can see the FSM I 
created below, and all the notes I sent my partner, before we finished it.
The various functions you see, like wait_avr(), puts_lcd2() are tools 
created to interface with the various hardware components, like the CPU
LED, and keyboard. 
*/

#define second 1000 //runs in Miliseconds

//This will be the refresh rate. How fast the game moves. Make 
//sure seconds is divisible by Hz.

#define Hz 4

#define parts second/Hz

//Sensitivity of button presses: Basically Latency. How 
//many button presses we sense per refresh
//Important: make sure parts is divisible by Latency.

#define Latency 10

//what we put into wait_avr().
unsigned int wait = parts / Latency;

//how long it takes for a day to end
char day_ends = 60;
//how long the games are
char end_game = 30;

//print buffer
char buffer[16];

enum tama_States { init, tama_menu, SS_menu, JG_menu, WM_menu, SS_GL, JG_GL, WM_GL, death } tama_State;
void clearBuffer();
int main(void){
	//Moore finite state machine. The variables below are things
	//the machine needs to remember after every loop.
	tama_State = init;
	char restart = 1;
	char Status;
	char Hunger;
	char Mood;
	char in_Game = 0; //boolean
	char frame = 0; //For games. Do stuff after a certain amount

	char key = 100;
	int refresh = 0; //display when refresh == Latency
	char seconds_menu = 0;
	char seconds_game = 0;
	char until_Hz = 0; //seconds++ when until_Hz == Hz
	char win = 1;
	
	char needTimeStamp = 1;
	char gameTimeStamp = 0;
	char untilHzTimeStamp = 0;
	
	
	//SS vars
	int randNum1 = 0;
	int randNum2 = 0;
	int expectedResult = 0;
	
	ini_lcd();
	clr_lcd();
	while(restart){
		//This switch is for doing actions.
		switch(tama_State){
			
			case init:
				key = 'Z';
				refresh = 0;
				clr_lcd();
				Status = 100;
				Hunger = 100;
				Mood = 100;
				until_Hz = 0;
				seconds_menu = 0; //stores time while in menu so tamagotchi doesn't get hungry when playing game
				seconds_game = 0; //time spent in game/remaining in game
				in_Game = 0;
				frame = 0;
				win = 1;
				break;

			case tama_menu:
				//implement function for Status, Health, and Mood 
				//display
				
				Status = (Hunger * Mood)/100;
				
				pos_lcd(0,13);
				puts_lcd2("S");
				pos_lcd(0,14);
				clearBuffer();
				sprintf(buffer,"%02d",seconds_menu);
				puts_lcd2(buffer);
				
				if(refresh == 0){
					clr_lcd();
					//display here
					//this is the temp start
					until_Hz++;
					frame++;
					frame = frame % 2; //temporary, for testing
					if(frame == 1){
						pos_lcd(0,6);
						puts_lcd2("(:>)");
					}
					if(frame == 0){
						pos_lcd(0,6);
						puts_lcd2("(<:)");
					}
					pos_lcd(1,0);
					clearBuffer();
					sprintf(buffer,"S%03d H%03d M%03d  ",(int)Status,(int)Hunger,(int)Mood);
					puts_lcd2(buffer);
					pos_lcd(0,13);
					puts_lcd2("S");
					pos_lcd(0,14);
					clearBuffer();
					sprintf(buffer,"%02d",seconds_menu);
					puts_lcd2(buffer);
				}
				if(until_Hz == Hz){
					//determines when a second has passed
					Hunger--;
					seconds_menu++;
					until_Hz = 0;
				}
				if(day_ends == seconds_menu){
					Mood-=10;
					seconds_menu = 0;
					//do stuff if we want to when the day ends.
				}
				break;

			case SS_menu:
				needTimeStamp = 1;
				seconds_game = 0;
				clr_lcd();
				pos_lcd(0,0);
				puts_lcd2("Simon Says!");
				pos_lcd(1,0);
				puts_lcd2("Get Ready");
				break;

			case JG_menu:
				seconds_game = 0;
				clr_lcd();
				pos_lcd(0,0);
				puts_lcd2("Dodge the Star!");
				pos_lcd(1,0);
				puts_lcd2("Get Ready");
				break;
			
			case WM_menu:
				seconds_game = 0;
				clr_lcd();
				pos_lcd(0,0);
				puts_lcd2("Wacka Mole!");
				pos_lcd(1,0);
				puts_lcd2("Get Ready");
				break;

			case SS_GL: //Simon Says
				//decide whether or not to do stuff during frames or 
				//seconds. Preferably frames.
				in_Game = 1;
				//initialize game
				if (needTimeStamp){
					untilHzTimeStamp = until_Hz;
					gameTimeStamp = seconds_game;
					needTimeStamp = 0;
					key = 'Z';
					clr_lcd();
					pos_lcd(0,0);
					clearBuffer();
					sprintf(buffer,"%s","Enter the Result");
					//puts_lcd2("Enter the Result");
				}
				
				else if (seconds_game == gameTimeStamp+1 && untilHzTimeStamp == until_Hz){
					randNum1 = rand() % 5;
					randNum2 = rand() % 6;
					
					expectedResult = randNum1 + randNum2;
					clr_lcd();
					pos_lcd(0,0);
					clearBuffer();
					sprintf(buffer,"%d+%d",randNum1,randNum2);
				} 

				else if ((seconds_game == gameTimeStamp+3 && untilHzTimeStamp == until_Hz) || key != 'Z'){
					switch(expectedResult){
						case 0:
						if (key != '0'){
							win = 0;
						}
						break;
						case 1:
						if (key != '1'){
							win = 0;
						}
						break;
						case 2:
						if (key != '2'){
							win = 0;
						}
						break;
						case 3:
						if (key != '3'){
							win = 0;
						}
						break;
						case 4:
						if (key != '4'){
							win = 0;
						}
						break;
						case 5:
						if (key != '5'){
							win = 0;
						}
						break;
						case 6:
						if (key != '6'){
							win = 0;
						}
						break;
						case 7:
						if (key != '7'){
							win = 0;
						}
						break;
						case 8:
						if (key != '8'){
							win = 0;
						}
						break;
						case 9:
						if (key != '9'){
							win = 0;
						}
						break;
						default:
						win = 1;
						break;
					}
					needTimeStamp = 1;
				}

				
				if(refresh == 0){
					//clr_lcd();
					//create new frame and do stuff. Logic here if you 
					//want to change every frame.
					
					puts_lcd2(buffer);
					pos_lcd(1,14);
					clearBuffer();
					sprintf(buffer,"%02d",seconds_game);
					puts_lcd2(buffer);
					until_Hz++;
					frame++;
				}
				if(until_Hz == Hz){
					//Logic here if you want to change every second.
					seconds_game++;
					until_Hz = 0;
				}
				
				if(!win){ //game ends only if player loses or game times out
					win = 1;
					in_Game = 0;
					clr_lcd();
					pos_lcd(0,0);
					puts_lcd2("You lose");
					wait_avr(second);
					Mood-=5;
					//needTimeStamp = 1;
					//change variables of tamagotchi
				}
				if(seconds_game == end_game){ //game times out
					in_Game = 0;
					Mood++;
					//needTimeStamp = 1;
					//change variables of tamagotchi
				}
				break;

			case JG_GL: //Dodge the Star
				//decide whether or not to do stuff during frames or 
				//seconds. Preferably frames.

				//keeps the FSM from switching back to the menu
				in_Game = 1;
				clr_lcd();
				pos_lcd(0,0);
				puts_lcd2("JGGL");
				wait_avr(second);
				win = 0;
				if(refresh == 0){
					//create new frame and do stuff. Logic here if you 
					//want to change every frame.
					until_Hz++;
					frame++;
				}
				if(until_Hz == Hz){
					//Logic here if you want to change every second.
					seconds_game++;
					until_Hz = 0;
				}
				if(!win){
					win = 1;
					in_Game = 0;
					//change variables of tamagotchi
				}
				if(seconds_game == end_game){
					in_Game = 0;
					//change variables of tamagotchi
				}
				break;

			case WM_GL: //Whack-a-mole
				//decide whether or not to do stuff during frames or 
				//seconds. Preferably frames.

				//keeps the FSM from switching back to the menu
				in_Game = 1;
				clr_lcd();
				pos_lcd(0,0);
				puts_lcd2("WMGL");
				wait_avr(second);
				win = 0;
				if(refresh == 0){
					clr_lcd();
					//create new frame and do stuff. Logic here if you 
					//want to change every frame.
					until_Hz++;
					frame++;
				}
				if(until_Hz == Hz){
					//Logic here if you want to change every second.
					seconds_game++;
					until_Hz = 0;
				}
				if(!win){
					win = 1;
					in_Game = 0;
					//change variables of tamagotchi
				}
				if(seconds_game == end_game){
					in_Game = 0;
					//change variables of tamagotchi
				}
				break;

			case death:
				//ask player if they want to restart. 
				//so far set to 1 if restart is accepted.
				clearBuffer();
				sprintf(buffer,"%s","Press 1 to restart");
				clr_lcd();
				pos_lcd(0,0);
				puts_lcd2(buffer);
				/*
				pos_lcd(0,0);
				clr_lcd();
				puts_lcd2("1 to Restart");
				pos_lcd(1,0);
				puts_lcd2("0 to Quit");
				*/
				break;
		}
		

		//This switch is for changing states.
		switch(tama_State){
			case init:
				tama_State = tama_menu;

			case tama_menu:
				if(Status == 0){
					tama_State = death;
				}
				else if(key == 'A'){
					tama_State = SS_menu;
				}
				else if(key == 'B'){
					tama_State = JG_menu;
				}
				else if(key == 'C'){
					tama_State = WM_menu;
				}
				else{
					tama_State = tama_menu;
				}

				break;

			case SS_menu:
				wait_avr(second*2);
				tama_State = SS_GL;
				break;

			case JG_menu:
				wait_avr(second*2);
				tama_State = JG_GL;
				break;
			
			case WM_menu:
				wait_avr(second*2);
				tama_State = WM_GL;
				break;

			case SS_GL:
				if(!in_Game){
					tama_State = tama_menu;
				}
				else{
					tama_State = SS_GL;
				}
				break;
				
			case JG_GL:
				if(!in_Game){
					tama_State = tama_menu;
				}
				else{
					tama_State = JG_GL;
				}
				break;
				
			case WM_GL:
				if(!in_Game){
					tama_State = tama_menu;
				}
				else{
					tama_State = WM_GL;
				}
				break;
			case death:
				if(key == '0')
					return 0;
				else if(key == '1')
					tama_State = init;
				else
					tama_State = death;
				break;
		}

		wait_avr(wait);
		key = get_char();

		//increment refresh. When 0, we will refresh in SM
		refresh++;
		refresh = refresh % Latency;
	}
}
void clearBuffer(){
	for (int i = 0; i < 16; i++){
		buffer[i] = ' ';
	}
}