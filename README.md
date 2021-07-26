# Carbon Usage Api exercise


#### API Rest that allow manage a database regarding carbon usage data for users

    # Be sure to have docker and docker-compose installed on you system.
    Example for Ubuntu 20.04 can be found here: 

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-pt

    #Build docker container
	docker-compose build
	
	#Run docker containers using docker-compose, first db then api
	docker-compose up
	
	#Run the migrations
	docker-compose exec api python manage.py migrate
	
	#Load initial data (usage types preload)
	docker-compose exec api python manage.py loaddata initial_usage_types
	
	#Create first admin user (user: admin, password: a)
	docker-compose exec api python manage.py initadmin
	
    
# API Documentation
- Documentation of the API is available in https://documenter.getpostman.com/view/5401097/TzsZs8ue
- Access the Postman Collection available in the root of the project
- Run "Login JWT", get the token and use it as an global variable or as collection variable with the name 'token'.

# Tests
- The tool used for the tests was Pytest.
- To run the tool e.g: "docker-compose exec api pytest".

# Other Notes
- Time of creation 5 hours for the API.
- Time for testing 6 hours.
- Most of my difficulty was related to testing. I had some experience with Pytest in the past but I've not been working with tests for some time. 
