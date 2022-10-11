#set style data lines
set xrange [0:30000]
set yrange [0:32500]
set xlabel "x"
set ylabel "sum intr energy spending"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'results_LA.txt' using 2:18 with lines lc 4 title "sum of intr energy",\
'results_LA.txt' using 2:19 with lines lc 6 title "max intr energy"




