SHELL=/bin/bash

UFABC=hostel.ufabc.edu.br
ASTERIX=192.168.0.10

#get :	
#	rsync --del --exclude=".git" -avuz  ~/Dropbox/public_html/ .	
#put :#
#	rsync --del -Cavuz --exclude="*~" --exclude=".git" ./ ~/Dropbox/public_html

#upload :#
#	rsync  --del -avuz  --exclude="*~" --exclude=".git" ./  -e ssh jair.donadelli@${UFABC}:~/public_html
upload:
	@for i in 1 2 3; do \
		rsync --del -avuz \
			--exclude="*~" \
			--exclude=".git" \
			./ \
			jair.donadelli@hostel.ufabc.edu.br:~/public_html \
		&& exit 0; \
		echo "falhou; aguardando 60s"; \
		sleep 60; \
	done; \
	exit 1
sync :
#	chmod -R 644 ./logica/*.*
#	make put upload
#	rm /home/yair/.ssh/known_hosts
	make upload
#	cp index.html jjdonadelli.github.io/ && \
#	cd  jjdonadelli.github.io/ && \
#	if ! git diff --quiet; then \
#		git commit -am "Página pessoal atualizada" && \
#		git push; \
#	else \
#		echo "Nada para atualizar."; \
#	fi


download : 
	 rsync  -avuzb -e ssh jair.donadelli@${UFABC}:~/public_html/  .







