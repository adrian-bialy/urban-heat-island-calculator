setup-env:
	conda create --name island python=3.10.12 pip ipython -y
	conda init bash

	echo 'Installing dependencies...'
	conda run --name island pip install -r requirements.txt