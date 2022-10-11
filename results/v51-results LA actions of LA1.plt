#set style data lines
set xrange [0:30000]
set yrange [0:300]
set xlabel "time"
set ylabel "dr 1-actions"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:25 with lines lc 1 lw 3 title "LA 1: action 1",\
'results_LA.txt' using 2:27 with lines lc 6 lw 3 title "LA 1: action 3",\
'results_LA.txt' using 2:29 with lines lc 5 lw 3 title "LA 1: action 5",\
'results_LA.txt' using 2:31 with lines lc 7 lw 3 title "LA 1: action 7",\
'results_LA.txt' using 2:33 with lines lc 3 lw 3 title "LA 1: action 9"







