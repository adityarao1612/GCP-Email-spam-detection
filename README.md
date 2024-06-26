# Email Spam Detection

Prerequisite:
- train a AutoML model on a spam-ham dataset from kaggle. example: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
- Add your private key to bearer token in app.py
- deploy the model to an endpoint and copy paste the endpoint to url in scan_spam() function
- enable Document AI api on GCP and copy paste the endpoint to url in get_ocr_data()

Run the app.py file:
- Tkinter window:
  
![image](https://github.com/adityarao1612/GCP-Email-spam-detection/assets/92964413/5d5bef53-c2e5-43c0-8efb-d7641092bbba)

- Take a snip screenshot of your email feed to check for spam:
  
sample image:

![image](https://github.com/adityarao1612/GCP-Email-spam-detection/assets/92964413/7216461c-1edd-4bc1-a301-2e2820eab5ed)

- click on Import from Clipboard and Scan for Spam:

output image:
  
![image](https://github.com/adityarao1612/GCP-Email-spam-detection/assets/92964413/f93c44db-44cf-4b39-82d8-7cb28c9aec66)

emails which are spam are highlighted in red and not spam are highlighted in green
