user="$()"
t_win=30 # Minutes before to store
u=$(whoami)
d1=$(date -u -d -"$t_win"minutes +%s)
tmp=$(mktemp /tmp/u_filt.XXXXXX)
cwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$cwd"
ps -u $u -eo "comm %cpu %mem" --no-headers \
| awk -v tnow="`date -u +%s`" '{comm[$1] = $1; cpu[$1] += $2; mem[$1] += $3}END{for (i in comm)printf "%s %s %0.1f %0.1f\n", comm[i], tnow, cpu[i], mem[i]}' \
| sort -nk +2 >> ~/.usagelog
awk -v d1="$d1" '$2 >= d1' ~/.usagelog > ${tmp}
mv ${tmp} ~/.usagelog