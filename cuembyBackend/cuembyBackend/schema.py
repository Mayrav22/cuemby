import graphene
import graphql_jwt
import players.schema
class QueryLogin(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()

class MutationLogin(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schemaLogin = graphene.Schema(query=QueryLogin, mutation=MutationLogin)



class Query(
    players.schema.Query,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)