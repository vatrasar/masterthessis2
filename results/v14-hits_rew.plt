set style data lines
set xrange [0:1050]
set yrange [0:15.5]
set xlabel "x"
set ylabel "reward"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'res2.txt' using 4:9 with lines lc 7 title "dron 2: reward"