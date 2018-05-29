mkdir ../dataL2
mkdir l2
mkdir ../err2
mkdir ../logs2
mkdir ../logs2/l/
mkdir ../err2/l/
for file in `ls ./$HOSTNAME/`
do
for line in `cat ./$HOSTNAME/$file`
do
echo $line
cd l2
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line.gz
mv $line ../../dataL2/$line.nt
cd ../..
python parse_data_larger.py . $line 1> logs2/l/llog$line.log 2>err2/l/lerr$line.err
mkdir ./dataL2/$file
mv ./dataL2/$line.nt ./dataL2/$file/$line.nt
cd datastore
done
done