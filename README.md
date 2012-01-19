WHAT IS THIS
============

This is the source code of the website http://cleanjscode.appspot.com
Javascript code review/checkstyle tool.

It is based on [cleanjs](https://github.com/captainbrosset/cleanjs) also developed by myself.

The website uses the Google App Engine SDK and infrastructure.

There's still a lot of work on the cleanjs tool itself, but at least now there's a website to run it easily.

Note that I haven't done anything special yet to manage the dependency from the website to cleanjs, so it is required to copy the required cleanjs version into the root folder of the website before deploying to prod.

TODO
====

- achievements, gifs for winners!
- run stats on the whole code submitted so far
- open REST service to integrate in other tools (service hook from github)
- optionally give possibility to identify code that was reviewed already in order to generate a widget with grade
- avoid to submit empty codes
- do a hash of the submitted code to avoid adding codes in DB that is already there
- cursor pointer on buttons
- button to upload, next to the review
- textfield to put url of code to review