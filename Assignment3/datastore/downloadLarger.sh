mkdir ../dataL
mkdir l
mkdir ../err
mkdir ../logs
mkdir ../logs/l/
mkdir ../err/l/
for file in `ls ./$HOSTNAME/`
do
for line in `cat ./$HOSTNAME/$file`
do
echo $line
cd l
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line.gz
mv $line ../../dataL/$line.nt
cd ../..
python parse_data_larger.py . $line 1> logs/l/llog$line.log 2>err/l/lerr$line.err
mkdir ./dataL/$file
mv ./dataL/$line.nt ./dataL/$file/$line.nt
cd datastore
done
done