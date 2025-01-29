
all: start

start:
	python src/app/main.py

apply:
	@pip freeze > function-source/requirements.txt
	@cd terraform && terraform init && terraform apply -auto-approve

destroy:
	@cd terraform && terraform init && terraform destroy -auto-approve
	@rm -f function-source.zip