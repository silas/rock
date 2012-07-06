setup:
	./misc/setup

package:
	vagrant ssh -c 'cd /vagrant/packages/rpms && brpm -d epel-6 ./build.json'

install:
	vagrant ssh -c 'sudo rm -fr /tmp/rpms && cp -r /vagrant/packages/rpms/build/epel/6/x86_64 /tmp/rpms && rm -f /tmp/rpms/*{debuginfo,rpmbuild}*.rpm && sudo yum localinstall --nogpgcheck -y /tmp/rpms/*.rpm'

uninstall:
	vagrant ssh -c 'sudo yum remove -y "rock-*" && sudo rm -fr /opt/rock'

destroy:
	vagrant destroy -f

.PHONY: setup destroy
