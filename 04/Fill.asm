// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
 
(INF)
    @i
    M = -1

    @KBD            //0 no pinta ........... diferente 0 pinta
    D = M
    @BLANCO
    D, JEQ          // D == 0 SALTA .......... si  D != 0 sigue abajo


(NEGRO)
    @i
    M = M + 1 
    D = M      
    
    @SCREEN
    A = A + D
    M = -1

    @i
    D = M
    @8191
    D = A - D

    @NEGRO
    D; JGT  

    @INF
    0; JMP


(BLANCO)    
    @i
    M = M + 1 
    D = M      
    
    @SCREEN
    A = A + D
    M = 0

    @i
    D = M
    @8191
    D = A - D

    @BLANCO
    D; JGT  // 0

    @INF
    0; JMP

