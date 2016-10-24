from halibot import HalModule
import urllib.request
import json

class Airports(HalModule):

    def airport(self, ap, msg):
        try:
            url = 'http://services.faa.gov/airport/status/{}?format=application/json'.format(ap)
            req = urllib.request.urlopen(url)
            data = json.loads(req.readall().decode('utf-8'))

            weather = 'Weather at {name} is {weather[weather]}, {weather[temp]}, wind {weather[wind]}, visibility {weather[visibility]}.'.format(**data)

            if data['delay'] == 'true':
                delay = 'There is a delay due to {status[reason]}. The average delay time is {status[avgDelay]}.'.format(**data)
            else:
                delay = 'There are no known delays.'

            self.reply(msg, body=weather + '\n' + delay)
        except urllib.error.HTTPError:
            self.reply(msg, body='Cannot find airport "{}".'.format(ap))

    def receive(self, msg):
        cmd = msg.body.split(' ')

        if cmd[0] == '!airport':
            for ap in cmd[1:]:
                if ap != '':
                    self.airport(ap, msg)
