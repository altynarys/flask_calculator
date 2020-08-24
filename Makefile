version := 1.0
app := 'calc-application'

build:
	docker build -t askarissayev/$(app):$(version) -f app/Dockerfile .
push:
	docker push askarissayev/$(app):$(version)
deploy:
	kubectl apply -f app/namespace.yaml -f app/deployment.yaml -f app/service.yaml -f app/ingress.yaml
delete:
	kubectl delete -f app/namespace.yaml -f app/deployment.yaml -f app/service.yaml -f app/ingress.yaml
