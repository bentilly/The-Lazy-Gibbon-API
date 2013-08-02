import logging
from google.appengine.api import mail


def sendResetPasswordEmail(tlguser, host_url):
    message = mail.EmailMessage()
    message.sender = "The Lazy Gibbon <ben.tilly@gmail.com>"
    message.subject = "The Lazy Gibbon password reset"
    toString = tlguser.name
    toString += " <"
    toString += tlguser.email
    toString += ">"
    message.to = toString
    message.body = "Hi "
    message.body += tlguser.name
    message.body += "\nClick the link below to reset your password \n\n"
    message.body += host_url #append the server / host URL that is processing this request
    message.body += "/reset/resetPasswordPage?resetToken="
    message.body += str(tlguser.resetToken)
    
    logging.info(message.body)
    
    message.send()
    return

def sendGroupInviteEmail(invite, host_url):
    inviter = invite.invited_by.get().name
    groupName = invite.group.get().name
    #send email to invitee
    message = mail.EmailMessage()
    message.sender = "The Lazy Gibbon <ben.tilly@gmail.com>"
    message.subject = "You have been invited to use The Lazy Gibbon"
    toString = " <"
    toString += invite.email
    toString += ">"
    message.to = toString
    message.body = "Hi\n"
    message.body += inviter
    message.body += ' has invited you to join '
    message.body += groupName
    message.body += ' on The Lazy Gibbon\n\n\n\n'
    message.body += 'To accept this invitation click this link:\n'
    message.body += host_url #append the server / host URL that is processing this request
    message.body += "/groupInvite/invitePage?inviteKey="
    message.body += str(invite.key.urlsafe())
    message.body += '\n\n Otherwise ignore this message' 
    
    logging.info(message.body)
    
    message.send() 
    return

def sendEmailConfirmation(tlguser, token, host_url):
    message = mail.EmailMessage()
    message.sender = "The Lazy Gibbon <ben.tilly@gmail.com>"
    message.subject = "Welcome to The Lazy Gibbon"
    toString = tlguser.name
    toString += " <"
    toString += tlguser.email
    toString += ">"
    message.to = toString
    message.body = "Hi "
    message.body += tlguser.name
    message.body += '\n\nThanks for signing up with The Lazy Gibbon. Please confirm your email address by clicking the following link:\n'
    message.body += host_url #append the server / host URL that is processing this request
    message.body += "/signup/confirmEmail?token="
    message.body += str( token.key.urlsafe() )
    
    logging.info(message.body)
    
    message.send() 
    return