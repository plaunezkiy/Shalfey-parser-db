import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from drugs.models import Drug


def drugs_to_csv(request):
    drugs = Drug.objects.all()
    response = HttpResponse()
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=drugs_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Drug ID', 'Name', 'Slug', 'url'])
    drugs_fields = drugs.values_list('id', 'name', 'slug', 'url')
    for drug in drugs_fields:
        writer.writerow(drug)
    return response


def classifier(request: HttpRequest):
    if request.method == "POST":
        pk = request.POST.get("drug_id")
        name = request.POST.get("name")
        description = request.POST.get("description")
        warning = request.POST.get("warning")
        tags = request.POST.get("tags")
        cats = request.POST.get("cats")
        drug = Drug.objects.get(pk=pk)
        drug.name = name
        drug.description = description
        drug.warning = warning
        drug.tags = tags
        drug.cats = cats
        drug.status = Drug.StatusCodes.READY
        drug.save()

        # print(request.body.decode())
        return redirect('classifier')
    # drug = Drug.objects.last()
    all_drugs = Drug.objects.all() 
    drugs = all_drugs.filter(status=Drug.StatusCodes.AWAITING) 
    drug = drugs.first()
    return render(request, 'drugs/classifier.html', context={"drug": drug, "total": len(all_drugs), "awaiting": len(drugs)})