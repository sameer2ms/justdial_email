# Copyright (c) 2023, Sameer Shaikh and contributors
# For license information, please see license.txt

import json
import re
import frappe
from frappe.model.document import Document
import imaplib
# import smtplib
from frappe import _
import email
from email.parser import BytesParser

from bs4 import BeautifulSoup

import os
import mimetypes


class JustdialSettings(Document):
	def validate(self):
		check_email_credentials(self.email, self.get_password("password"), self.imap, self.folder)
		
def check_email_credentials(email, password, imap, folder):

		imap_server = imaplib.IMAP4_SSL(imap)  # Replace with the IMAP server address

		try:
			# Login to the server with the provided email and password
			mail = imaplib.IMAP4_SSL(imap)
			mail.login(email, password)
			
			mail.select(folder)

			# If the login is successful, the email and password are correct
			frappe.msgprint(_("Email Connected Sucessfully"))
		except imaplib.IMAP4.error:
			# If there's an error during login, the email or password is incorrect
			frappe.msgprint(_("Incorrect Email, Password or IMAP <br> Also check the Folder name "))

		# Logout from the server
		imap_server.logout()	


@frappe.whitelist()
def jd_get_emails():
	print(" this is \n\n button click")
	jd = frappe.get_doc("Justdial Settings")
	# imap_server = imaplib.IMAP4_SSL(jd.imap)  # Replace with the IMAP server address
	print("\n\n hjis is js", jd)

	try:

		imap_server = imaplib.IMAP4_SSL(jd.imap)  # Replace with the IMAP server address
		username = jd.email  # Replace with your email address
		password = jd.get_password("password") # Replace with your email password
		print("\n\n this is line, 49")
		# Login to the server
		imap_server.login(username, password)

		# Select the mailbox/folder you want to fetch emails from
		mailbox = 'Inbox'  # Replace with the desired mailbox/folder name
		imap_server.select(mailbox)

		email_addresses = ['sameer.s@indictranstech.com']
		print("\n\n this is line, 58")
		last_fetched_uid = 5149  # Replace with the UID of the last fetched email, or initialize it to the first UID to fetch

# Prepare the search query
		# search_query = ' OR '.join(['FROM "{}"'.format(email) for email in email_addresses]) + f' UID {last_fetched_uid+1}:*'
		search_query = ' OR '.join(['FROM "{}"'.format(email) for email in email_addresses]) 
		print("\n\n this is search query line 64")
		# Search for emails matching the query
		status, response = imap_server.uid('search', None, search_query)

		if status == 'OK':
			uids = response[0].split()

			for uid in uids:
				# Fetch the email
				status, email_data = imap_server.uid('fetch', uid, '(RFC822)')

				if status == 'OK':
					# Process the email data as needed

					parser = BytesParser()
					email_message = parser.parsebytes(email_data[0][1])

					# Extract the subject and main message
					subject = email_message['Subject']
					main_message = ''

					if email_message.is_multipart():
						for part in email_message.get_payload():
							if part.get_content_type() == 'text/plain':
								main_message = part.get_payload()
								break
					else:
						main_message = email_message.get_payload()

					# #print the subject and main message
					# print("Subject:", subject)
					# print("Main Message:", main_message)

					# Update the last fetched UID
					last_fetched_uid = uid

					print("\n\n line 104")
					raw_email1 = email_data[0][1].decode('utf-8')
					email_message1 = email.message_from_string(raw_email1)
					from_ = email_message1["From"]
					subject1 = email_message1["Subject"]
					counter = 1

					for part in email_message1.walk():
						# print(" this is insode part")
						if part.get_content_maintype() == "multipart":
							continue
						filename = part.get_filename()
						if not filename:
							# print(" this is insode not filename")
							ext = '.html'
							filename = 'msg-part-%08d%s' %(counter, ext)
						counter += 1

					content_type = part.get_content_type()
					# print(" tjis is content type", content_type)

					if "plain" in content_type:
						print("\n\n this is plain")
					elif "html" in content_type:
						html_ = part.get_payload()
						soup = BeautifulSoup(html_, "html.parser") 
						text = soup.get_text()
						# print("\n\n",subject1)
						# print("\n",text)




