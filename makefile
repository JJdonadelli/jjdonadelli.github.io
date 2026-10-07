# Diretórios
PUBLIC_HTML := $(HOME)/public_html
REPO        := $(HOME)/jjdonadelli.github.io

# Servidor remoto
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
		$(PUBLIC_HTML)/ $(HOST):$(REMOTE_DIR)/

# Mostra o estado do repositório local
status:
	cd $(REPO) && git status



