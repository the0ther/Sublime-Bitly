# Bit.ly Sublime Plugin

Hello, this is a small plugin I've put together based on [a demo I found on the web at Nettuts+](http://bit.ly/HdS3BQ).

I find the URL-shortening service [Bit.ly](http://bitly.com) to be quite handy. Short URLs are aesthetically pleasing, to be sure. The thing I really like about Bit.ly though are the reports I can get about shortened links I've sent others.

_This is an early release._

## Settings

The only settings for this plugin are account-related. You can use this plugin with your own account by using the following settings:

```
{
	"api_login": "<YOUR_BITLY_USERNAME_HERE>",
	"api_key": "<YOUR_API_KEY_HERE>"
}
```

To get a new API key from Bit.ly [visit this link](https://bitly.com/a/your_api_key).

## Todos

* Add instructions for obtaining API from Bit.ly.
* Add in contextual menu, so you can choose 1 URL to shorten

## Issues

1. Needs tests
2. The regular expression used to detect URLs is not well-tested.