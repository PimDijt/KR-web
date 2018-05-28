for file in `ls ./$HOSTNAME/`
for line in `cat ./$HOSTNAME/$file`
do
    cd ..
    python get_features_larger.py $file $line 1> ./logs/$file/$line.log 2> ./err/$file/$line.err
    cd datastore
done
done