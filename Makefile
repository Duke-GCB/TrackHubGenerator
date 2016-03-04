HUBROOT=/trackhub
DATA=/data
all: hub bigbeds

hub:
	$(MAKE) -f Makefile.hub HUBROOT=$(HUBROOT)

bigbeds:
	$(MAKE) -f Makefile.bigbed HUBROOT=$(HUBROOT) HG19_BEDFILES=$(DATA)/hg19/central20bp/E2F1 HG38_BEDFILES=HG19_BEDFILES=$(DATA)/hg38/central20bp/E2F1 FILE_PREFIX=E2F1

clean:
	rm -rf $(HUBROOT)/*
