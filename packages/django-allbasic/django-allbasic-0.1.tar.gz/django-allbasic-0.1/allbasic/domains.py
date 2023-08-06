from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class BaseDomain(object):
    def __init__(self, context={}):
        self.context = context

    def apply(self):
        pass


class ContextDomain(object):
    def __init__(self, domain):
        self.__domain = domain

    def do_apply(self):
        return self.__domain.apply()


class DomainPagination(BaseDomain):
    def __get_page(self):
        request = self.context.get('request')
        return request.GET.get('page', 1)

    def apply(self):
        queryset = self.context.get('queryset')
        page = self.__get_page()
        limit = self.context.get('limit', 10)
        context = {
            'next': None,
            'previous': None,
            'total': 0,
            'results': []
        }

        paginator = Paginator(queryset, limit)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        if queryset.has_previous():
            context['previous'] = queryset.previous_page_number()

        if queryset.has_next():
            context['next'] = queryset.next_page_number()

        context['total'] = queryset.paginator.count

        return context, queryset

