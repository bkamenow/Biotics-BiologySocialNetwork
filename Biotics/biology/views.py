from django.shortcuts import render


# Create your views here.


def zoology_home(request):
    return render(request, template_name='biology/zoology-home.html')


def botany_home(request):
    return render(request, template_name='biology/botany.html')


def microbiology_home(request):
    return render(request, template_name='biology/microbiology.html')


def anatomy_and_physiology(request):
    return render(request, template_name='biology/zoology/anatomy_physiology.html')


def behavior(request):
    return render(request, template_name='biology/zoology/behavior.html')


def conservation(request):
    return render(request, template_name='biology/zoology/conservation.html')


def ecology(request):
    return render(request, template_name='biology/zoology/ecology.html')


def evolution(request):
    return render(request, template_name='biology/zoology/evolution.html')


def genetics(request):
    return render(request, template_name='biology/zoology/genetics.html')


def taxonomy_classification(request):
    return render(request, template_name='biology/zoology/taxonomy_classification.html')


def bacteriology(request):
    return render(request, template_name='biology/microbiology/bacteriology.html')


def environmental_microbiology(request):
    return render(request, template_name='biology/microbiology/environmental_microbiology.html')


def industrial_microbiology(request):
    return render(request, template_name='biology/microbiology/industrial_microbiology.html')


def medical_microbiology(request):
    return render(request, template_name='biology/microbiology/medical_microbiology.html')


def microbial_genetics(request):
    return render(request, template_name='biology/microbiology/microbial_genetics.html')


def microbial_physiology(request):
    return render(request, template_name='biology/microbiology/microbial_physiology.html')


def mycology(request):
    return render(request, template_name='biology/microbiology/mycology.html')


def protozoology(request):
    return render(request, template_name='biology/microbiology/protozoology.html')


def virology(request):
    return render(request, template_name='biology/microbiology/virology.html')


def economic_botany(request):
    return render(request, template_name='biology/botany/economic_botany.html')


def ethnobotany(request):
    return render(request, template_name='biology/botany/ethnobotany.html')


def physiology(request):
    return render(request, template_name='biology/botany/physiology.html')


def plant_biotechnology(request):
    return render(request, template_name='biology/botany/plant_biotechnology.html')


def plant_ecology(request):
    return render(request, template_name='biology/botany/plant_ecology.html')


def plant_systematics(request):
    return render(request, template_name='biology/botany/plant_systematics.html')


def plantanatomy_morphology(request):
    return render(request, template_name='biology/botany/plantanatomy_morphology.html')


def plantevolution_genetics(request):
    return render(request, template_name='biology/botany/plantevolution_genetics.html')


def taxonomy_systematics(request):
    return render(request, template_name='biology/botany/taxonomy_systematics.html')
