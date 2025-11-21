# SimpleDay
This is a custom coding language/esolang that is built around python. It is also called SD by me, cause of course I'm too lazy to spell SimpleDay.  
_____________________________________________________________________
#### To Use SimpleDay  
If you want to download the python interpreter from the website for use, you download the file, and put it into your system's `PATH`  

If you want to use git, you can do the following on the line below:  
```bash
git clone https://github.com/Error404-linux/SimpleDay.git
```
To run a file, you need to have a .day extension, and run the file with it.  
______________________________________________________________________
#### To code in SimpleDay
This code language is symbolic and is right-handed (sorry for you left-handed users)  

`/` | This represents a letter by count. `/ = a`, `// = b`, etc. This sets a character into the cell.  
`n` | This represents a number by count. `n = 1`, `nn = 2`, etc. This sets a number into the cell.  
`[ or ]` | This changes the cell by one, no matter what. Can be used to create variables.  
`\` | Backslashes can be chained up to 3. 1 of `\` prints the current cell, 2 of these `\` make a space and 3 makes a newline.   
`.` | This converts a number to a letter starting at a and yes, if you use a negative number, it will lower it by that number.  
`;` | The semicolon asks for an input, so please give it one, else it will hate you...  
`$` | This sign makes a comment. Why `$` instead of `#`? yes.  
`_` | This converts a number represented by n negative, or a character represented by / captial. Examples, `_n = -1`, `_/ = A`.  
`o/p` | This creates a comparison with a number stated to the current cell. o is <, p is >. e.g. `o2`, `p3`. Can also be used with cell data like [0] to get the value in cell 0  
`+/-` | The `+` sign __ADDS__ 1 to the cell. The `-` sign __SUBTRACTS__ 1 from the cell.  
`<N/C...>` | These 2 symbols `<` and `>` create loops, set by a number or cell at the start of a loop. `[1]` gets the value of cell 1 as the times it has to loop, and 1 makes the loop loops once. e.g. `<1+\>`, `<[0]+>\`  
`p/...p\` | This uses embedded python possible, though limited.  
`m/...m\` | This uses math. e.g. `m/[0]*4m\`. What this does is it gets the value of cell 0 * 4  

_______________________________________________________________________________

###### Examples  
```
[;\]
m/[1]*4m\
\
```
_____________________________________________________________________________________
#### Hope you enjoy this coding language, give it a star if you like it.
