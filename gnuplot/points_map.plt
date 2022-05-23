set style data lines
set xlabel "cm"
set ylabel "Najlepsza wartośc punktowa uzyskana ze strefy"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'points_map.txt' using 1:2:3 with yerrorbars lc 4 title "odchylenie standardowe",\
 'points_map.txt' using 1:2 with lines lc 4 lw 3 title "wartość punktowa",\
 'points_map.txt' using 1:4 with lines lc 6 lw 3 title "Wartość maksymalna"
pause -1 "Hit any key to continue"
