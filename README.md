Elastic Search API for tsuru PaaS
=================================

[![Build Status](https://travis-ci.org/globocom/elastic-search-api.svg)](https://travis-ci.org/globocom/elastic-search-api)

The API goal is to create a communication pipe between tsuru and Elastic Search service.

Installation
------------

It's really easy to install the API using tsuru.

First, you need to create a new app (I'm assuming you already are authenticated and all setup):

    $> tsuru app-create elastic-search-api
    $> git remote add tsuru git@remote-here

After the app status change to started you can push the API code to the newly created vm:

    $> git push tsuru master

If everything works as expected, you should access your vm url/ip (use tsuru app-list to find it) and get a 401,
because the API is protected by basic auth. The default username / password is specified by two environment variables:

```
ES_BROKER_USERNAME
ES_BROKER_PASSWORD
```
Which if not set, default to admin / password. Once you have authenticated, you should receive a 404 on a GET request to
'/' as the web app has no default route.

Configuration
-------------

With the API set up, you should tell it where the Elasticsearch instance is, for that you should use
the `ELASTICSEARCH_HOST` environment variable, to export that variable using tsuru, run the following command:

    $> tsuru env-set elastic-search-api ELASTICSEARCH_HOST=yourelasticsearchurl.com

If your elasticsearch server is running on a port other than 9200 you can change the port by setting an environment variable:

    $> tsuru env-set elastic-search-api ELASTICSEARCH_PORT=20001


To generate a service mainifest, copy service.yaml.example to manifest.yaml, changing the endpoint to the correct elastic
search server.

Now we have to tell tsuru (using crane cmd line) that it has a new service available, do that by running the following:

    $> crane create path/to/manifest.yaml


That's it! You can check if everything worked fine by running:

    $> tsuru service-list

The output should be something like that:

    +----------------+-----------+
    | Services       | Instances |
    +----------------+-----------+
    | elastic-search |           |
    +----------------+-----------+

Common problems
---------------

- API doesn't load: this is probably an access problem at the IaaS level, try to telnet the API vm in the port the API is running (in this case, 80), if it doesn't work, try to open port 80, if you have no access to do that, call someone that has :)

ToDo
----

 * Add multi-tenancy support.
 * Improve security model.
