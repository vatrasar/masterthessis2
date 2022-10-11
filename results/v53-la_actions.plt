#set style data lines
set xrange [0:600]
set yrange [0:1]
set xlabel "time"
set ylabel "dr 2-actions"
#set key at 95,80
#set label "b=1.4, k=6" at 5,110
plot 'la_actions_freq.txt' using 1:2 with lines lc 2 lw 3 title "LA 2: action 1",\
'la_actions_freq.txt' using 1:3 with lines lc 1 lw 3 title "LA 2: action 2",\
'la_actions_freq.txt' using 1:4 with lines lc 3 lw 3 title "LA 2: action 3",\
'la_actions_freq.txt' using 1:5 with lines lc 4 lw 7 title "LA 2: action 4",\
'la_actions_freq.txt' using 1:6 with lines lc 5 lw 3 title "LA 2: action 5",\
'la_actions_freq.txt' using 1:7 with lines lc 6 lw 3 title "LA 2: action 6",\
'la_actions_freq.txt' using 1:8 with lines lc 7 lw 3 title "LA 2: action 7",\
'la_actions_freq.txt' using 1:9 with lines lc 8 lw 3 title "LA 2: action 8",\
'la_actions_freq.txt' using 1:10 with lines lc 9 lw 3 title "LA 2: action 9",\
'la_actions_freq.txt' using 1:11 with lines lc 10 lw 3 title "LA 2: action 10"