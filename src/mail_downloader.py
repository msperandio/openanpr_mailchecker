import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from config_mgr import ConfigMgr


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


class MailDownloader:
    def __init__(self):
        config = ConfigMgr().config
        self.username = config['email_to_check']['address']
        self.password = config['email_to_check']['password']
        self.mb = config['email_to_check']['mailbox']
        self.trash = config['email_to_check']['trash']
        self.imap_add = config['email_to_check']['imap_add']

    def mail_attachments_download(self):
        # create an IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL(self.imap_add)

        # authenticate
        imap.login(self.username, self.password)

        status, messages = imap.select(self.mb)
        # total number of emails        
        messages = int(messages[0])
        print("Messages: ", messages)
        while(messages>0):
            # for i in range(1, messages + 1, 1):
            status, messages = imap.select(self.mb)
            # total number of emails
            messages = int(messages[0])
            print(messages)
            # print(i)
            # fetch the email message by ID
            # res, msg = imap.fetch(str(i), "(RFC822)")
            res, msg = imap.fetch("1", "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # print("Subject:", subject)
                    # print("From:", From)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                # print(body)
                                pass
                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    folder_name = clean(subject)
                                    folder_path = os.path.join("attachments", folder_name)
                                    if not os.path.isdir("attachments"):
                                        os.mkdir("attachments")
                                    if not os.path.isdir(folder_path):
                                        # make a folder for this email (named after the subject)
                                        os.mkdir(folder_path)
                                    filepath = os.path.join(folder_path, filename)
                                    # download attachment and save it
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print only text email parts
                            # print(body)
                            pass
                    if content_type == "text/html":
                        # if it's HTML, create a new HTML file and open it in browser
                        folder_name = clean(subject)
                        folder_path = os.path.join("../attachments", folder_name)
                        if not os.path.isdir(folder_path):
                            # make a folder for this email (named after the subject)
                            os.mkdir(folder_path)
                        filename = "index.html"
                        filepath = os.path.join(folder_path, filename)
                        # write the file
                        open(filepath, "w").write(body)
                        # open in the default browser
                        webbrowser.open(filepath)
            # copy_resp = imap.copy(str(i), self.trash)
            copy_resp = imap.copy("1", self.trash)
            if copy_resp[0] != 'OK':
                print("Error on moving to trash: " + str(i))

        # close the connection and logout
        imap.close()
        imap.logout()
