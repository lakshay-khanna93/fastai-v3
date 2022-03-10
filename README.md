One-time setup
Fork the starter app on GitHub.
Fork https://github.com/lakshay-khanna93/fastai-v3 into your GitHub account.

Create a Render account
Sign up for a Render account. 

Upload your trained model file
Upload the trained model file created with learner.export (for example export.pkl) to a cloud service like Google Drive or Dropbox. Copy the download link for the file.

Note the download link should start the file download directly—and is typically different from the share link (which presents you with a view to download the file).

Google Drive: Use this [link](https://www.wonderplugin.com/online-tools/google-drive-direct-link-generator/) generator.
Dropbox: Use this [link](https://syncwithtech.blogspot.com/p/direct-download-link-generator.html) generator
Customize the app for your model
Check what versions of packages you are using with following command in the Jupyter Notebook you built your model in: ! pip list
Edit the file requirements.txt inside the repo and update the package versions so that they correspond to the ones used by your Jupyter Notebook.
Edit the file server.py inside the app directory and update the export_file_url variable with the URL copied above.
Commit and push your changes to GitHub.
Make sure to keep the GitHub repo you created above current. Render integrates with your GitHub repo and automatically builds and deploys changes every time you push a change.

Deploy
Create a new Web Service on Render and use the repo you created above. You will need to grant Render permission to access your repo in this step.

On the deployment screen, pick a name for your service and use Docker for the Environment. The URL will be created using this service name. The service name can be changed if necessary, but the URL initially created can’t be edited.

Click Save Web Service. That’s it! Your service will begin building and should be live in a few minutes at the URL displayed in your Render dashboard. You can follow its progress in the deploy logs.


Link to the heart sound detection web app is [here](https://heartdiseasecetection.onrender.com/)

Local testing
To run the app server locally, run this command in your terminal:

python app/server.py serve
If you have Docker installed, you can test your app in the same environment as Render’s by running the following command at the root of your repo:

docker build -t fastai-v3 . && docker run --rm -it -p 5000:5000 fastai-v3
Go to http://localhost:5000/ to test your app.

Thanks to FastAI for the sample.