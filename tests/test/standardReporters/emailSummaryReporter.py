"""

"""

import os
import pprint
import smtplib
from email.mime.text import MIMEText

import assetQC.api.reporter as reporter
import assetQC.api.register as register
import assetQC.api.context as context
import assetQC.api.utils as utils


class EmailSummaryReporter(reporter.Reporter):

    # static variables
    enable = True
    priority = 2
    assetTypes = []
    hostApps = []

    def __init__(self):
        super(EmailSummaryReporter, self).__init__()

    def condition(self, ctx):
        return True

    def run(self, ctx):
        senderAddr = ctx.getUserEmailAddress()
        recipentAddr = ctx.getUserEmailAddress()

        emailMessage = 'Assets QC Summary' + os.linesep + os.linesep
        emailMessage += 'Context:' + os.linesep
        emailMessage += 'User = ' + ctx.getUserName() + os.linesep
        emailMessage += 'User Email = ' + ctx.getUserEmailAddress() + os.linesep
        emailMessage += 'Host Application = ' + ctx.getHostApp() + os.linesep
        emailMessage += 'Host Name = ' + ctx.getHostName() + os.linesep
        emailMessage += 'Data = ' + os.linesep
        emailMessage += pprint.pformat(ctx.data) + os.linesep + os.linesep

        lines = utils.formatInstances(ctx, True)
        emailMessage += '==-- PASSED --==' + os.linesep
        emailMessage += str(os.linesep).join(lines)
        emailMessage += os.linesep + os.linesep

        lines = utils.formatInstances(ctx, False)
        emailMessage += '==-- FAILED --==' + os.linesep
        emailMessage += str(os.linesep).join(lines)
        emailMessage += os.linesep + os.linesep

        # Create a text/plain message
        msg = MIMEText(emailMessage)
        msg['Subject'] = 'My test email'
        msg['From'] = senderAddr
        msg['To'] = recipentAddr
        # print 'msg', msg

        # # Send the message via our own SMTP server, but don't include the
        # # envelope header.
        # hostName = ctx.getHostName()
        # s = smtplib.SMTP(hostName)
        # s.sendmail(senderAddr, [recipentAddr], msg.as_string())
        # s.quit()

        return


manager = register.getPluginManager()
manager.registerPlugin(EmailSummaryReporter)
