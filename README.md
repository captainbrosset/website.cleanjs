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

- Save reports and link them with padlessb64 urls
- header separated
- colors to be revised. Maybe icons rather than colors. Nice embossed
- grade reports, run stats (grade= % of errors/warn per file lines)
- achievements
- allow upload, url, textarea