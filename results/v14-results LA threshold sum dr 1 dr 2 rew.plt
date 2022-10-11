#set style data lines
set xrange [0:30000]
set yrange [0:4000]
set xlabel "time"
set ylabel "thresh reward sum dr 1, dr 2"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:24 with lines lc 7 title "dr 1: thresh rew sum"

#'results_LA.txt' using 1:11 with lines lc 2 title "dr 2: rew sum"




