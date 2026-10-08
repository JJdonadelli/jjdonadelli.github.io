# Diretórios
PUBLIC_HTML := $(HOME)/public_html
REPO        := $(HOME)/jjdonadelli.github.io

# Servidor remoto
REMOTE_USER := jair.donadelli
HOST        := hostel.ufabc.edu.br
REMOTE_DIR  := ~/public_html

.PHONY: atualiza repo remoto status

# Atualiza tudo
atualiza: repo remoto

# Copia public_html para o repositório Git local
repo:
	@echo "==> Atualizando repositório local..."
	rsync -av --delete \
		--exclude='.git/' \
		$(PUBLIC_HTML)/ $(REPO)/
	@echo "==> Estado do repositório:"
	cd $(REPO) && git status

# Copia public_html para o servidor
remoto:
	@echo "==> Atualizando $(HOST):$(REMOTE_DIR)..."
	rsync -av --delete \
		$(PUBLIC_HTML)/ $(REMOTE_USER)@$(HOST):$(REMOTE_DIR)/

# Mostra o estado do repositório local
status:
	cd $(REPO) && git status

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

download : 
	 rsync  -avuzb -e ssh jair.donadelli@${UFABC}:~/public_html/  .



