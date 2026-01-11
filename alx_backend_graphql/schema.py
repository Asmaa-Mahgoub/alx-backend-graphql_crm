import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
<<<<<<< HEAD
    hello = graphene.String(default_value="Hello, GraphQL!")
=======
    pass
>>>>>>> 74fab26 (Scheduling and Automating Tasks)

class Mutation(CRMMutation, graphene.ObjectType):
    pass

<<<<<<< HEAD
schema = graphene.Schema(query=Query, mutation=Mutation)
=======
schema = graphene.Schema(query=Query, mutation=Mutation)
>>>>>>> 74fab26 (Scheduling and Automating Tasks)
