# Python entrypoint; override MAIN if your project uses a different filename.
PYTHON ?= python3
MAIN ?= main.py
NAME ?= n-puzzle

.PHONY: all clean fclean re test

all: $(NAME)

$(NAME): $(MAIN)
	@printf '#!/bin/sh\nexec %s "%s" "$$@"\n' '$(PYTHON)' '$(MAIN)' > $(NAME)
	@chmod +x $(NAME)

clean:
	@find . -type d -name __pycache__ -prune -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete
	@rm -rf .pytest_cache

fclean: clean
	@rm -f $(NAME)

re: fclean all

test:
	@$(PYTHON) -m pytest -q
