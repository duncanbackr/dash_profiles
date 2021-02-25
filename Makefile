start:
	docker-compose build
	docker-compose up

deploy:
	gcloud config set project ${PROJECT}
	gcloud builds submit
