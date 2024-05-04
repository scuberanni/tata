from django.shortcuts import render, redirect ,get_object_or_404
from.models import product_master,retailer_master,box_master,product,to_ret_product,box_product,ret_ret
from.forms import Pr_Form,box_Form,ret_Form,ProductForm,to_ret_Form,to_ret_Form2,sale_ProductForm,sale_to_ret_Form
from django.forms import formset_factory
from .forms import BoxProductForm,BoxProductForm2,BoxProductForm1,RetailerForm,adjust_form
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.db.models import Sum


# Create your views here.
def home(request):
    # Retrieve products
    products = to_ret_product.objects.all().order_by('-box2')[:9]
    products2 = to_ret_product.objects.all().order_by('-box2')
    products1 = product.objects.all()
    
    # Calculate sums
    sum_cable2 = products2.aggregate(total_cable=Sum('cable2'))['total_cable'] or 0
    sum_lnb2 = products2.aggregate(total_lnb=Sum('lnb2'))['total_lnb'] or 0
    sum_dish2 = products2.aggregate(total_dish=Sum('dish2'))['total_dish'] or 0
    sum_kit2 = products2.aggregate(total_kit=Sum('kit2'))['total_kit'] or 0
    sum_box2 = products2.aggregate(total_box=Sum('box2'))['total_box'] or 0

    sum_cable1 = products1.aggregate(total_cable=Sum('cable'))['total_cable'] or 0
    sum_lnb1 = products1.aggregate(total_lnb=Sum('lnb'))['total_lnb'] or 0
    sum_dish1 = products1.aggregate(total_dish=Sum('dish'))['total_dish'] or 0
    sum_kit1 = products1.aggregate(total_kit=Sum('kit'))['total_kit'] or 0
    

    sum_cable = sum_cable2 + sum_cable1
    sum_lnb = sum_lnb2 + sum_lnb1
    sum_dish = sum_dish2 + sum_dish1
    sum_kit = sum_kit2 + sum_kit1
    sum_box = sum_box2

    return render(request, 'index.html', {'products': products, 'products1': products1, 
                                          'sum_cable': sum_cable, 'sum_lnb': sum_lnb, 
                                          'sum_dish': sum_dish, 'sum_kit': sum_kit,'sum_box': sum_box})

def admin(request):
    return render(request,'admin')

def stock_view(request):
    
    products = to_ret_product.objects.all().order_by('retailer__r_name')
    products1=product.objects.all()
    return render(request, 'stock_view.html', {'products': products,'products1': products1}) 

def stock_view_ret(request,pk):
    product = to_ret_product.objects.get(pk=pk)

    retailer_id = product.retailer.id

    products1 = box_product.objects.filter(r_name_id=retailer_id,woc_date__isnull=True)
    products = to_ret_product.objects.filter(retailer_id=retailer_id)

    retailer = retailer_master.objects.get(id=retailer_id)
    r_name = retailer.r_name

    products5 = retailer_master.objects.filter(r_name=r_name)

    return render(request, 'stock_view_ret.html', {'products': products,'products1': products1,'products5': products5})

def stock_view_all(request):
    if request.method == 'POST':
        form = RetailerForm(request.POST)  # Initialize the form with POST data
        if form.is_valid():
            r_name = form.cleaned_data['r_name']
            retailer_obj = retailer_master.objects.filter(r_name=r_name).first()

            if retailer_obj:
                r_name_id = retailer_obj.id

                # Fetch products related to the retailer from different models
                products = to_ret_product.objects.filter(retailer_id=retailer_obj.id)
                products1 = box_product.objects.filter(r_name_id=retailer_obj.id, woc_date__isnull=True)

                # Fetch all products
                products3 = product.objects.all()
                products4 = box_product.objects.filter(Q(r_name_id='2') | Q(r_name_id=None),woc_date__isnull=True)
                products5 = retailer_master.objects.filter(r_name=r_name)


                # Render the template with the retrieved products and another data
                return render(request, 'stock_view_all.html', {'products': products, 'products1': products1, 'products3': products3, 'products4': products4,'products5': products5,})
            else:
                # Render error template if retailer not found
                return render(request, 'error.html', {'message': 'Retailer not found.'})  
    else:
        form = RetailerForm()  # Initialize the form with no data for initial rendering
        
        # Fetch all products if it's not a POST request
        products3 = product.objects.all()
        products4 = box_product.objects.filter(Q(r_name_id='2') | Q(r_name_id=None))
    
    return render(request, 'stock_view_all.html', {'form': form, 'products3': products3,'products4': products4,})

