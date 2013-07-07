#!bin/python
import json, logging, email, urllib
import klein
from twisted.web.client import getPage
from twisted.internet.defer import inlineCallbacks
logging.basicConfig(level=logging.WARN)

CHECKVIST = "http://checkvist.com"

config = json.load(open("config.json"))

def tasksUri():
    return CHECKVIST + "/checklists/%s/tasks.json" % str(config['checklist_id'])

@inlineCallbacks
def postTask(taskText):
    result = yield getPage(CHECKVIST + "/auth/login.json", method="POST",
                postdata=urllib.urlencode({
                    'username': config['username'],
                    'remote_key': config['remote_key'],
                    }))
    token = json.loads(result)

    yield getPage(tasksUri(), method="POST",
                postdata=urllib.urlencode({
                    'token': token,
                    'task[content]': taskText,
                    'task[position]': 1,
                }))

@klein.route('/')
def index(request):
    return ('POST an email message to <a href="/newmail">newmail</a> '
            'to add a task. The email subject line becomes the task text.')
    
@klein.route('/newmail', methods=['POST'])
def newmail(request):
    msg = email.message_from_file(request.content)
    subject = msg['subject']
    if subject is None:
        raise ValueError("no subject found")
    
    done = postTask(subject)
    done.addCallback(lambda result: "ok")
    return done

klein.run('0.0.0.0', port=9108)
