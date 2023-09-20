IMAGE_NAME = ra-bot
WEBHOOK_URL = "your_webhook_url_here"
SITE_URL = "https://retroachievements.org/user/Lahey"

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -e WEBHOOK_URL=$(WEBHOOK_URL) -e SITE_URL=$(SITE_URL) -v $(PWD)/last_rank.txt:/app/last_rank.txt $(IMAGE_NAME)

.PHONY: build run
