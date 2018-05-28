mkdir ../dataS
mkdir s
mkdir ../err
mkdir ../logs
mkdir ../logs/s/
mkdir ../err/s/
for file in `ls ./$HOSTNAME/`
do
for line in `cat ./$HOSTNAME/$file`
do
echo $line
cd s
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line.gz
mv $line ../../dataS/$line.nt
cd ../..
python parse_data_larger.py $line 1> logs/s/slog$line.log 2>err/s/serr$line.err
mkdir ./dataS/$file
mv ./dataS/$line.nt ./dataS/$file/$line.nt
cd datastore
done
done