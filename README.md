# Airtime Notifier

Log where you left your favorite tv shows and this project will crawl the airtimes to notify you via email.

## Installation

`git clone https://github.com/guvenonur/airtime.git`

## Getting Started

```
docker-compose build --no-cache --parallel && docker-compose up
```

### Test

Check `http://localhost:5000/`

## How It Works
#### Homepage
Add your tv-show

![homepage](/static/images/homepage.png)
#### TV Show List
Edit your TV show list

![show_list](/static/images/show_list.png)

#### Send Mail
Enter your e-mail and send notification

![send_mail](/static/images/send_mail.png)

#### Thank You
After you are forwarded to Thank you page, application is crawling the airtimes in the background and preparing the mail. Check your e-mail.

![thank_you](/static/images/thank_you.png)

#### Check Your E-mail
You will find your airtime notifications in your e-mail in a few seconds.

![mail](/static/images/mail.png)

## Acknowledgements
* Big shout out to all my colleagues for helping and guiding me through it all, especially `Egemen Zeytinci` and `Tarık Yılmaz`.
