mkdir logsDT
mkdir errDT
mkdir logsDT/l
mkdir errDT/l
mkdir logsDT/l
mkdir errDT/l
while true
do
for file in `ls ./dataL/`
do
mkdir logsDT/l/$file
mkdir errDT/l/$file
if [ -d ./dataL/$file ]; then
cd ./dataL/$file
for line in `ls ./ | cut -d'.' -f1`
do
    cd ../..
    echo $file $line
    python apply_rule_larger.py $file $line 1> ./logsDT/l/$file/$line.log 2> ./errDT/l/$file/$line.err
    cd dataL/$file
done
cd ../..
fi
done
done