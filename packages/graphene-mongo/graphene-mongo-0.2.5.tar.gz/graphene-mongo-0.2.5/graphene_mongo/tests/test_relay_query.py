import base64
import os
import pytest

import graphene

from graphene.relay import Node

from .setup import fixtures, fixtures_dirname
from .models import Article, Reporter
from .nodes import (ArticleNode,
                    EditorNode,
                    PlayerNode,
                    ReporterNode,
                    ChildNode,
                    ParentWithRelationshipNode,
                    ProfessorVectorNode,)
from ..fields import MongoengineConnectionField


def get_nodes(data, key):
    return map(lambda edge: edge['node'], data[key]['edges'])


def test_should_query_reporter(fixtures):

    class Query(graphene.ObjectType):
        reporter = graphene.Field(ReporterNode)

        def resolve_reporter(self, *args, **kwargs):
            return Reporter.objects.first()

    query = '''
        query ReporterQuery {
            reporter {
                firstName,
                lastName,
                email,
                awards,
                articles {
                    edges {
                        node {
                            headline
                        }
                    }
                },
                embeddedArticles {
                    edges {
                        node {
                            headline
                        }
                    }
                },
                embeddedListArticles {
                    edges {
                        node {
                            headline
                        }
                    }
                },
                genericReference {
                    __typename
                    ... on ArticleNode {
                        headline
                    }
                }
            }
        }
    '''
    expected = {
        'reporter': {
            'firstName': 'Allen',
            'lastName': 'Iverson',
            'email': 'ai@gmail.com',
            'awards': ['2010-mvp'],
            'articles': {
                'edges': [
                    {
                        'node': {
                            'headline': 'Hello'
                        }
                    },
                    {
                        'node': {
                            'headline': 'World'
                        }
                    }
                ],
            },
            'embeddedArticles': {
                'edges': [
                    {
                        'node': {
                            'headline': 'Real'
                        }
                    },
                    {
                        'node': {
                            'headline': 'World'
                        }
                    }
                ],
            },
            'embeddedListArticles': {
                'edges': [
                    {
                        'node': {
                            'headline': 'World'
                        }
                    },
                    {
                        'node': {
                            'headline': 'Real'
                        }
                    }
                ],
            },
            'genericReference': {
                '__typename': 'ArticleNode',
                'headline': 'Hello'
            }
        }
    }

    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data['reporter'] == expected['reporter']


