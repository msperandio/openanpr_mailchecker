import images_checker
import mail_downloader
import plates_checker

print("Checking for new mails...")
mail_downloader.mail_attachments_download()
print("Retrived images processing...")
plate_list = images_checker.process_images()
print("Checking recognized plates...")
plates_checker.process_plates(plate_list)