#  new JUL 04 https://www.youtube.com/watch?v=Jt8LizzxkPU
					email_content = email_data[0][1].decode('utf-8')
					raw_email = email_data[0][1]
					email_message = email.message_from_bytes(raw_email)

					# Extract the email fields
					subject = email_message['Subject']
					from_email = email_message['From']
					to_email = email_message['To']
					date = email_message['Date']

					# Extract the main message body (HTML content)
					main_message = ''

					if email_message.is_multipart():
						for part in email_message.get_payload():
							if part.get_content_type() == 'text/html':
								main_message = part.get_payload(decode=True).decode('utf-8')
								break
					else:
						main_message = email_message.get_payload(decode=True).decode('utf-8')

					# Create a dictionary with the email data
					email_data_dict = {
						'Subject': subject,
						'From': from_email,
						'To': to_email,
						'Date': date,
						'Main Message': main_message
					}

					# Convert the dictionary to JSON format
					email_data_json = json.dumps(email_data_dict)

					# Print the email data in JSON format
					# sprint(email_data_json)
					# #print("Email Content:", email_content)

					 # Get the sender's email address (From)
					sender_info = email_data[0][0].decode('utf-8').split(' ')[1]
					# sender_email = sender_info.split('<')[1].strip('>')
					
					# #print the email content, sender's email address, and UID
					# #print("Email Content:", email_content)
					##print("From:", sender_email)
					##print("UID:", uid)

					# Update the last fetched UID
					last_fetched_uid = uid

		# 55555555555
		search_query = ' OR '.join(['FROM "{}"'.format(email) for email in email_addresses])

# Search for emails matching the query
		status, response = imap_server.search(None, search_query)

		if status == 'OK':
			uids = response[0].split()

			for uid in uids:
				# Fetch the email
				status, email_data = imap_server.fetch(uid, '(RFC822)')

				if status == 'OK':
					# Process the email data as needed
					email_content = email_data[0][1].decode('utf-8')
					#print("Email Content:", email_content)

					

			# 444444444444
		# uids = []
		# for email_address in email_addresses:
		# 	status, response = imap_server.uid('search', None, f'(FROM "{email_address}")')

		# 	if status == 'OK':
		# 		uids.extend(response[0].split())

		# # Fetch the emails
		# for uid in uids:
		# 	status, email_data = imap_server.uid('fetch', uid, '(RFC822)')

		# 	if status == 'OK':
		# 		# Process the email data as needed
		# 		email_content = email_data[0][1].decode('utf-8')
		# 		#print("Email Content:", email_content)
				# 33333333333333333333
		# Get the UID of the last fetched email
		last_fetched_uid = 5143  # Replace with the UID of the last fetched email, or initialize it to the first UID to fetch

		# Fetch emails with UIDs greater than the last fetched UID
		status, response = imap_server.uid('search', f'{last_fetched_uid+1}:*')
		#print("this is sucess", response, status)

		if status == 'OK':
			uids = response[0].split()
			#print("\n\n this  uids", uids)

			for uid in uids:
				# Fetch the email
				#print("\n\n this is uid", uid)
				status, email_data = imap_server.uid('fetch', uid, '(RFC822)')

				if status == 'OK':
					# Process the email data as needed
					email_content = email_data[0][1].decode('utf-8')
					# print("Email Content:", email_content)

					# Update the last fetched UID
					last_fetched_uid = uid
		imap_server.logout()			
		# #print(" this is data", jd.imap, jd.email, jd.get_password("password"))
		# # Login to the server with the provided email and password
		mail = imaplib.IMAP4_SSL(jd.imap)
		mail.login(jd.email, jd.get_password("password"))

		
		# # desired mailbox/folder name
		mail.select(jd.folder)
		# #print("\n\n this is sucessfull \n\n")

		# Search for emails based on criteria (e.g., 'ALL' for all emails)
		# last_fetched_uid = 6043
		# search_criteria = f'(UID {"6043"}:*)'
		status, response = mail.search(None, 'ALL')
		# status, response = mail.search(None, search_criteria)

		

		if status == 'OK':
		
			email_ids = response[0].split()  # Get the list of email IDs
			# #print(" \n\n emaildis\n\n", email_ids)
			
			for email_id in email_ids:
			# 	# Fetch the email based on the ID
				status, response = mail.fetch(email_id, '(RFC822)')
			# 	# #print("\n\n this is reposm", response ,type(response))
				# uid = response[0].split()[2].decode('utf-8')

			# 	# uid_data = response[0]
			# 	# uid_list = uid_data.split()
			# 	# uid = uid_list[2].decode('utf-8')
				for item in response:
					if isinstance(item, tuple):
						uid_data = item[0]
						uid_list = uid_data.split()
						uid = uid_list[2].decode('utf-8')
						break

			# 	# #print the UID
			# 	frappe.set_value("Justdial Settings", "Justdial Settings", "uid", uid)
				# frappe.client.set_value("Justdial Settings", "Justdial Settings", "uid", uid)
				
				#print("\n\n UID of the last fetched email:", uid , type(uid))

				if status == 'OK':
					email_data = response[0][1]
				# 	# Parse the email data
					raw_email = email.message_from_bytes(email_data)

					# #print the email content
					print("From:", raw_email["From"], type(raw_email["From"]))