def test_should_query_reporters_with_nested_document(fixtures):

    class Query(graphene.ObjectType):
        reporters = MongoengineConnectionField(ReporterNode)

    query = '''
        query ReporterQuery {
            reporters(firstName: "Allen") {
                edges {
                    node {
                        firstName,
                        lastName,
                        email,
                        articles(headline: "Hello") {
                             edges {
                                  node {
                                       headline
                                  }
                             }
                        }
                    }
                }
            }
        }
    '''
    expected = {
        'reporters': {
            'edges': [
                {
                    'node': {
                        'firstName': 'Allen',
                        'lastName': 'Iverson',
                        'email': 'ai@gmail.com',
                        'articles': {
                            'edges': [
                                {
                                    'node': {
                                        'headline': 'Hello'
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }

    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data['reporters'] == expected['reporters']


def test_should_query_all_editors(fixtures, fixtures_dirname):

    class Query(graphene.ObjectType):
        editors = MongoengineConnectionField(EditorNode)

    query = '''
        query EditorQuery {
          editors {
            edges {
                node {
                    id,
                    firstName,
                    lastName,
                    avatar {
                        contentType,
                        length,
                        data
                    }
                }
            }
          }
        }
    '''

    avator_filename = os.path.join(fixtures_dirname, 'image.jpg')
    with open(avator_filename, 'rb') as f:
        data = base64.b64encode(f.read())

    expected = {
        'editors': {
            'edges': [
                {
                    'node': {
                        'id': 'RWRpdG9yTm9kZTox',
                        'firstName': 'Penny',
                        'lastName': 'Hardaway',
                        'avatar': {
                            'contentType': 'image/jpeg',
                            'length': 46928,
                            'data': str(data)
                        }
                    }
                },
                {
                    'node': {
                        'id': 'RWRpdG9yTm9kZToy',
                        'firstName': 'Grant',
                        'lastName': 'Hill',
                        'avatar': {
                            'contentType': None,
                            'length': 0,
                            'data': None
                        }
                    }

                },
                {
                    'node': {
                        'id': 'RWRpdG9yTm9kZToz',
                        'firstName': 'Dennis',
                        'lastName': 'Rodman',
                        'avatar': {
                            'contentType': None,
                            'length': 0,
                            'data': None
                        }
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data['editors'] == expected['editors']


def test_should_filter_editors_by_id(fixtures):

    class Query(graphene.ObjectType):
        node = Node.Field()
        all_editors = MongoengineConnectionField(EditorNode)

    query = '''
        query EditorQuery {
          allEditors(id: "RWRpdG9yTm9kZToy") {
            edges {
                node {
                    id,
                    firstName,
                    lastName
                }
            }
          }
        }
    '''
    expected = {
        'allEditors': {
            'edges': [
                {
                    'node': {
                        'id': 'RWRpdG9yTm9kZToy',
                        'firstName': 'Grant',
                        'lastName': 'Hill'
                    }

                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert dict(result.data['allEditors']) == expected['allEditors']


def test_should_filter(fixtures):

    class Query(graphene.ObjectType):
        node = Node.Field()
        articles = MongoengineConnectionField(ArticleNode)

    query = '''
        query ArticlesQuery {
            articles(headline: "World") {
                edges {
                    node {
                        headline,
                        pubDate,
                        editor {
                            firstName
                        }
                    }
                }
            }
        }
    '''
    expected = {
        'articles': {
            'edges': [
                {
                    'node': {
                        'headline': 'World',
                        'editor': {
                            'firstName': 'Grant'
                        },
                        'pubDate': '2020-01-01T00:00:00'
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_filter_by_reference_field(fixtures):

    class Query(graphene.ObjectType):
        node = Node.Field()
        articles = MongoengineConnectionField(ArticleNode)

    query = '''
        query ArticlesQuery {
            articles(editor: "RWRpdG9yTm9kZTox") {
                edges {
                    node {
                        headline,
                        editor {
                            firstName
                        }
                    }
                }
            }
        }
    '''
    expected = {
        'articles': {
            'edges': [
                {
                    'node': {
                        'headline': 'Hello',
                        'editor': {
                            'firstName': 'Penny'
                        }
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_filter_through_inheritance(fixtures):

    class Query(graphene.ObjectType):
        node = Node.Field()
        children = MongoengineConnectionField(ChildNode)

    query = '''
        query ChildrenQuery {
            children(bar: "bar") {
                edges {
                    node {
                        bar,
                        baz,
                        loc {
                             type,
                             coordinates
                        }
                    }
                }
            }
        }
    '''
    expected = {
        'children': {
            'edges': [
                {
                    'node': {
                        'bar': 'bar',
                        'baz': 'baz',
                        'loc': {
                             'type': 'Point',
                             'coordinates': [10.0, 20.0]
                        }
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_filter_by_list_contains(fixtures):
    # Notes: https://goo.gl/hMNRgs
    class Query(graphene.ObjectType):
        reporters = MongoengineConnectionField(ReporterNode)

    query = '''
        query ReportersQuery {
            reporters (awards: "2010-mvp") {
                edges {
                    node {
                        id,
                        firstName,
                        awards
                    }
                }
            }
        }
    '''
    expected = {
        'reporters': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3J0ZXJOb2RlOjE=',
                        'firstName': 'Allen',
                        'awards': ['2010-mvp']
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_filter_by_id(fixtures):
    # Notes: https://goo.gl/hMNRgs
    class Query(graphene.ObjectType):
        reporter = Node.Field(ReporterNode)

    query = '''
        query ReporterQuery {
            reporter (id: "UmVwb3J0ZXJOb2RlOjE=") {
                id,
                firstName,
                awards
            }
        }
    '''
    expected = {
        'reporter': {
            'id': 'UmVwb3J0ZXJOb2RlOjE=',
            'firstName': 'Allen',
            'awards': ['2010-mvp']
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_first_n(fixtures):

    class Query(graphene.ObjectType):

        editors = MongoengineConnectionField(EditorNode)

    query = '''
        query EditorQuery {
            editors(first: 2) {
                edges {
                    cursor,
                    node {
                        firstName
                    }
                }
                pageInfo {
                    hasNextPage
                    hasPreviousPage
                    startCursor
                    endCursor
                }
            }
        }
    '''
    expected = {
        'editors': {
            'edges': [
                {
                    'cursor': 'xxx',
                    'node': {
                        'firstName': 'Penny'
                    }
                },
                {
                    'cursor': 'xxx',
                    'node': {
                        'firstName': 'Grant'
                    }
                }
            ],
            'pageInfo': {
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'xxx',
                'endCursor': 'xxx'
            }
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)

    assert not result.errors
    assert all(item in get_nodes(result.data, 'editors')
               for item in get_nodes(expected, 'editors'))


def test_should_after(fixtures):
    class Query(graphene.ObjectType):

        players = MongoengineConnectionField(PlayerNode)

    query = '''
        query EditorQuery {
            players(after: "YXJyYXljb25uZWN0aW9uOjA=") {
                edges {
                    cursor,
                    node {
                        firstName
                    }
                }
            }
        }
    '''
    expected = {
        'players': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'firstName': 'Magic',
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'firstName': 'Larry'
                    }
                },
                {
                     'cursor': 'YXJyYXljb25uZWN0aW9uOjM=',
                     'node': {
                        'firstName': 'Chris'
                     }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)

    assert not result.errors
    assert result.data == expected


def test_should_before(fixtures):
    class Query(graphene.ObjectType):

        players = MongoengineConnectionField(PlayerNode)

    query = '''
        query EditorQuery {
            players(before: "YXJyYXljb25uZWN0aW9uOjI=") {
                edges {
                    cursor,
                    node {
                        firstName
                    }
                }
            }
        }
    '''
    expected = {
        'players': {
            'edges': [
                {
                    'cursor': "YXJyYXljb25uZWN0aW9uOjA=",
                    'node': {
                        'firstName': 'Michael',
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'firstName': 'Magic',
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)

    assert not result.errors
    assert result.data == expected


def test_should_last_n(fixtures):
    class Query(graphene.ObjectType):
        players = MongoengineConnectionField(PlayerNode)

    query = '''
        query PlayerQuery {
            players(last: 2) {
                edges {
                    cursor,
                    node {
                        firstName
                    }
                }
            }
        }
    '''
    expected = {
        'players': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'firstName': 'Larry',
                    }
                },
                {
                     'cursor': 'YXJyYXljb25uZWN0aW9uOjM=',
                     'node': {
                          'firstName': 'Chris'
                     }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)

    assert not result.errors
    assert result.data == expected


def test_should_self_reference(fixtures):

    class Query(graphene.ObjectType):

        all_players = MongoengineConnectionField(PlayerNode)

    query = '''
        query PlayersQuery {
            allPlayers {
                edges {
                    node {
                        firstName,
                        players {
                            edges {
                                node {
                                    firstName
                                }
                            }
                        },
                        embeddedListArticles {
                            edges {
                                node {
                                    headline
                                }
                            }
                        }
                    }
                }
            }
        }
    '''
    expected = {
        'allPlayers': {
            'edges': [
                {
                    'node': {
                        'firstName': 'Michael',
                        'players': {
                            'edges': [
                                {
                                    'node': {
                                        'firstName': 'Magic'
                                    }
                                }
                            ]
                        },
                        'embeddedListArticles': {
                            'edges': []
                        }
                    }
                },
                {
                    'node': {
                        'firstName': 'Magic',
                        'players': {
                            'edges': [
                                {
                                    'node': {
                                        'firstName': 'Michael'
                                    }
                                }
                            ]
                        },
                        'embeddedListArticles': {
                            'edges': []
                        }

                    }
                },
                {
                    'node': {
                        'firstName': 'Larry',
                        'players': {
                            'edges': [
                                {
                                    'node': {
                                        'firstName': 'Michael'
                                    }
                                },
                                {
                                    'node': {
                                        'firstName': 'Magic'
                                    }
                                }
                            ]
                        },
                        'embeddedListArticles': {
                            'edges': []
                        }
                    }
                },
                {
                     'node': {
                          'firstName': 'Chris',
                          'players': {
                              'edges': []
                          },
                          'embeddedListArticles': {
                               'edges': []
                          }
                     }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_lazy_reference(fixtures):

    class Query(graphene.ObjectType):
        node = Node.Field()
        parents = MongoengineConnectionField(ParentWithRelationshipNode)

    schema = graphene.Schema(query=Query)

    query = """
    query {
        parents {
            edges {
                node {
                    beforeChild {
                        edges {
                            node {
                                name,
                                parent { name }
                            }
                        }
                    },
                    afterChild {
                        edges {
                            node {
                                name,
                                parent { name }
                            }
                        }
                    }
                }
            }
        }
    }
    """

    expected = {
        "parents": {
            "edges": [
                {"node": {
                    "beforeChild": {
                        "edges": [
                            {"node": {
                                "name": "Akari",
                                "parent": {"name": "Yui"}
                            }}
                        ]
                    },
                    "afterChild": {
                        "edges": [
                            {"node": {
                                "name": "Kyouko",
                                "parent": {"name": "Yui"}
                            }}
                        ]
                    }
                }}
            ]
        }
    }

    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_query_with_embedded_document(fixtures):

    class Query(graphene.ObjectType):

        all_professors = MongoengineConnectionField(ProfessorVectorNode)

    query = '''
    query {
        allProfessors {
            edges {
                node {
                    vec,
                    metadata {
                        firstName
                    }
                }
            }
        }
    }
    '''
    expected = {
        'allProfessors': {
            'edges': [
                {
                    'node': {
                        'vec': [1.0, 2.3],
                        'metadata': {
                             'firstName': 'Steven'
                        }
                    }

                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert dict(result.data['allProfessors']) == expected['allProfessors']


def test_should_get_queryset_returns_dict_filters(fixtures):

    class Query(graphene.ObjectType):
        node = Node.Field()
        articles = MongoengineConnectionField(ArticleNode, get_queryset=lambda *_, **__: {"headline": "World"})

    query = '''
           query ArticlesQuery {
               articles {
                   edges {
                       node {
                           headline,
                           pubDate,
                           editor {
                               firstName
                           }
                       }
                   }
               }
           }
       '''
    expected = {
        'articles': {
            'edges': [
                {
                    'node': {
                        'headline': 'World',
                        'editor': {
                            'firstName': 'Grant'
                        },
                        'pubDate': '2020-01-01T00:00:00'
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected


def test_should_get_queryset_returns_qs_filters(fixtures):

    def get_queryset(model, info, **args):
        return model.objects(headline="World")

    class Query(graphene.ObjectType):
        node = Node.Field()
        articles = MongoengineConnectionField(ArticleNode, get_queryset=get_queryset)

    query = '''
           query ArticlesQuery {
               articles {
                   edges {
                       node {
                           headline,
                           pubDate,
                           editor {
                               firstName
                           }
                       }
                   }
               }
           }
       '''
    expected = {
        'articles': {
            'edges': [
                {
                    'node': {
                        'headline': 'World',
                        'editor': {
                            'firstName': 'Grant'
                        },
                        'pubDate': '2020-01-01T00:00:00'
                    }
                }
            ]
        }
    }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected
