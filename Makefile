
all: start

start:
	python src/app/main.py

apply:
	@pip freeze > function-source/requirements.txt
	@cd terraform && terraform init && terraform apply -auto-approve

destroy:
	@rm -f function-source.zip
	@cd terraform && terraform init && terraform destroy -auto-approve