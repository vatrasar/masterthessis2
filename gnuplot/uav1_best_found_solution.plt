set style data lines
set xlabel "Iteracje"
set ylabel "Średnia najlepsza wartosc funkcji"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'uav1_best_found_solution_data.txt' using 1:2:3 with yerrorbars lc 4 title "odchylenie standardowe",\
 'uav1_best_found_solution_data.txt' using 1:2 with lines lc 4 lw 3 title "Maksymalna uzyskana liczba punktów",\
 'uav1_best_found_solution_data.txt' using 1:4 with lines lc 7 lw 3 title "Maksymalna liczba punktów do zdobycia"
pause -1 "Hit any key to continue"