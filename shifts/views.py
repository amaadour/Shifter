from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy,reverse
from .models import *
from .forms import ArrangementForm,addForm,DayForm,StaffForm
from .util import daysInPeriod
from django.forms import formset_factory
# Create your views here.
def index(request):
    return render(request,'shifts/index.html')

def addStaff(request):
    return render(request,'shifts/addStaff.html',context={})
    
def form2(request,pk):  
    query = get_object_or_404(Arrangement,pk=pk)
    if query.is_filled:
        return HttpResponseRedirect(reverse_lazy("detail",kwargs = {"pk":pk}))
    start = query.start
    end = query.end
    formCount = len(daysInPeriod(start, end))
    dayFormSet = formset_factory(DayForm,extra = formCount)
    staffFormSet = formset_factory(StaffForm,extra=0)
    context = {
        "dayFormSet" : dayFormSet,
        "staffFormSet":staffFormSet    
    }
    if request.method=="POST":
        i=0
        query.resetDays()
        querySet = Day.objects.filter(arrangement = query)
        for day in querySet:
            try:
                num = int(request.POST[f"form-{i}-minStaff"])
            except: 
                num=1
            day.setMinStaff(num)
            day.save()
            i+=1
        staffExtra = int(request.POST['form-TOTAL_FORMS'])
        for x in range(staffExtra):
            try:
                username = request.POST[f"form-{x}-username"]
                if username=="":
                    pass
            except KeyError:
                pass
            staff = Staff(username=username)
            staff.save()
            query.staffSet.add(staff)
        query.is_filled=True
        query.save()
        query.arrange()
        return HttpResponseRedirect(reverse("index"))
            
    return render(request,"shifts/form2.html",context)    

def detailView(request,pk):
    query = get_object_or_404(Arrangement,pk=pk)
    daySet = Day.objects.filter( arrangement=query)
    print(list(daySet))
    context = {
        "object":query,
        "days":daySet
    }
    return render(request,"shifts/detail.html",context)


class ArrangementCreateView(CreateView):
    model = Arrangement
    template_name: str = "shifts/createArrangement.html"
    form_class =   ArrangementForm

class ArrangementListView(ListView):
    queryset = Arrangement.objects.all()
    template_name = "shifts/listArrangement.html"
    
    
    

    

    
    

# def multiplying(request,*args, **kwargs):
#     if request.method =="POST":
#         sum=0
#         for key in request.POST.keys():
#             if "form" in str(key):
#                 sum+=int(request.POST[key])
#         context={
#             "sum":sum
#         }
#     return render(request,"shifts/multiply.html",context)

    
# def adding(request):
#     formCount = 5
#     formSet = formset_factory(addForm,extra=formCount)
#     context={
#         'formSet':formSet,
#         'sum':0
#     }
#     if request.method=="POST":
#         sum = 0
#         for i in range(formCount):
#             sum+=int(request.POST[f"form-{i}-num"])
#         context['sum']=sum
#         return multiplying(request,sum=sum)
#     return render(request,"shifts/add.html",context) 
