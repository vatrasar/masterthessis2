#set style data lines
set xrange [0:30000]
set yrange [0:29000]
set xlabel "time"
set ylabel "drons sum energy spending"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:10 with lines lc 7 title "dr 1: sum energy spend",\
'results_LA.txt' using 2:14 with lines lc 2 title "dr 2: sum energy spend",\
'results_LA.txt' using 2:20 with lines lc 8 title "dr 2: uav max energy"

#'results.txt' using 2:11 with impulses lc 2 title "dr 2: rew",\
#'results.txt' using 2:12 with lines lc 9 title "dr 2: sum of rew"




