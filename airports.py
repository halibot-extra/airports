from halibot import CommandModule
import urllib.request
import json

class Airports(CommandModule):

    HAL_MINIMUM = "0.2.0"

    topics = {
        'airport': '''Quert airport status.

Usage:
  !airport <three-letter airport code> '''
    }

    def init(self):
        self.commands = {
            'airport': self.airport
        }

    def airport(self, ap, msg):
        if ap != '':
            try:
                url = 'http://services.faa.gov/airport/status/{}?format=application/json'.format(ap)
                req = urllib.request.urlopen(url)
                data = json.loads(req.read().decode('utf-8'))

                weather = 'Weather at {name} is {weather[weather]}, {weather[temp]}, wind {weather[wind]}, visibility {weather[visibility]}.'.format(**data)

                if data['delay'] == 'true':
                    delay = 'There is a delay due to {status[reason]}. The average delay time is {status[avgDelay]}.'.format(**data)
                else:
                    delay = 'There are no known delays.'

                self.reply(msg, body=weather + '\n' + delay)
            except urllib.error.HTTPError:
                self.reply(msg, body='Cannot find airport "{}".'.format(ap))
