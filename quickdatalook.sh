cat data/dak-en-thuislozenzorg.csv | cut -d';' -f24
cat data/verpleeg-en-verzorgingshuizen.csv | cut -d';' -f24 | less
cat data/lhbt-hulpverlening.csv | cut -d';' -f24