def detail_view(request):
    categories = retailer_master.objects.all()
    return render(request, 'details.html', {'categories': categories})  

def pr_master(request): 
    frm=Pr_Form()
    if request.POST:
        frm=Pr_Form(request.POST,request.FILES)
        if frm.is_valid():
            frm.save()
            return redirect('pr_master')
            
    else:
        frm=Pr_Form()        
    return render(request,'pr_master.html',{'frm':frm})

def bo_master(request): 
    frm=box_Form()
    if request.POST:
        frm=box_Form(request.POST,request.FILES)
        if frm.is_valid():
            frm.save()
            return redirect('bo_master')
            
    else:
        frm1=box_Form()        
    return render(request,'pr_master.html',{'frm':frm})

def add_box_master(request):
    BoxMasterFormSet = formset_factory(BoxProductForm, extra=10)
    if request.method == 'POST':
        formset = BoxMasterFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('b_name'):
                    # Create a new box master instance
                    box_master_instance = form.save()

                    # Increment box2 for the corresponding retailer
                    retailer_name = box_master_instance.r_name
                    try:
                        to_ret_product_instance = to_ret_product.objects.get(retailer=retailer_name)
                        to_ret_product_instance.box2 += 1
                        to_ret_product_instance.save()
                    except to_ret_product.DoesNotExist:
                        return redirect('add_box_master')    
                    messages.success(request, "Box master added successfully.")
                else:
                    messages.error(request, "No existing product found.")
            return redirect('add_box_master')  # Redirect to the same page after saving
        else:
            messages.error(request, "Formset is not valid.")
    else:
        formset = BoxMasterFormSet()
    return render(request, 'add_box_master.html', {'formset': formset})

def box_details_edit(request, pk):
    box_product_instance = get_object_or_404(box_product, pk=pk)
    old_retailer_name = box_product_instance.r_name
    
    if request.method == 'POST':
        form = BoxProductForm2(request.POST, instance=box_product_instance)
        if form.is_valid():
            new_retailer_name = form.cleaned_data['r_name']

            try:
                old_to_ret_product_instance = to_ret_product.objects.get(retailer=old_retailer_name)
                new_to_ret_product_instance = to_ret_product.objects.get(retailer=new_retailer_name)

                # Update box2 for the old retailer
                old_to_ret_product_instance.box2 -= 1
                old_to_ret_product_instance.save()

                # Update box2 for the new retailer
                new_to_ret_product_instance.box2 += 1
                new_to_ret_product_instance.save()

            except to_ret_product.DoesNotExist:
                pass

            form.save()

            return redirect('close_box_master')
    else:
        form = BoxProductForm2(instance=box_product_instance)
    
    return render(request, 'box_details_edit.html', {'form': form})

