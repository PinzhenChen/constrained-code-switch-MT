for i in fk12 1 2 4 6 12 24 36 48
#for i in 1 4 12 24 36 48
do
 echo "normalizing the output with beam size $i"
 INPUT=valid.output.${i}.hg

 hinums=( "०" "१" "२" "३" "४" "५" "६" "७" "८" "९" )
 for i in {0..9}
 do
  h=${hinums[${i}]}
  sed -i "s/${h}/${i}/g" $INPUT
 done
done
