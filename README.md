# RustPiDeployment
  
  ## How to use:
  	
   	- Export PI_HOST, PI_NAME and PI_PASSWORD as env variables
    - Run the script with: python3 deploy.py deploy <path_of_project_folder>

	The Script will SSH into your Raspi, move your code via sftp , compile and run it. 
    At the moment you have to exit it with CTRL-C to kill the session.
