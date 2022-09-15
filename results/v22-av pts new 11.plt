set style data lines
set xrange [0:5000]
set yrange [0:25]
set xlabel "iter"
set ylabel "av pts new"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'sa_results.txt' using 1:11 with lines lc 7 title "av pts new"
