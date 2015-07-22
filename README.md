Elastic Search API for tsuru PaaS
=================================

The API goal is to create a communication pipe between tsuru and Elastic Search service.

Installation
------------

It's really easy to install the API using tsuru.

First, you need to create a new app (I'm assuming you already are authenticated and all setup):

    $> tsuru app-create elastic-search-api
    $> git remote add tsuru git@remote-here

After the app status change to started you can push the API code to the newly created vm:

    $> git push tsuru master

If everything works as expected, you should access your vm url/ip (use tsuru app-list to find it) and get a 404,
because the API does not have a route to /.

Configuration
-------------

With the API set up, you should tell it where is the Elastic Search machine (or vm perhaps), for that you should use
the `ELASTIC_SEARCH_URL` environment variable, to export that variable using tsuru, run the following command:

    $> tsuru env-set elastic-search-api ELASTIC_SEARCH_URL=yourelasticsearchurl.com:9200

Now we have to tell tsuru (using crane cmd line) that it has a new service available, do that by running the following:

    $> crane create path/to/manifest.yaml

The manifest.yaml file is contained in the API repository.

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
