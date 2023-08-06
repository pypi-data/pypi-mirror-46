# SMSframework AfricasTalking Provider

[Africa's Talking] Provider for [smsframework]

[Africa's Talking]: https://africastalking.com/
[smsframework]: https://pypi.python.org/pypi/smsframework/

# Initialization

```
from smsframework import Gateway
from smsframework_africastalking import AfricasTalkingProvider

gateway = Gateway()
gateway.add_provider('africas_talking', AfricasTalkingProvider,
    username='sandbox',
    api_key='\*\*\*'
)
```

## Config

- `username: str`: Username for your Africa's Talking account, use `sandbox` for development `Required`
- `api_key: str`: API key for your Africa's Talking account `Required`

# Sending Parameters

Provider-specific sending params:

- `target_country: str`: 2-digit ISO code of the country the phonenumber should be interpretted as from `Required`

Example:

```
from smsframework import OutgoingMessage

message = OutgoingMessage('+254789789789', 'Hello Kenya').params(target_country='KE')

gateway.send(message)
```

# Additional Information

AfricasTalking SMS API also supports sending premium messages and receiving incoming messages. These features are not currently implemented in this provider.