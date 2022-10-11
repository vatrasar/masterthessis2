#set style data lines
set xrange [0:21]
set yrange [0:15.5]
set xlabel "zone_id"
set ylabel "av reward"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'freq_of_hits.txt' using 1:3 with steps lc 7 title "av reward"
 
