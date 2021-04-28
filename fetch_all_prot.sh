touch $2
rm $2
i=0
while read line; do
	if [ $i -ne 0 ]; then
		species_name=`echo $line | cut -f 1 -d ","`
		esearch -db protein -query "$species_name [ORGN]" < /dev/null |
			efetch -format fasta >> $2
	else
		i=$((i+1))
	fi
done < $1
