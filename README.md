Author:         Haotian

Last Update:    March 3, 2014 

----
### front end
	bootstrap
	javascript

### back end
	python
	flask
	jinja
	mongodb
	

----
# Setup


All assume MAC, PC please do the equivalent and ask me 
install Python (you should have by default)

#### Check Python
    
    haotians-mbp:~ Ted$ python 
    Python 2.7.5 (default, Sep  2 2013, 05:24:04)
make sure version is > 2.7, if not update

#### Install git (you should have by default)
setup github and fork
[https://github.com/tedsunnyday/SE-Server
](http://)

#### Install homebrew 
[http://brew.sh/](http://)    
goto shell and run 

    ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

#### Install pip

    sudo easy_install pip


#### Install google app engine SDK for python
[    https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python](http://)
run the application, if cannot get started then try to cd to the SE-Server dir, and run below command

        sudo pip install -r requirements.txt

#### (optional) Install MongoDB to localmachine

you may need to sudo as well

    brew update
    brew install mongodb
and then start the MongoDB daemon by 
	
	mongod

and then in another terminal 

	mongo
    
you should now in the interactive shell, more info here    [http://docs.mongodb.org/manual/tutorial/getting-started/](http://)
**please noted** that even you are running the application locally, the current connection string is still pointing to the remote mongolab db, so, if you want to point the mongo db locally, find the db config code in `main.py` and
comment out and comment the code, which has been commented so quite selfexplaintary, make sure you mongod first



## Account Info
---

#### Gmail

    yale.hout@gmail.com
    yalese14

#### MongoDB

https://mongolab.com/databases/yalehout/collections/
	
	yale.hout@gmail.com
	qwe123

    current 2 db
        yalehout
        yalehout_prod

