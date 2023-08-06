import random
import re
import itertools
import json
import datetime
import datetime
import traceback
import re
import sys

try:
    import dhttp

except ImportError:
    import __init__ as dhttp


PORT = (random.randint(8000, 8050) if sys.argv[1] == 'random' else (int(sys.argv[1]) if len(sys.argv) > 1 else 8000))

app = dhttp.DHTTPServer()

class AntiControlChar(object):
    def __init__(self):
        control_chars = ''.join(re.escape(chr(c)) for c in itertools.chain(range(0,32), range(127,160)))
        self.control_char_re = re.compile('[%s]' % control_chars)

    def strip_control(self, s):
        return self.control_char_re.sub('', s)

acc = AntiControlChar()

app.alias('/index', '/')
app.alias('/index.htm', '/')
app.alias('/index.html', '/')

test_index = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>My first DHTTP server</title>
</head>

<body>
    <p><h2>Congratulations!</h2></p>
    <hr>
    <p><b>dhttp {version}</b> is now running on your machine.</p>
    <p>How about <i>{party}</i> to comemorate? :)</p>
    <br/>
    <p><small>{time}</small></p>
</body>
</html>"""

party_stuff = [
    'a bottle of wine', 'a bottle of champagne', 'a big party',
    'THE party, just', 'THE party', 'lots of cats', 'partyception',
    'balloons and cakes', 'a big-endian cake', 'lots of confetti',
    'the Confetti-o-Tron 2000', 'HTTP juice', 'Spicy Bytes',
    'antimatter', 'cats writing code', 'a smile breaking the 4th wall'
]

@app.get('/')
def serve_index(req, res):
    res.end(test_index.format(
        party = res['party'],
        time = res['time'],
        version = dhttp.DHTTP_VERSION
    ))

@app.on_log
def print_log(log):
    if log.request.get_header('X-Forwarded-For') is not None:
        log.ip = log.request.get_header('X-Forwarded-For')
        print(log, '  (forwarded)')

    else:
        print(log)

@app.use()
def set_party(req, res):
    this_party = random.choice(party_stuff)
    res['party'] = this_party

    utc = datetime.datetime.utcnow()
    res['time'] = f"Right now, in the UTC, this {utc.strftime('%A')} it's {utc.strftime('%H:%M:%S')}."

    if req.resolve_path() == '/':
        print(dhttp.DHTTPGenericLog("PARTY", f"And now, {this_party} to comemorate!"))

app.static('/static',  './static')
app.static('/src/jinja', './static/jinja')

log = []
clients = set()
nick = {}
bad = set()

@app.jinja_folder('/jinja', './static/jinja')
async def jinja_folder(req, set, done):
    set('utctime', datetime.datetime.utcnow().strftime('%H:%M:%S'))
    set('upper_log', log)
    set('regex', re)
    done()

@app.websocket('/ws/upper')
def uppercase_stuff(client, req):
    if req.get_header('X-Forwarded-For') is not None:
        ip = req.get_header('X-Forwarded-For')

    else:
        ip = ':'.join(str(comp) for comp in client.address)

    idhex = hex(id(client))[2:]
    clients.add(client) 

    print(dhttp.DHTTPGenericLog('CHAT', f"New connection received: {idhex} ({ip})"))

    @client.ws_receiver
    def make_me_uppercase(data):
        try:
            msg = json.loads(data.content.decode('utf-8'))

        except json.JSONDecodeError:
            return

        if not isinstance(msg, dict):
            return

        if 'content' not in msg or 'type' not in msg:
            return

        msg['content'] = acc.strip_control(msg['content'][:400])

        if msg['type'] == 'message' and idhex in nick and idhex not in bad:
            print(dhttp.DHTTPGenericLog('CHAT', f" (MSG)  <{nick[idhex]}> {msg['content']}"))
            log.append(f"<{nick[idhex]}> {msg['content']}")

            for c in clients:
                c.ws_write(f"MSG {json.dumps([nick[idhex], msg['content']])}")

        elif msg['type'] == 'nick':
            msg['content'] = msg['content'][:40]

            old_nick_r = nick.get(idhex, None)
            old_nick = old_nick_r and '"' + old_nick_r + '"' or ''
            new_nick = '"' + msg['content'] + '"'

            if msg['content'] == '' or msg['content'] not in nick.values():
                if idhex in bad:
                    bad.remove(idhex)

                nick[idhex] = msg['content']
                client.ws_write(f"NICK yes")

                if old_nick_r is None:
                    print(dhttp.DHTTPGenericLog('CHAT', f"Join from {ip}; {idhex} ({new_nick})"))
                    log.append(f"->> msg['content'] has joined")

                    for c in clients:
                        c.ws_write(f"JOIN {msg['content']}")

                else:
                    print(dhttp.DHTTPGenericLog('CHAT', f"Nickname change from {ip}; {idhex} ({old_nick}) now known as {new_nick}"))

                    for c in clients:
                        c.ws_write(f"CHNICK {json.dumps([old_nick_r, msg['content']])}")

                log.append(f"*** {old_nick_r} is now known as {msg['content']}")

            else:
                bad.add(idhex)
                client.ws_write(f"NICK no")

    @client.on_close
    def make_me_dead(_):
        clients.remove(client)
        print(dhttp.DHTTPGenericLog('CHAT', f"Connection closed: {idhex} ({ip})"))

        if idhex in nick:
            n = nick[idhex]

            log.append(f"<<- {n} has left")

            for c in clients:
                c.ws_write(f"PART {n}")

            del nick[idhex]

@app.on_response_finish
def on_served(req, res):
    print(dhttp.DHTTPGenericLog("INFO", f"Served {req.method} to '{req.path}'"))    

@app.on_response_error
def catch_error(call, err):
    print(dhttp.DHTTPGenericLog("ERR!", f'Caught {type(err).__name__} trying to run {call[3]}! Ignoring...'))
    print(f' -> {str(err)}')
    traceback.print_tb(err.__traceback__)

app.add_port(PORT)
app.add_port(PORT + 1,
    tls = True,
    cert_mode = dhttp.tcp.CertMode.CM_GENERATED,
    cert_file = '.server.demo.cert.pem',
    key_file = '.server.demo.key.pem'
)

@app.run_forever()
def on_serve():
    print(f"\n   == Listening on ports: {', '.join(str(serv[0]) for serv in app.tcp_servers)} ==\n")