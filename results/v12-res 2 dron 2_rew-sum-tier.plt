set style data lines
set xrange [0:1050]
set yrange [0:30.5]
set xlabel "x"
set ylabel "reward"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'res2.txt' using 4:9 with impulses lc 2 title "dr 2: reward",\
'res2.txt' using 4:12 with points lc 4 title "sum of rew",\
'res2.txt' using 4:5 with lines lc 9 title "tier dr 2",\
 