def woc(request, pk):
    box_product_instance = get_object_or_404(box_product, pk=pk)

    if request.method == 'POST':
        form = BoxProductForm1(request.POST, instance=box_product_instance)
        if form.is_valid():
            with transaction.atomic():
                r_name_id = form.cleaned_data.get('r_name').id
                set_value = form.cleaned_data.get('set')
                print(r_name_id)

                if set_value == 'BOX_ONLY':
                    set_var = 0
                elif set_value == 'FULL_SET':
                    set_var = 1
                else:
                    set_var = None  # Handle other cases if needed

                
                if set_var == 1:
                    # Subtract from product or to_ret_product based on r_name
                    if form.cleaned_data.get('r_name').r_name == "Distributor BOX":
                        product_instance = product.objects.first()
                        if product_instance:
                            # Check if input data exceeds existing data
                            a, b, c, d = 10, 1, 1, 1  # Assuming these are the input values
                            if (a > product_instance.cable or
                                b > product_instance.lnb or
                                c > product_instance.dish or
                                d > product_instance.kit):
                                messages.error(request, "Input data cannot exceed existing data", extra_tags='alert-danger')
                                return render(request, 'woc.html', {'form': form})

                            # Proceed with subtraction
                            product_instance.cable -= a
                            product_instance.lnb -= b
                            product_instance.dish -= c
                            product_instance.kit -= d
                            product_instance.save()

                            to_ret_product_instance = to_ret_product.objects.filter(retailer_id=r_name_id).first()
                            to_ret_product_instance.box2 -= 1
                            to_ret_product_instance.save()

                        else:
                            messages.error(request, "Input data cannot exceed existing data")
                    else:
                        to_ret_product_instance = to_ret_product.objects.filter(retailer_id=r_name_id).first()
                        if to_ret_product_instance:
                            # Check if input data exceeds existing data
                            # Similar logic as above
                            a, b, c, d = 10, 1, 1, 1
                            if (a > to_ret_product_instance.cable2 or
                                b > to_ret_product_instance.lnb2 or
                                c > to_ret_product_instance.dish2 or
                                d > to_ret_product_instance.kit2):
                                messages.error(request, "Input data cannot exceed existing data")
                                return render(request, 'woc.html', {'form': form})

                            # Proceed with subtraction
                            to_ret_product_instance.cable2 -= a
                            to_ret_product_instance.lnb2 -= b
                            to_ret_product_instance.dish2 -= c
                            to_ret_product_instance.kit2 -= d
                            to_ret_product_instance.box2 -= d
                            to_ret_product_instance.save()
                        else:
                            messages.error(request, "Input data cannot exceed existing data")
                    
                    box_product_instance = form.save(commit=False)
                    box_product_instance.set = 1  # Set the set field to 0
                    box_product_instance.save()
                    return redirect('close_box_master')
            
                else:
                    to_ret_product_instance = to_ret_product.objects.filter(retailer_id=r_name_id).first()
                    to_ret_product_instance.box2 -= 1
                    to_ret_product_instance.save()

                    box_product_instance = form.save(commit=False)
                    box_product_instance.set = 0  # Set the set field to 0
                    box_product_instance.save()
                    return redirect('close_box_master')
    else:
        form = BoxProductForm1(instance=box_product_instance)

    return render(request, 'woc.html', {'form': form})

def box_details_delete(request, pk):
    # Retrieve the box_product instance by its primary key (pk)
    box_product_instance = get_object_or_404(box_product, pk=pk)
    
    # Fetch the retailer name associated with the box_product instance
    retailer_name = box_product_instance.r_name
    
    # Find the old_to_ret_product_instance for the old retailer
    old_to_ret_product_instance = to_ret_product.objects.get(retailer=retailer_name)

    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the box_product instance
        box_product_instance.delete()

        # Update box2 for the old retailer
        old_to_ret_product_instance.box2 -= 1
        old_to_ret_product_instance.save()
        
        # Redirect to a success page or any other desired action
        return redirect('close_box_master')
    
    # If the request method is not POST, render a confirmation page
    return render(request, 'box_details_delete.html', {'box_product_instance': box_product_instance})

def close_box_master(request):
    
    products1 = box_product.objects.filter(woc_date__isnull=True)
    return render(request, 'woc_all.html', {'products1':products1}) 

def box_edit(request,pk):
    instance_edit=box_master.objects.get(pk=pk)
    if request.POST:
        frm=box_Form(request.POST,request.FILES,instance=instance_edit)
        if frm.is_valid():
            instance_edit.save()
            return redirect('master')
    else:
       frm=box_Form(instance=instance_edit) 
    return render(request,'box_master.html',{'frm':frm})

def box_dlt(request,pk):
    instance_dlt= get_object_or_404(box_master, pk=pk)
    if request.method == 'POST':
        
            instance_dlt.delete()
            return redirect('master')
     
    return render(request,'delete.html',{'box_product_instance':instance_dlt})

def product_edit(request,pk):
    instance_edit=product_master.objects.get(pk=pk)
    if request.POST:
        frm=Pr_Form(request.POST,request.FILES,instance=instance_edit)
        if frm.is_valid():
            instance_edit.save()
            return redirect('master')
    else:
       frm=Pr_Form(instance=instance_edit) 
    return render(request,'pr_master.html',{'frm':frm})

def product_dlt(request,pk):
    instance_dlt= get_object_or_404(product_master, pk=pk)
    if request.method == 'POST':
        
            instance_dlt.delete()
            return redirect('master')
     
    return render(request,'delete.html',{'box_product_instance':instance_dlt})

