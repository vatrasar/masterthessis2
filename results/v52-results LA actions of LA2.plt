#set style data lines
set xrange [0:30000]
set yrange [0:300]
set xlabel "time"
set ylabel "dr 2-actions"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:26 with lines lc 2 lw 3 title "LA 2: action 2",\
'results_LA.txt' using 2:29 with lines lc 5 lw 3 title "LA 2: action 5",\
'results_LA.txt' using 2:30 with lines lc 4 lw 3 title "LA 2: action 6",\
'results_LA.txt' using 2:31 with lines lc 7 lw 7 title "LA 2: action 7",\
'results_LA.txt' using 2:34 with lines lc 1 lw 3 title "LA 2: action 10"







