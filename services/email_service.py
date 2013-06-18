import logging
from google.appengine.api import mail


def sendResetPasswordEmail(tlguser):
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
    message.body += "thelazygibbonapi.appspot.com/reset/resetPasswordPage?resetToken="
    message.body += str(tlguser.resetToken)
    message.send()
    return

def sendGroupInviteEmail(invite):
    inviter = invite.invited_by.get().name
    groupName = invite.group.get().name
    #send email to intitee
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
    message.body += "thelazygibbonapi.appspot.com/groupInvite/invitePage?inviteKey="
    message.body += str(invite.key.urlsafe())
    message.body += '\n\n Otherwise ignore this message' 
    
    message.send() 
    return