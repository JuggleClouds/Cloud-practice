# variables projects
REPO = docker.io/
DOCKER_USER = juggleclouds
DOCKER_PASS = ''
NAMEAPP = juggleclouds/cloudpractice
VERSIONAPP = helm-k8s-exampleapp-0.1.0
NAMECHART = example-blog
NAMEDB = juggleclouds/cloudpractice
VERSIONDB = helm-k8s-exampledb-0.1.0
NAMESPACE = exampleapp

.PHONY: upgrade prep build build_app build_db push run status clean dry-run purge

prep:
	@#@ Enables deployment of pods to the master node
	kubectl taint nodes --all dedicated- || echo "OK"


build: build_app build_db
	@#@ build docker images. Before you need install docker

build_app:
	cd image_base_app/ && docker build -t $(REPO)$(NAMEAPP):$(VERSIONAPP) .

build_db:
	cd image_base_db/ && docker build -t  $(REPO)$(NAMEDB):$(VERSIONDB) .

login:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS) $(REPO)

push: login
	@#@ Push images. Before shove you need to set the variables DOCKER_USER & DOCKER_PASS
	docker push $(REPO)$(NAMEAPP):$(VERSIONAPP)
	docker push $(REPO)$(NAMEDB):$(VERSIONDB)

dry-run:
	@#@ dry-run helm projects
	helm install  . --dry-run --debug --name $(NAMECHART) --set app.Image=$(REPO)$(NAMEAPP),app.ImageTag=$(VERSIONAPP),db.ImageDb=$(REPO)$(NAMEDB),db.ImageTagDb=$(VERSIONDB)  --namespace $(NAMESPACE)

run:
	@#@ install helm projects
	helm install  . --name $(NAMECHART) --set app.Image=$(REPO)$(NAMEAPP),app.ImageTag=$(VERSIONAPP),db.ImageDb=$(REPO)$(NAMEDB),db.ImageTagDb=$(VERSIONDB) --namespace $(NAMESPACE)

upgrade:
	@#@ upgrade helm projects
	helm upgrade $(NAMECHART)  . --debug   --set app.Image=$(REPO)$(NAMEAPP),app.ImageTag=$(VERSIONAPP),db.ImageDb=$(REPO)$(NAMEDB),db.ImageTagDb=$(VERSIONDB)   --namespace $(NAMESPACE)


status:
	@#@ status helm projects
	helm status $(NAMECHART)

clean:
	@#@ delete helm projects
	helm delete $(NAMECHART)

purge:
	@#@ Purge helm projects
	helm delete --purge $(NAMECHART)

help:
	@grep -P "\t@#@" $(CURDIR)/Makefile -B 2 | \
	grep -P "^([\w$$]+|\t)" | \
	awk '{if ($$1 ~ /^@?#/) {$$1="\t\t";print;} else print "\033[1;37m" $$1 "\033[0m "}'
