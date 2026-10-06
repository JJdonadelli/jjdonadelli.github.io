#Time-stamp: <Tue Mar 23 08:16:14 2010 jair@asterix>
SHELL=/bin/bash

upload : 
#	cp cripto.html index.html	
	rsync --exclude="*.{tex,dvi,pdf}" -avuz --del ./ -e ssh jair@fradim.inf.ufpr.br:~/WWW/cripto-html

clean:
	rm -rfdv auto *.{flc,dvi,*~,aux,log,tmp,toc,xref,idx,out,nav,snm,ps,bak}

