# All Basic


All Basic is a simple Django app to to add some basic functionality to use the DRF API. It consists of separating business logic and the application of nested data that comes from user requests and validations that support nested data.

## Quick start

Add `allbasic` to your `INSTALLED_APPS` setting like this:

```
INSTALLED_APPS = [
    ...
    'allbasic',
]
```

Create an application (what name is up) and create several files:

```
myapp/
    domains.py
    presentations.py
    validations.py
```

In your `validations.py`:

```
from allbasic.validations import BaseValidation

class ValidationUserDetailUpdate(BaseValidation):
    def schema(self):
        return {
            'last_name': {
                'type': 'string',
                'required': True,
                'empty': False
            },
            'first_name': {
                'type': 'string',
                'required': True,
                'empty': False
            }
        }
```

In your `domains.py`:

    from allbasic.domains import BaseDomain

    class DomainUserUpdate(BaseDomain):
        @transaction.atomic()
        def apply(self):
            data = self.context.get('data')
            user = self.context.get('user')

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)

            return user.save()

In your `presentations.py`:

```
from allbasic.presentations import BasePresentation

class UserDetailPresentation(BasePresentation):
    def present(self):
        user = self.context.get('user')

        return {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'last_name': user.last_name,
            'first_name': user.first_name
        }
```

In your `views.py`:

```
from allbasic.domains import ContextDomain
from allbasic.presentations import ContextPresentation
from allbasic.validations import ContextValidation

class UserDetailView(APIView):
    authentication_classes = (
        JSONWebTokenAuthentication,
        SessionAuthentication,
        BasicAuthentication
    )
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        validation = ContextValidation(ValidationUserDetailUpdate(request.data))

        if validation.validate():
            ContextDomain(DomainUserUpdate(context={'data': validation.data, 'user': request.user})).do_apply()
            presentation = ContextPresentation(UserDetailPresentation(context={'user': request.user}))
            return Response(presentation.do_present())

        return Response(validation.errors, status=status.HTTP_400_BAD_REQUEST)
```
