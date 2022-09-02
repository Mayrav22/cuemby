
from email.policy import default
import graphene
from players.models import *
from graphene_django.types import DjangoObjectType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_paginator(qs, page_size, page, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return paginated_type(
        total=p.count,
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        index_start_obj = page_obj.start_index(),
        index_end_obj = page_obj.end_index(),
        players=page_obj.object_list,
        **kwargs
    )

class EnumOrder(graphene.Enum):
    ASC = "ASC"
    DESC = "DESC"

class Paginador(graphene.Interface):
    total = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    index_start_obj = graphene.Int()
    index_end_obj = graphene.Int()

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player

class PlayerPaginatedType(graphene.ObjectType):
    class Meta:
        interfaces = (Paginador,)
    players = graphene.List(PlayerType)

class Query(graphene.ObjectType):
    get_players = graphene.Field(PlayerPaginatedType, club=graphene.String(), search=graphene.String(), order=EnumOrder(default_value=EnumOrder.ASC.name), page=graphene.Int(default_value=1), page_size=graphene.Int(default_value=50))

    def resolve_get_players(self, info, page=None, page_size=200, **kwargs):
        datos = Player.objects.all()
        if 'club' in kwargs:
            datos = datos.filter(club__icontains=kwargs['club'])
        if 'search' in kwargs:
            datos = datos.filter(name__icontains=kwargs['search'])
        if 'order' in kwargs:
            if kwargs['order'] == 'ASC':
                order = 'name'
            else:
                order = '-name'
            datos = datos.order_by(order)
        return get_paginator(datos, page_size, page, PlayerPaginatedType)

schema = graphene.Schema(query=Query)