# newwwwwwwwwww
					raw_email1 = response[0][1].decode('utf-8')
					email_message1 = email.message_from_string(raw_email1)
					from_ = email_message1["From"]
					subject1 = email_message1["Subject"]
					counter = 1

					for part in email_message1.walk():
						print(" this is insode part")
						if part.get_content_maintype() == "multipart":
							continue
						filename = part.get_filename()
						if not filename:
							print(" this is insode not filename")
							# ext = '.html'
							content_type = part.get_content_type()
							ext = mimetypes.guess_extension(content_type)
							if not ext:
								ext = '.bin'
							filename = 'msg-part-%08d%s' %(counter, ext)
						counter += 1

					
					print(" tjis is content type", content_type)

					if "plain" in content_type:
						print("\n\n this is plain")
					elif "html" in content_type:
						html_ = part.get_payload()
						soup = BeautifulSoup(html_, "html.parser") 
						text = soup.get_text()
						print("\n\n subject \n",subject1)
						print("\n text \n",text)
					else:
						print("\n\n this is  Image files")

					# #print("To:", raw_email["To"])
					# #print("Subject:", raw_email["Subject"])
					# #print("Date:", raw_email["Date"])

					if raw_email.is_multipart():
						for part in raw_email.walk():
							content_type = part.get_content_type()
							if content_type == 'text/plain' or content_type == 'text/html':
								email_body = part.get_payload(decode=True)
								print("\nEmail Body: 111")
								print(type(email_body.decode('utf-8')), email_body.decode('utf-8'))
								email_string = email_body.decode('utf-8')
								# Use regular expression to extract the name
								name_match = re.search(r"City:\s*(\w+)", email_string)
								state1 = re.search(r"State:\s*(\w+)", email_string)
								requ1 = re.search(r'User Requirement:\s*([\w\s]+)', email_string)
								search_dt1 = re.search(r'\b(\w+,\s\d+\s\w+\s\d+\s\d+:\d+:\d+)\b', email_string)
								phone_no1 = re.search(r'\+(\d+)', email_string)

								name_ = re.search(r'\b(\w+\+\w+)\sinquired', email_string)
								if name_:
									print(" this is true")
									name1 = name_.group(1)
									print(" this is customer _ name", name1)
								else:
									print("Name not found.")	
								
								if name_match:
									name = name_match.group(1)
									print("Name:", name)
								if state1:	
									state = state1.group(1)
									print("State:", state)
								if requ1:	
									requ = requ1.group(1).strip()
									print("requ", requ)
								if search_dt1:	
									search_dt = search_dt1.group(1).strip() 
									print(" date ", search_dt)
								if phone_no1:	
									phone_no = phone_no1.group(1)

									print("Phone :", phone_no)


								break
					# else:
					# 	email_body = raw_email.get_payload(decode=True)
					# 	#print("\nEmail Body:")
					# 	#print(email_body.decode('utf-8'))
					# uid = response[0].split()[2].decode('utf-8')

					


		# mail.logout()
	except imaplib.IMAP4.error:
		# If there's an error during login, the email or password is incorrect
		print(_("Incorrect Email, Password or IMAP"))	

	return True	
