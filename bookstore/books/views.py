from django.shortcuts import render
from django.views.generic import View
from .models import Books
from django.db.models import Q

class MainView(View):
    model = Books
    template_name = 'books/main_page.html'
    def getUser(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return None

    def get(self, request, **kwargs):
        numpage=kwargs.get('page', 1)
        objects=[]
        for i in range(numpage*10-10,numpage*10):
            obj=''
            try:
                obj=Books.objects.get(pk=i)
            except:
                continue
            if obj.available and obj.published:
                objects.append(obj)
            else:
                pass
        prevAllowed=(numpage*10-11>0)#prev page
        nextAllowed=False#next page
        #next page
        try:
            nextObj=Books.objects.get(pk=numpage*10+1)
            nextAllowed=True
        except:
            #default
            pass

        context={
            'books': objects,
            'title': 'Books page {}'.format(numpage),
            'prev':(prevAllowed, numpage-1),
            'next':(nextAllowed, numpage+1),
        }
        return render(request, self.template_name, context=context)
# Create your views here.
