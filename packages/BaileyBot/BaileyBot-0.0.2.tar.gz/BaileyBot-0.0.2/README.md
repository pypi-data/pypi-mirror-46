BaileyBot is a GMAIL client that can very simply, send emails.

Here is an example script:

```python
import BaileyBot
email = BaileyBot.signIn('JohnSmith@example.com', 'password')
email.sendEmail('Bob@example.com', 'Example Subject', 'Example Body')
```
This package has not yet added OAuth2, however that will be added in the future.

For further installation details, documentation, and the roadmap, go to https://sites.google.com/view/python3-baileybot
