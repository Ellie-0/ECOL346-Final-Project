# Author: Maya Bose
# Purpose: This script takes a list of species ($1) and the name of a protein ($2)
# and returns all protein sequences containing that protein name available for 
# each species of fish from the NCBI Protein database. 
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
