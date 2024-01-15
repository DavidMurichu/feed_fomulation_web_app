from django.shortcuts import render, redirect
import numpy as np
from pulp import *
from .models import Feed
from .optimizer import feed_fomulate
from django.shortcuts import get_object_or_404
# Create your views here.
selected_id=[]
nutrients_required=set()
nutrient_requirement={}
fomulation_data={}
shared_context={}
def check(input):
    if input=='' or input== None:
        return None
    else:
        return int(input)
def feed(request):
    context = shared_context
    if request.method == 'POST':
        for nutrient in list(nutrients_required):
            min_value = check(request.POST.get(f'min_{nutrient}', None))
            max_value = check(request.POST.get(f'max_{nutrient}', None))
            nutrient_requirement[nutrient] = {'min':min_value, 'max':max_value}

        for feed_id in selected_id:
            min_value = request.POST.get(f'min_{feed_id}')
            max_value = request.POST.get(f'max_{feed_id}')
            obj = get_object_or_404(Feed, id=int(feed_id))
            
            for ingridient, nutrients in obj.ingridient_batch.items():
                # Create a new dictionary for each ingredient
                nutrients['max']=check(max_value)
                nutrients['min']=check(min_value)
                fomulation_data[ingridient]=nutrients
            
        result=feed_fomulate(nutrient_requirements=nutrient_requirement, ingredients_x=fomulation_data)
        context.update(result)
        context['data'] = fomulation_data
        context['nutrients'] = nutrient_requirement
        return render(request, 'home.html', context)
    return render(request, 'home.html', context)


def ingridient_exist(check_ingridient):
    feed_instances = Feed.objects.all()
    for feed_instance in feed_instances:
        print(feed_instance.ingridient_batch.items())
        for ingredient, nutrients in feed_instance.ingridient_batch.items():
            print(ingredient)
            if ingredient == check_ingridient:
                return True          
    return False


def add_ingridient(request):
    context={}
    deleted_feed_data = request.session.pop('deleted_feed', None)
    if deleted_feed_data:
        # Use the data as needed
        context['deleted_feed_data'] = deleted_feed_data
        request.session.flush()
    if request.method == 'POST':
        ingridient = request.POST.get('ingridient')
        ingridient=ingridient.strip()
        cost = request.POST.get('cost')
        if ingridient_exist(ingridient):
            return render(request, 'add_ingridients.html', context)
        else:
            count = int(request.POST.get('name_count', ''))
            ingridient_batch={}
            nutrients = {}
            for i in range(count):
                nutrient_name = request.POST.get(f'n_{i}')
                nutrient_amount = float(request.POST.get(f'a_{i}'))
                nutrients[nutrient_name] = nutrient_amount
            nutrients['cost'] = int(cost)

            ingridient_batch[ingridient]=nutrients
            # Create a Feed instance and save it to the database
            feed_instance = Feed(ingridient_batch=ingridient_batch)
            feed_instance.save()

            # Redirect or render a response as appropriate
            return redirect('feed_store')  # Replace 'feed_store' with the appropriate URL

    return render(request, 'add_ingridients.html', context)


def feed_store(request):
    context={}
    if request.method=='POST':
        selected=request.POST.getlist('feed')
        def is_unique(value, my_set):
            return value not in my_set 
        ingridients = {}
        

        for id in selected:
            selected_id.append(id)
            obj = get_object_or_404(Feed, id=int(id))
            for ingridient, nutrients in obj.ingridient_batch.items():
                ingridients[ingridient]=id
                for nutrient, value in nutrients.items():
                    if nutrient != 'cost':
                        if is_unique(nutrient, nutrients_required):
                            nutrients_required.add(nutrient)
        shared_context['nutrients'] = list(nutrients_required)
        shared_context['ingridient'] = ingridients

        return redirect('home')


        
    
    feed_instances = Feed.objects.all()
    feeds_data = []
    for feed_instance in feed_instances:
        ingredients_data = []
        for ingredient, nutrients in feed_instance.ingridient_batch.items():
            ingredients_data.append({
                'ingredient': ingredient,
                'nutrients': nutrients.items(),
            })

        feeds_data.append({
            'id': feed_instance.id,
            'ingredients_data': ingredients_data,
        })
        context = {'feeds_data': feeds_data}
    return render(request, 'feed.html', context )

def edit(request, id):
    object = get_object_or_404(Feed, id=id)
    request.session['deleted_feed'] = {
        'ingridient_batch': object.ingridient_batch,
        
    }
   
    object.delete()
    return redirect('add_ingridient')




def delete(request, id):
    object = get_object_or_404(Feed, id=id)
    object.delete()
    return redirect('feed_store')


