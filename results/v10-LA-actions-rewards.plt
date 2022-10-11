set style data lines
set xrange [1:10]
set yrange [0:16]
set xlabel "goal-action"
set ylabel "action reward"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'LA_goals.txt' using 1:11 with steps lc 7 lw 3 title "avg rew",\
'LA_goals.txt' using 1:6 with steps lc 7 title "dr 1 rew",\
'LA_goals.txt' using 1:7 with steps lc 2 title "dr 2 rew"
 
