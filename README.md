multipart (mcurl.py or multiple curl)
=====================================

A python 2.7 script which uses cURL to download a file in multiple parts simultaneously. This can significantly accelerate download time, especially for large files.

### Usage

    python mcurl.py output_name url

or

    import mcurl

    mcurl.multi_curl(destination, url)
