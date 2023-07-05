from django.db.models import Q
from customer.models import Representatives, Vendor
def limit_off(model, request, serial):
        query_params = request.query_params
        id = query_params['id'] if query_params.get('id') else False
        limit = query_params['limit'] if query_params.get('limit') else False
        offset  = query_params['offset'] if query_params.get('offset')  else False
        search = query_params['search'] if query_params.get('search')  else False
        if id:
            query = model.objects.filter(id=id)
        elif search:
            query = search_func(search, model)
        elif limit and offset:
            query = model.objects.all()[int(offset):int(limit)+int(offset)]
        elif limit or offset:
            if limit:
                query = model.objects.all()[:int(limit)]
            else:
                query = model.objects.all()[int(offset):]
        else:
            query = model.objects.all()
        serializer = serial(query, many=True)
        return serializer.data
def search_func(data, model):
    if model._meta.object_name == "Vendor":
        queryObj = model.objects.filter(Q(company_name__contains = data ) | Q(address__contains = data))
    if model._meta.object_name == "Representatives":
        queryObj = model.objects.filter(Q(firstname__contains = data ) | Q(lastname__contains = data) | Q(email__contains = data ) | Q(contact_no__contains = data))
    if model._meta.object_name == "Selected":
        queryObj = model.objects.filter(Q(project_name__contains = data ) | Q(project_duration_contains = data) | Q(working_person__contains = data ) | Q(extend_status__contains = data))
    
    return queryObj