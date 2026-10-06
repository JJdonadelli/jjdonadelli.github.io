#Time-stamp: <Mon Apr 12 13:30:52 2010 jair@asterix>
SHELL=/bin/bash

upload : 
	cp algale.html index.html
	rsync --exclude="*.{tex,pdf,dvi}*" -avuz --del ./ -e ssh jair@ime.usp.br:~/www/algale-html


