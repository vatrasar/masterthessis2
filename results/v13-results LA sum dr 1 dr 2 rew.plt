#set style data lines
set xrange [0:30000]
set yrange [0:2200]
set xlabel "time"
set ylabel "reward sum dr 1, dr 2"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:8 with lines lc 7 title "dr 1: rew sum",\
'results_LA.txt' using 2:12 with lines lc 2 title "dr 2: rew sum"




