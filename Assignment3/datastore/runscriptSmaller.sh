for line in `cat ./$HOSTNAME/md5hashes.txt`
do
echo $line
if [ ! -f ../data2/$line.nt ]; then
cd s
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line.gz
mv $line ../../data2/$line.nt
cd ../..
python parse_data_smaller.py $line 1> slog$line.log 2>serr$line.err
cd datastore
fi
done