def retailer_edit(request,pk):
    instance_edit=retailer_master.objects.get(pk=pk)
    if request.POST:
        frm=ret_Form(request.POST,request.FILES,instance=instance_edit)
        if frm.is_valid():
            instance_edit.save()
            return redirect('master')
    else:
       frm=ret_Form(instance=instance_edit) 
    return render(request,'ret_master.html',{'frm':frm})

def retailer_edit1(request,pk):
    instance_edit=retailer_master.objects.get(pk=pk)
    if request.POST:
        frm=ret_Form(request.POST,request.FILES,instance=instance_edit)
        if frm.is_valid():
            instance_edit.save()
            return redirect('stock_view_all')
    else:
       frm=ret_Form(instance=instance_edit) 
    return render(request,'ret_master.html',{'frm':frm})

def retailer_dlt(request,pk):
    instance_dlt= get_object_or_404(retailer_master, pk=pk)
    if request.method == 'POST':
        
            instance_dlt.delete()
            return redirect('master')
     
    return render(request,'delete.html',{'box_product_instance':instance_dlt})

from .models import to_ret_product

def ret_master(request):
    # Initialize the form
    frm = ret_Form()

    # If form is submitted
    if request.method == 'POST':
        frm = ret_Form(request.POST, request.FILES)
        if frm.is_valid():
            # Check if retailer with the same name already exists
            if to_ret_product.objects.filter(retailer__r_name=request.POST['r_name']).exists():
                # If retailer with same name exists, add an error to the form
                frm.add_error('r_name', 'Retailer with this name already exists.')
            else:
                # Save the form data
                retailer = frm.save(commit=False)
                retailer.save()
                
                # Create a related object
                to_ret_product.objects.create(
                    retailer=retailer,
                    cable2=0,
                    lnb2=0,
                    dish2=0,
                    kit2=0,
                    box2=0
                )
                
                # Redirect to ret_master view after successful form submission
                return redirect('ret_master')

    # Render the form if it's not submitted or is invalid
    return render(request, 'pr_master.html', {'frm': frm})

def master(request):
    products = product_master.objects.all()
    boxes = box_master.objects.all()
    retailers = retailer_master.objects.all()
    return render(request, 'master.html', {'products': products, 'boxes': boxes, 'retailers': retailers})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            cable = form.cleaned_data['cable']
            lnb = form.cleaned_data['lnb']
            dish = form.cleaned_data['dish']
            kit = form.cleaned_data['kit']
            
            # Check if the product already exists in the database
            existing_product = product.objects.first()  # You may need to change this query
            
            if existing_product:
                # Update existing product's quantities
                existing_product.cable += cable
                existing_product.lnb += lnb 
                existing_product.dish += dish
                existing_product.kit += kit
                existing_product.save()
            else:
                # Create a new product
                new_product = product.objects.create(
                    cable=cable,
                    lnb=lnb,
                    dish=dish,
                    kit=kit
                )
                new_product.save()
            
            return redirect('add_product')  # Redirect to the same page after successful submission
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})

def ret_product(request):
    form = to_ret_Form()  # Correcting form instantiation

    if request.method == 'POST':
        form = to_ret_Form(request.POST)
        
        if form.is_valid():
            # Collect form data
            retailer2 = form.cleaned_data['retailer']
            cable2 = form.cleaned_data['cable2']
            lnb2 = form.cleaned_data['lnb2']
            dish2 = form.cleaned_data['dish2']
            kit2 = form.cleaned_data['kit2']

            # Check if the product already exists in the database
            existing_product = product.objects.first()  # Update this query
            
            if existing_product:
                # Check if input data exceeds existing data
                if (cable2 > existing_product.cable or
                    lnb2 > existing_product.lnb or
                    dish2 > existing_product.dish or
                    kit2 > existing_product.kit):
                    form.add_error(None, "Input data cannot exceed existing data")
                else:
                    # Update existing product's quantities
                    existing_product.cable -= cable2
                    existing_product.lnb -= lnb2 
                    existing_product.dish -= dish2
                    existing_product.kit -= kit2
                    existing_product.save()

                    # Create or update to_ret_product
                    new_to_ret_product, created = to_ret_product.objects.get_or_create(retailer=retailer2)
                    new_to_ret_product.cable2 += cable2
                    new_to_ret_product.lnb2 += lnb2 
                    new_to_ret_product.dish2 += dish2
                    new_to_ret_product.kit2 += kit2
                    new_to_ret_product.save()

                    return redirect('ret_product')  # Replace 'some_url_name' with a valid URL name
            else:
                messages.error(request, "No existing product found.")
        
    # This line should be outside the if block
    return render(request, 'ret_product.html', {'form': form})

