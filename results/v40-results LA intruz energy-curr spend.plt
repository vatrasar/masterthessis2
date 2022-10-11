#set style data lines
set xrange [0:30000]
set yrange [0:110]
set xlabel "x"
set ylabel "curr intr energy spending"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:23 with impulses lc 7 title "curr intr energy spend"

#'results.txt' using 1:16 with lines lc 4 title "sum of intr energy",\
#'results.txt' using 1:17 with lines lc 6 title "max intr energy"




