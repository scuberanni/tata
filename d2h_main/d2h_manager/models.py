from django.db import models


set_choice= [ 
    ('BOX_ONLY', 'BOX_ONLY'),
    ('FULL_SET', 'FULL_SET'),
    
]

# Create your models here.
class product_master(models.Model):
    p_name=models.CharField(max_length=50 ,null=True)
    
    def __str__(self):
        return self.p_name
    
class box_master(models.Model):
    b_name=models.CharField(max_length=50 ,null=True)
    
    def __str__(self):
        return self.b_name 
    


class retailer_master(models.Model):
    r_name=models.CharField(max_length=50 ,null=True)
    address=models.CharField(max_length=50 ,null=True)
    ph_no=models.CharField(max_length=50 ,null=True)
    
    def __str__(self):
        return self.r_name  
    
class ret_ret(models.Model):
    retailer1 = models.ForeignKey(retailer_master, on_delete=models.CASCADE,null=True,related_name='r1')
    retailer2 = models.ForeignKey(retailer_master, on_delete=models.CASCADE,null=True,related_name='r2')
    quantity = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.retailer1} - {self.retailer2}"    
    
class box_product(models.Model):
    r_name = models.ForeignKey(retailer_master,on_delete=models.CASCADE,null=True,blank=True)
    b_name = models.ForeignKey(box_master, on_delete=models.CASCADE)
    b_slno=models.CharField(max_length=50 ,null=True,blank=True)
    b_vscno=models.CharField(max_length=50 ,null=True,blank=True)
    woc_date = models.DateField(null=True, blank=True )
    set= models.CharField(choices=set_choice , max_length=50 ,null=True )

    def __str__(self):
         return f"{self.b_name} - {self.b_vscno}"  

    

class box_retailer_master(models.Model): 
    retailer = models.ForeignKey(retailer_master, on_delete=models.CASCADE) 
    b_vcsno= models.ForeignKey(box_product, on_delete=models.CASCADE)
    add_date=models.DateField(null=True)
    sl_date=models.DateField(null=True, blank=True)

    def __str__(self):
        return self.retailer   
    
class Invoice(models.Model):
    retailer = models.ForeignKey(retailer_master, on_delete=models.CASCADE)
    product = models.ForeignKey(product_master, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # Assuming quantity can't be negative

class product(models.Model):
    cable = models.PositiveIntegerField(default=0, null=True)
    lnb = models.PositiveIntegerField(default=0, null=True)
    dish = models.PositiveIntegerField(default=0, null=True)
    kit = models.PositiveIntegerField(default=0, null=True)
    
    def __str__(self):
        return f"Cable: {self.cable}, LNB: {self.lnb}, Dish: {self.dish}, Kit: {self.kit}"

    
       
class to_ret_product(models.Model):
    retailer = models.ForeignKey(retailer_master, on_delete=models.CASCADE)
    cable2=models.PositiveIntegerField(default=0,null=True)
    lnb2=models.PositiveIntegerField(default=0,null=True)
    dish2=models.PositiveIntegerField(default=0,null=True) 
    kit2=models.PositiveIntegerField(default=0,null=True)
    box2=models.PositiveIntegerField(default=0,null=True)

    def __str__(self):
        return f"retailer: {self.retailer}"

class sale_product(models.Model):
    cable3=models.PositiveIntegerField(default=0,null=True,blank=True)
    lnb3=models.PositiveIntegerField(default=0,null=True,blank=True)
    dish3=models.PositiveIntegerField(default=0,null=True,blank=True) 
    kit3=models.PositiveIntegerField(default=0,null=True,blank=True)
    sl_date3 = models.DateField(null=True, blank=False)

    def __str__(self):
        return f"sl_date3: {self.sl_date3}"
    
class sale_to_ret_product(models.Model):
    retailer4 = models.ForeignKey(retailer_master, on_delete=models.CASCADE)
    cable4=models.PositiveIntegerField(default=0,null=True,blank=True)
    lnb4=models.PositiveIntegerField(default=0,null=True,blank=True)
    dish4=models.PositiveIntegerField(default=0,null=True,blank=True) 
    kit4=models.PositiveIntegerField(default=0,null=True,blank=True)
    sl_date4 = models.DateField(null=True, blank=False)

    def __str__(self):
        return f"retailer4: {self.retailer4}"


        
    
 

   