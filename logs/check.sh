#!/bin/sh

echo " // Rapport creation chemin //
" > ./results.txt
for i in *.log ; do
    if [ -f $i ]
    then
        fin_fic=$(tail -1 $i)
        if [ ! $fin_fic ]
        then    
            echo "erreure creation chemin : voir fichier $i
            pour plus de details ! " >> ./results.txt
        fi
    fi
    
done
echo "-----------------------------" >> ./results.txt

exit 0
            