def ret_home(request):
    
    form1= to_ret_Form()
    form2= to_ret_Form2()
    
    return render(request, 'ret_kan.html', {'form': form1,'form2': form2})

def ret_kan(request):
    form = to_ret_Form()  # Correcting form instantiation

    if request.method == 'POST':
        form = to_ret_Form(request.POST)
        
        
        if form.is_valid():
            # Collect form data
            retailer = form.cleaned_data['retailer']
            cable2 = form.cleaned_data['cable2']
            lnb2 = form.cleaned_data['lnb2']
            dish2 = form.cleaned_data['dish2']
            kit2 = form.cleaned_data['kit2']

            # Check if the product already exists in the database
            existing_product = product.objects.first()  # You may need to change this query
            existing1_product = to_ret_product.objects.filter(retailer=retailer).first() 
            
            if existing1_product:
                # Check if the input data exceeds existing data
                if (cable2 > existing1_product.cable2 or
                    lnb2 > existing1_product.lnb2 or
                    dish2 > existing1_product.dish2 or
                    kit2 > existing1_product.kit2):
                    form.add_error(None, "Input data cannot exceed existing data")
                else:
                    # Update existing product's quantities
                    existing_product.cable += cable2
                    existing_product.lnb += lnb2 
                    existing_product.dish += dish2
                    existing_product.kit += kit2
                    existing_product.save()

                    # Create or update to_ret_product
                    new_product, created = to_ret_product.objects.get_or_create(retailer=retailer)
                    new_product.cable2 -= cable2
                    new_product.lnb2 -= lnb2 
                    new_product.dish2 -= dish2
                    new_product.kit2 -= kit2
                    new_product.save() 
                    
                      

                    return redirect('ret_home')  # Redirect to the same page after successful submission
            else:
                form.add_error(None, "No existing product found")
                return redirect('ret_home')   # Handle case where no product exists
    else:
        form = to_ret_Form()
    
    return render(request, 'ret_kan.html', {'form': form})

def ret_ret(request):
    form2 = to_ret_Form2()

    if request.method == 'POST':
        form2 = to_ret_Form2(request.POST)
        if form2.is_valid():
            r1 = form2.cleaned_data['retailer1']
            r2 = form2.cleaned_data['retailer2']
            qty = form2.cleaned_data['quantity']

            a = qty * 10
            b = qty * 1
            c = qty * 1
            d = qty * 1

            # Fetch existing product data associated with r1
            existing_product = to_ret_product.objects.filter(retailer=r1).first()

            if existing_product:
                # Check if the input data exceeds existing data
                if (a > existing_product.cable2 or
                    b > existing_product.lnb2 or
                    c > existing_product.dish2 or
                    d > existing_product.kit2):
                    form2.add_error(None, "Input data cannot exceed existing data")
                else:
                    # Update existing product's quantities
                    existing_product.cable2 -= a
                    existing_product.lnb2 -= b
                    existing_product.dish2 -= c
                    existing_product.kit2 -= d
                    existing_product.save()

                    # Create or update to_ret_product for r2
                    existing2_product, created2 = to_ret_product.objects.get_or_create(retailer=r2)
                    
                    existing2_product.cable2 += a
                    existing2_product.lnb2 += b
                    existing2_product.dish2 += c
                    existing2_product.kit2 += d
                    existing2_product.save() 

                    return redirect('ret_home')  # Redirect to the same page after successful submission
            else:
                form.add_error(None, "No existing product found for retailer 1")
                return redirect('ret_home')
        else:
            form = to_ret_Form2()       
    
    return render(request, 'ret_kan.html', {'form2': form2})

