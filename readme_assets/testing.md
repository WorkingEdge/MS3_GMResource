Initial set up followed the process usedin the walkthrough task manager app.

After setting up the Db, the config, getting the MONGO_URI string etc, testing the app raised the following error:
 - insert mongo_not_defined.png

 This was caused by a missing constructor method: 
 mongo = PyMongo(app)

 Adding this resolved the issue and page loaded correctly showing a test record from the connected db:
 - insert resolved_mongo_not_defined.png
