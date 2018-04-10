for i in `ls data/`
do
  cat data/$i | cut -d';' -f24 | less
done  