def sale_ret_product(request):
    form = sale_ProductForm()  # Correcting form instantiation

    if request.method == 'POST':
        form = sale_ProductForm(request.POST)
        
        if form.is_valid():
            # Collect form data
            
            cable3 = form.cleaned_data['cable3']
            lnb3 = form.cleaned_data['lnb3']
            dish3 = form.cleaned_data['dish3']
            kit3 = form.cleaned_data['kit3']
            

            # Check if the product already exists in the database
            existing_product = product.objects.first()  # You may need to change this query
             
            
            if existing_product:
                # Check if the input data exceeds existing data
                if (cable3 > existing_product.cable or
                    lnb3 > existing_product.lnb or
                    dish3 > existing_product.dish or
                    kit3 > existing_product.kit):
                    form.add_error(None, "Input data cannot exceed existing data")
                else :
                    # Update existing product's quantities
                    form.is_valid()
                    form.save()

                    existing_product.cable -= cable3
                    existing_product.lnb -= lnb3
                    existing_product.dish -= dish3
                    existing_product.kit -= kit3
                    existing_product.save()

                    
                    
                    
                      
                    return redirect('sale_ret_product')  # Redirect to the same page after successful submission
            else:
                form.add_error(None, "No existing product found")  # Handle case where no product exists
    else:
        form = sale_ProductForm()    
    
    
    return render(request, 'sale_ret_product.html', {'form': form})

def sale_ret_kan(request):
    form = sale_to_ret_Form()  # Correcting form instantiation

    if request.method == 'POST':
        form = sale_to_ret_Form(request.POST)
        
        if form.is_valid():
            # Collect form data
            
            cable4 = form.cleaned_data['cable4']
            lnb4 = form.cleaned_data['lnb4']
            dish4 = form.cleaned_data['dish4']
            kit4 = form.cleaned_data['kit4']
            

            # Check if the product already exists in the database
            existing_product = to_ret_product.objects.first()  # You may need to change this query
             
            
            if existing_product:
                # Check if the input data exceeds existing data
                if (cable4 > existing_product.cable2 or
                    lnb4 > existing_product.lnb2 or
                    dish4 > existing_product.dish2 or
                    kit4 > existing_product.kit2):
                    form.add_error(None, "Input data cannot exceed existing data")
                else :
                    # Update existing product's quantities
                    form.is_valid()
                    form.save()

                    existing_product.cable2 -= cable4
                    existing_product.lnb2 -= lnb4
                    existing_product.dish2 -= dish4
                    existing_product.kit2 -= kit4
                    existing_product.save()

                    
                    
                    
                      
                    return redirect('sale_ret_kan')  # Redirect to the same page after successful submission
            else:
                form.add_error(None, "No existing product found")  # Handle case where no product exists
    else:
        form = sale_to_ret_Form()    
    
    
    return render(request, 'sale_ret_kan.html', {'form': form})

def search(request):
    
    if request.method == 'GET':
        b_vscno = request.GET.get('b_vscno')
        b_slno = request.GET.get('b_slno')

        box_products = box_product.objects.none()

        if b_vscno:
            box_products = box_product.objects.all()
            box_products = box_products.filter(b_vscno__icontains=b_vscno)

        if b_slno:
            box_products = box_product.objects.all()
            box_products = box_products.filter(b_slno__icontains=b_slno) 
     
        return render(request, 'search.html',{'box_products': box_products})
    
def sales_reports(request):

    if request.method=='POST':
        
        S_date=request.POST.get('start_date1')
        E_date=request.POST.get('end_date1')
        P_rep=box_product.objects.filter(woc_date__gte=S_date,woc_date__lte=E_date).order_by('woc_date')

       
        return render ( request,'sales_reports.html',{'pr_reports':P_rep})
    else:
         
        return render(request,'sales_reports.html',) 
         
def adjust_box(request):
    form = adjust_form(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        adjustment = int(request.POST.get('adjustment'))
        action = request.POST.get('action')
        
        new_retailer_name = form.cleaned_data['retailer']
        
        # Attempt to get the retailer's product instance
        try:
            new_to_ret_product_instance = to_ret_product.objects.get(retailer=new_retailer_name)
        except to_ret_product.DoesNotExist:
            # Handle the case where the retailer doesn't exist
            # You might want to add a message to notify the user
            return redirect('adjust_box')

        # Based on the action, adjust the box2 field
        if action == 'subtract':
            new_to_ret_product_instance.box2 -= adjustment
        elif action == 'add':
            new_to_ret_product_instance.box2 += adjustment

        new_to_ret_product_instance.save()

        return redirect('adjust_box')  # Redirect to a success page after adjustment

    return render(request, 'adjust_box.html', {'form': form})



