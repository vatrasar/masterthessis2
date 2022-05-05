set style data lines
set xlabel "Iteracje"
set ylabel "Średnia najlepsza wartosc funkcji"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'freqency_of_hits.txt' using 1:2:3 with yerrorbars lc 4 title "odchylenie standardowe",\
 'freqency_of_hits.txt' using 1:2 with lines lc 4 lw 3 title "Średnia liczba uderzeń"
pause -1 "Hit any key to continue"