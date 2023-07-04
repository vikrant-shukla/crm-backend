def limit_off(model, request, serial):
        query_params = request.query_params
        id = query_params['id'] if query_params.get('id') else False
        limit = query_params['limit'] if query_params.get('limit') else False
        offset  = query_params['offset'] if query_params.get('offset')  else False
        if id:
            query = model.objects.filter(id=id)
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