
import images_checker
from mail_downloader import MailDownloader
import plates_checker

print("Checking for new mails...")
#MailDownloader().mail_attachments_download()
print("Retrived images processing...")
plate_list = images_checker.process_images()
print("Checking recognized plates...")
plates_checker.process_plates(plate_list)
