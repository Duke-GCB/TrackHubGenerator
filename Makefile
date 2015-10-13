HUBROOT=/trackhub
DATA=/data
all: hub bigwigs

hub:
	$(MAKE) -f Makefile.hub HUBROOT=$(HUBROOT)

bigwigs:
	$(MAKE) -f Makefile.bigwig HUBROOT=$(HUBROOT) BEDFILES_DIR=$(DATA)/central20bp/E2F1 FILE_PREFIX=E2F1
	$(MAKE) -f Makefile.bigwig HUBROOT=$(HUBROOT) BEDFILES_DIR=$(DATA)/central20bp/E2F4 FILE_PREFIX=E2F4

clean:
	rm -rf $(HUBROOT)/*
