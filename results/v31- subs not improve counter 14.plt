#set style data lines
set xrange [0:5500]
set yrange [0:5500]
set xlabel "iter"
set ylabel "subs not improve cr"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'sa_results.txt' using 1:14 with lines lc 7 title "subs not improve counter"




