#Time-stamp: <Mon Jun 21 14:58:38 2010 jair@asterix>

SHELL=/bin/bash

NAME=$(notdir $(CURDIR))

clean : 
	rm -fv *.{ps,pdf,log,aux,bbl,flc,out,idx,ilg,ind,fig.bak,*~,4ct,4tc,blg,css,dvi,idv,idx,lg,tmp,toc,xref,loa}
	rm -rfdv auto
	rm -rfdv figs/*{~,bak}

upload : 
	 rsync  --del -avuz /home/jair/DISCIPLINAS/$(NAME)/ -e ssh jair@fradim.inf.ufpr.br:~/DISCIPLINAS/$(NAME)

download : 
	rsync -avuz -e ssh jair@fradim.inf.ufpr.br:~/DISCIPLINAS/$(NAME)/ /home/jair/DISCIPLINAS/$(NAME)

atualiza : 
	cp ci065.html index.html
	 rsync --del --exclude="aula*" --exclude="figs/*" --exclude="figs" --exclude="lista*html" --exclude="*.tex*" --exclude="*dvi" -avuz ./ -e ssh jair@ime.usp.br:~/www/ci065





#------------------------------------------------------------------------------
TEX_FILE=$(NAME).tex
#------------------------------------------------------------------------------
.PHONY : dvi\
	 pdf\
	 xdvi\
	 clean\
	 upload\
	 overfull

dvi : $(NAME).dvi

pdf : $(NAME).pdf

html: $(NAME).html
#------------------------------------------------------------------------------

$(NAME).dvi : $(NAME).tex $(NAME).ind
	latex $<;\
	if egrep -q 'There were undefined references' $(NAME).log; then\
	    bibtex $(NAME);\
	    latex $<;\
	    fi;\
	while egrep -q 'Rerun|No file $(NAME).toc' $(NAME).log; do latex $<; done

$(NAME).ps : $(NAME).dvi
	dvips -t $(paper) -o $@ $<

$(NAME).pdf : $(NAME).tex
	pdflatex $<

$(NAME).bbl : $(NAME).dvi

$(NAME).ind : $(NAME).idx $(NAME).tex
	makeindex $<

$(NAME).idx : $(NAME).aux

$(NAME).aux : $(NAME).tex
	latex $<;\
	if egrep -q 'There were undefined references' $(NAME).log; then\
	    bibtex $(NAME);\
	    latex $<;\
	    fi;\
	while egrep -q 'Rerun|No file $(NAME).toc' $(NAME).log; do latex $<; done

#------------------------------------------------------------------------------

overfull : $(NAME).log
	@grep 'Overfull \\hbox' $<\
	| sed -e 's/Overfull \\hbox (//'\
	| sed -e 's/pt too wide)//'\
	| sort -nr\
	#| head -1

underfull : $(NAME).log
	@grep 'Underfull \\hbox' $<\
	| sed -e 's/Underfull \\hbox (badness //'\
	| sed -e 's/)//'\
	| sort -nr\
	| head -1

