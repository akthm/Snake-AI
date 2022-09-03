Snake Game


How to use

	pip3 install -r requirements.txt
	
	python3 main.py
	
	python3 main.py -h to show all options


Examples: 

	using q-learning => --agent q-learning --model 10000.pickle (only use pickle dumps).
	
	training q-learning => --agent q-learning -t --num_episodes 10000 --interface silent.
	
	using A-star => --agent astar --heuristic manhattan -ob 4 -w (for wall and obstacles).
	
	using hamilton => --agent hamilton (do not add obstacles it is not optimized for that).
	
	using human agent => --agent human 
