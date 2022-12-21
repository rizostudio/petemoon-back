update_deps:
	@echo "Updating dependencies..."
	-pip-compile common.in --output-file common.txt
	-pip-compile dev.in --output-file dev.txt
	-pip-compile production.in --output-file production.txt
	-pip-compile test.in --output-file test.txt
	@echo "Done."