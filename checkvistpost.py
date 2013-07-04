import restkit, json, logging
logging.basicConfig(level=logging.WARN)
config = json.load(open("config.json"))
cv = restkit.Resource("http://checkvist.com/")
token = json.loads(cv.post(
    "auth/login.json",
    username=config['username'],
    remote_key=config['remote_key'],
  ).body_string())
print "token %r" % token

cv.post("checklists/%s/tasks.json" % config['checklist_id'], **{
    'token': token,
    'task[content]': 'demo1',
    'task[position]': 1,
})
