#set style data lines
set xrange [0:30000]
set yrange [0:100]
set xlabel "time"
set ylabel "drons energy spending"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:9 with lines lc 7 title "dr 1: energy spend",\
'results_LA.txt' using 2:13 with lines lc 2 title "dr 2: energy spend"

#'results.txt' using 1:10 with impulses lc 2 title "dr 2: rew",\
#'results.txt' using 1:11 with lines lc 9 title "dr 2: sum of rew"




