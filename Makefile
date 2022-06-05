WORKING_DIR := $(shell pwd)
.DEFAULT_GOAL := help

.PHONY: build push

docs:: ## Builds the README.md for charts
		helm-docs

bump-%:: ## Bump the version of charts and pyproject.toml
		poetry version $*
		for chart in "$(shell ls -1 charts)"; do helm local-chart-version bump --chart charts/$${chart} --version-segment $*; done
		make docs

# a help target including self-documenting targets (see the awk statement)
define HELP_TEXT
Usage: make [TARGET]... [MAKEVAR1=SOMETHING]...

Available targets:
endef
export HELP_TEXT
help: ## this help target
	@cat .banner
	@echo
	@echo "$$HELP_TEXT"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
		{printf "\033[36m%-30s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
