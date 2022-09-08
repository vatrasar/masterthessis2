#set style data lines
set xrange [0:1200]
set yrange [0:10]
set xlabel "x"
set ylabel "subs not acc cr"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'sa_results.txt' using 1:13 with lines lc 7 title "subs not improved counter"




