for line in `cat ./md5hashes.txt`
do
echo $line
if [ ! -f ../data/$line.nt ]; then
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line.gz
mv $line ../data/$line.nt
#cd ..
#python parse_data.py
#cd datastore
fi
done
