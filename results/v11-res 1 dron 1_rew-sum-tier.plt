#set style data lines
set xrange [0:1050]
set yrange [0:30.5]
set xlabel "x"
set ylabel "reward"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'res1.txt' using 2:6 with impulses lc 7 title "dron 1: reward",\
'res1.txt' using 2:12 with points lc 4 title "sum of rewards",\
'res1.txt' using 2:3 with points lc 9 title "tier dron 1"
 
