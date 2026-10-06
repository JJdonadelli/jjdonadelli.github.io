#Time-stamp: <Mon Mar 22 21:37:56 2010 jair@asterix>
SHELL=/bin/bash

upload : 
	cp post.html index.html	
	rsync --exclude="*.{tex,dvi,pdf}" -avuz --del ./ -e ssh jair@fradim.inf.ufpr.br:~/WWW/discreta-html

download : 
	rsync -avuz -e ssh jair@fradim.inf.ufpr.br:~/disciplinas/Discreta/ ~/disciplinas/Discreta

clean:
	rm -rfdv auto *.{flc,dvi,*~,aux,log,tmp,toc,xref,idx,out,nav,snm,ps,bak}

