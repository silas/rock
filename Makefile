setup:
	./misc/setup

clean:
	vagrant destroy -f

.PHONY: build clean
