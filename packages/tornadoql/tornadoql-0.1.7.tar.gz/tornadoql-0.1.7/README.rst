A `Tornado <http://www.tornadoweb.org/>`__ boilerplate for
`Graphene <http://graphene-python.org/>`__ with subscriptions.

Installation
------------

.. code:: sh

    git clone https://github.com/deep-compute/tornadoql
    cd tornadoql
    python setup.py install

Using
-----

A very easy to use, fully extensible Tornado Web Server Integration with
Graphene to make serving GraphQL APIs, including Websocket
subscriptions, as easy as defining your schema.

With TornadoQL, exposing a graphene schema as a GraphQL API takes two
imports and one line of code. You can also make that API part of a
larger application by simply adding to the GraphQL endpoints and Tornado
application settings before calling start. Getting your own API-only
server up is as simple as defining a Graphene schema and the following
code:

.. code:: python

    import graphene
    from tornadoql import TornadoQL

    class TestType(graphene.ObjectType):
        id = graphene.ID()
        value = graphene.String()

    class Query(graphene.ObjectType):
        test = graphene.Field(TestType)

        def resolve_test(self, info):
            return TestType(id='1', value='test value')

    schema = graphene.Schema(query=Query)

    tql = TornadoQL(schema)
    tql.start()

This will start a server with ``/graphql``, ``/graphiql``, and
``/subscriptions`` endpoints, supporting optional arguments for port and
application settings. TornadoQL includes an extended version of graphiql
GraphQL browser that supports subscriptions as well as queries and
mutations.

::

    $ python example_app.py run
    2019-05-07T12:21:19.371580Z [info     ] starting_server                host=prashanth-dev id=20190507T122119_9e53062670c211e984939600001c5856 name=example_app.py type=log urls={'graphiql': 'http://localhost:8888/graphiql', 'queries_and_mutations': 'http://localhost:8888/graphql', 'subscriptions': 'ws://localhost:8888/subscriptions'}
