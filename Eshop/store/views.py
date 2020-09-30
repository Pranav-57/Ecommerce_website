from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .models.product import Product
from .models.category import Category, SubCategory
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm,PasswordChangeForm,SetPasswordForm
from .forms import Signupform,Edituserform,Userorderform,Productform,Productcategory, Productsubcategory
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from .models.order import Userorder
from django.contrib.auth.models import User
from .forms import Reviewform
from .models.review import Review
from django.core.cache import cache
from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView


# Create your views here.
subcates = SubCategory.objects.all()
def index(request):
    q = request.session.get('q')
    cache_value = cache.get('time','the time')
    print('cache_value',cache_value)
    # print('cart',carts)
    # for cart in carts:
    #     print('onecart',cart)
    # product = Product.objects.filter(category=id)
    product = Product.objects.all().order_by('?')
    category = Category.objects.all()
    print(request.session.get('customer_id'))
    print(request.session.get('name'))
    q = request.session.get('q')
    print('q',q)
    user__id = request.session.get('ii')
    print('user__id',user__id)
    mn = cache.get('user_cartt', 0,version=user__id)
    print('mn',mn)
    m = []
    n = []
    # m = Product.objects.all().filter(rating=4)
    for products in product:
        if products.offer >= 30:
            m.append(products)                       
        
    for products in product:
        if products.rating >= 4:
            n.append(products)
                      

    # aa = Product.objects.filter(subcategory == 'Mens')
    subcates = SubCategory.objects.all()
    return render(request,'store/index.html',{'products':product,'categories':category,'ms':m[:4],'ns':n[:4] , 'subcates':subcates})

def filter(request,id):
    filter_product = []
    product = Product.objects.filter(category_id=id)
    subcates = SubCategory.objects.all()

    b = []        
    for products in product:
        d=products.category
        break

    for products in product:
        if len(b) == 0: 
            b.append(products.brand) 
        else:
            if products.brand in b:
                pass
            else:
                b.append(products.brand) 
    print(b)    

    for i in b:
        i = request.GET.get('i')
        print(i)

    category = Category.objects.all() 
    four = request.GET.get('four')
    ranges = request.GET.get('range')
    three = request.GET.get('three')
    two = request.GET.get('two')
    one = request.GET.get('one')
    g = []
    if request.GET.get('ywc'):
        g.append(request.GET.get('ywc'))
    if request.GET.get('samsung'):
        g.append(request.GET.get('samsung'))
    if request.GET.get('iphone'):
        g.append(request.GET.get('iphone'))
    if request.GET.get('realme'):
        g.append(request.GET.get('realme'))
    if request.GET.get('redmi'):
        g.append(request.GET.get('redmi'))
    if request.GET.get('nike'):
        g.append(request.GET.get('nike'))
    if request.GET.get('Monte_Carlo'):
        g.append(request.GET.get('Monte_Carlo'))
    if request.GET.get('Louis_Philippe'):
        g.append(request.GET.get('Louis_Philippe'))
    if request.GET.get('Peter_England'):
        g.append(request.GET.get('Peter_England'))
    if request.GET.get('Allen_Solly'):
        g.append(request.GET.get('Allen_Solly'))
    if request.GET.get('fastrack'):
        g.append(request.GET.get('fastrack'))
    if request.GET.get('sony'):
        g.append(request.GET.get('sony'))
    print('yeee',g)

    offer = request.GET.get('offer')
    print(ranges)
    if four or three or two or one or offer or ranges or g:
        filter_product = forfilter(g,four,ranges,three,two,one,offer,filter_product,product)
        return render(request,'store/filters.html',{'cate':d, 'products':filter_product,'categories':category,'brands':b, 'subcates':subcates})
    else:
        return render(request,'store/filters.html',{'products':product,'categories':category,'cate':d,'brands':b, 'subcates':subcates})

def signup(request):
    category = Category.objects.all()
    subcates = SubCategory.objects.all()
    if request.method == "POST":        
        fm = Signupform(request.POST)
        if fm.is_valid():
            fm.save()
            messages.info(request,'Account Created Suscessfully')
            return render(request,'store/login.html',{'form':fm,'categories':category})

    else:       
        fm = Signupform()
    return render(request,'store/signup.html',{'form':fm,'categories':category, 'subcates':subcates})

def user_login(request):
    category = Category.objects.all()
    subcates = SubCategory.objects.all()
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            # print(email,password)
            # users = Customer.get_customer_by_email(email)
            user = authenticate(username=username,password=password)
            print('user',user)
            if user is not None:
                login(request,user)
                print(user.id)
                request.session['customer_id']=user.id
                request.session['name']=user.username

                # request.session['user']=user
                # print(request.session['user'])
                messages.info(request,'login Suscessfully')
                return HttpResponseRedirect('/')
            else:
                messages.info(request,'Please Enter Your Username and Password.')
                return HttpResponseRedirect('/login/')
                        
        else:
            return render(request,'store/login.html',{'categories':category, 'subcates':subcates})
    else:
        return HttpResponseRedirect('/')

def profile(request):
    category = Category.objects.all()
    subcates = SubCategory.objects.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = Edituserform(instance=request.user, data=request.POST)
            if fm.is_valid:
                fm.save()
                messages.info(request,'Profile Upadated ')
                return HttpResponseRedirect('/')
        else:    
            fm = Edituserform(instance=request.user)
        return render(request,'store/profile.html',{'form':fm,'categories':category, 'subcates':subcates})
    else:
        return HttpResponseRedirect('/login/')

def changepass(request):
    category = Category.objects.all()
    subcates = SubCategory.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.info(request,'Password Change Successfully')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,'store/changepass1.html',{'form':fm,'categories':category})
    
    else:
        return HttpResponseRedirect('/login/')

def changepass1(request):
    category = Category.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.info(request,'Password Change Successfully')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request,'store/changepass2.html',{'form':fm,'categories':category, 'subcates':subcates})
    
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    messages.info(request,'logout')
    return HttpResponseRedirect('/')

def productview(request,id):
    mains = id
    product = Product.objects.all().order_by('?')
    category = Category.objects.all() 
    cloth = Product.objects.get(pk=id)
    print('cloth_date',cloth.date.day)
    i =0
    m = [] 
    for products in product:
        if products.category == cloth.category:
            if products.id != cloth.id:
                i=i+1
                print(products.name)
                m.append(products)                       
                if i==4:
                    print(m) 
                    break               
                else:
                    pass   
    products = Product.objects.get(pk=id)
    customer_name = request.session.get('name') 
    # available = Product.objects.get(pk=id)
    print('namehgwjhdja',customer_name)
    if customer_name:
        customer_name = request.session.get('name') 
        cus_id = request.session.get('customer_id')
        custo = User.objects.get(pk=cus_id)
        names = custo
        print(names)
        product = Product.objects.get(pk=id)
        print(product.id)
        print('hello',Review.id)
        if request.method == 'POST':
            fm = Reviewform(request.POST)
            if fm.is_valid():    
                cus_id = request.session.get('customer_id')
                custo = User.objects.get(pk=cus_id)
                names = custo.id
                customer_names = custo.username
                print(names)
                productss = Product.objects.get(pk=id)
                print(productss.id)
                user_names = custo.username
                ratings = fm.cleaned_data['rating']
                comment = fm.cleaned_data['comments']
                customer_name = request.session.get('name') 
                feedback = Review(product=productss,customer=custo,user_name=user_names,rating=ratings,comments=comment)
                feedback.save()
                r = productss.review_count + 1
                print(r,'r')  
                print('product',productss.rating)  
                print('rating',ratings)            
                a = productss.rating + ratings
                l = a/r
                names = productss.name
                prices = productss.price
                categorys = productss.category
                sub = productss.subcategory
                image = productss.images
                image1 = productss.images1
                image2 = productss.images2
                quantitys = productss.quantity
                offers =  productss.offer   
                des = productss.description 
                one_day_offer = productss.one_day_offer 
                bran = productss.brand
                date = product.date
                final = Product(id=mains,name=names,description=des,price=prices,category=categorys,subcategory=sub, quantity=quantitys,offer=offers,rating=l,review_count=r,brand=bran,one_day_offer=one_day_offer,images=image,images1=image1,images2=image2,date=date)  
                final.save()                          
                print('bye',a)
                feedback = Review.objects.all()                  
            fm = Reviewform()
        else:   
            print('name',request.session.get('name')) 
            customer_name = request.session.get('name')        
            fm = Reviewform()
            feedback = Review.objects.all()            
            print(Review.id)

        return render(request,'store/productview.html',{'products':products,'categories':category,'form':fm,'feedbacks':feedback,'customer_names':customer_name,'ms':m, 'subcates':subcates})
    
    else:
        return render(request,'store/productview.html',{'products':products,'categories':category,'ms':m, 'subcates':subcates})

def addtocart(request,id):
    category = Category.objects.all()
    q = request.session.get('q')
    print('q',q)
    user__id = request.session.get('ii')
    print('user__id',user__id)
    mn = cache.get('user_cartt', 0,version=user__id)
    print('mn',mn)
    if mn == 0 or mn == None:
        pass
    else:
        request.session['q'] = mn
        print(q)
        bb = request.session.get('q')
        print('bb',bb)
    q = request.session.get('q')
    print('ky matter ahe',q)
    if not q:
        request.session['q'] = []
        nn = request.session.get('q')
        print('nn',nn)
    else:
        q = request.session.get('q')
    print('ky matter ahe',q)
    if request.method == 'POST':
        product_id = int(id)
        print('product_idhhhhhhhhhhhhhhhhhhhhhhhhhhh',product_id)
        idd = product_id
        print(type(product_id))
        products = Product.objects.get(pk=id)
        vau = request.POST.get('product')
        quantity = request.POST.get('quantity')
        print(quantity)
        quantity = int(quantity)
        products.id = request.session.get(products.id)

        # print(quantity)
        # quantity = int(quantity)
        # products.id = request.session.get(products.id)
        # if products.id:
        #     pass
        # else:
        #     product_id = {}
        #     product_id[idd] = quantity
        # print(product_id)
        # print(q)
        # q.append(product_id)
        # print(q)
        # request.session['q'] = q
        # q = request.session.get('q')

        if products.id:
            print('inside product.id',product.id)
            pass
        else:
            product_id = {}
            product_id[idd] = quantity
        print(product_id)
        print(type(q))
        q.append(product_id)
        print(q)
        request.session['q'] = q
        q = request.session.get('q')
        user__id = request.session.get('ii')
        print('user__id',user__id)
        cache.set('user_cartt', q, 60*60*5 ,version=user__id)
        # carts = request.session.get('carts')
        # if carts:
        #         carts[int(product_id)] = quantity
        #         print('cart inside if and if',carts)
        # else:
        #     carts = {}
        #     carts[int(product_id)]=quantity
        #     print('anothercarts',carts)
        # request.session['carts']=carts
    else:
        carts = request.session.get('carts')
        products = Product.objects.get(pk=id)
    return render(request,'store/addtocart.html',{'product':products ,'categories':category, 'subcates':subcates})

def user_cart(request):
    category = Category.objects.all()
    # carts = request.session.get('carts')
    q = request.session.get('q')
    print('q',q)
    user__id = request.session.get('ii')
    print('user__id',user__id)
    mn = cache.get('user_cartt', 0,version=user__id)
    print('mn',mn)
    request.session['q'] = mn
    q = request.session.get('q')
    if q:
        q = request.session.get('q')
    else:
        q = None
        
    products = Product.objects.all()  
    category = Category.objects.all()  
    return render(request,'store/cart.html',{'usercarts':q,'products':products,'categories':category, 'subcates':subcates})
    
def search(request):
    category = Category.objects.all()
    search = request.GET.get('search')
    print(search)
    if search:
        match = Product.objects.filter(Q(name__icontains=search)|Q(description__icontains=search))
        print(match)
        # perform AND operation
        # match = Product.objects.filter(name__icontains=search).filter(description__icontains=search)
        if match:
            return render(request,'store/search.html',{'products':match,'categories':category,'subcates':subcates})    
        else:
            content = 'No Result Found'
            return render(request,'store/search.html',{'contents':content,'categories':category,'subcates':subcates})
    else:
        content = 'Please Enter Something in Search Box'
        return render(request,'store/search.html',{'content':content,'categories':category,'subcates':subcates})

def order(request,id):
    category = Category.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Userorderform(request.POST)
            if fm.is_valid():
                # quantitys = fm.cleaned_data['quantity']
                # addresss = fm.cleaned_data['address']
                # mobiles = fm.cleaned_data['mobile']
                # pincodes = fm.cleaned_data['pincode']
                # error_message = None
                # if not quantitys:
                #     error_message = 'Enter quantity of product'
                # elif quantitys <= 0:
                #     error_message = 'Quantity of product should not be "zero" or less than that.'
                # elif not addresss:
                #     error_message = 'Please enter Address.'
                # elif len(addresss) <= 10:
                #     error_message = 'Address is invalid , Address Should be More Than 10 Words.'
                # elif not mobiles:
                #     error_message = 'Please Enter Mobile Number.'
                # elif len(mobiles) < 10 or len(mobiles) > 10:
                #     error_message = 'Mobile Number Should 10 Digits.'
                # elif not pincodes:
                #     error_message = 'Please Enter Pincode Number.'
                # elif len(pincodes) < 6 or len(pincodes) > 6:
                #     error_message = 'Mobile Number Should 6 Digits.'
                
                # if not error_message:
                product = Product.objects.get(pk=id)
                cus_id = request.session.get('customer_id')
                custo = User.objects.get(pk=cus_id)
                product_names = product
                print(product.id)
                names = custo
                # print('names',names.first_name)
                prices  = product.price
                quantitys = fm.cleaned_data['quantity']
                print('hello',quantitys)
                # total = prices*quantitys
                if product.offer != 0:
                    a = product.price * product.offer
                    b = a/100
                    offers_price = product.price - b
                else:
                    offers_price = product.price
                total = offers_price * quantitys
                addresss = fm.cleaned_data['address']
                mobiles = fm.cleaned_data['mobile']
                pincodes = fm.cleaned_data['pincode']
                details = Userorder(product=product_names,order_id=product.id,customer=names,quantity=quantitys,offer=product.offer,address=addresss,mobile=mobiles,price=total ,pincode=pincodes)
                print('qbhsj',quantitys)
                cloths = Product.objects.get(pk=id)
                cloths_quantity = cloths.quantity
                print(type(cloths_quantity)) 
                if cloths_quantity != 0: 
                    if cloths_quantity >= quantitys:
                        cloths_quantity = cloths_quantity - quantitys
                        cloths_price = cloths.price
                        cloths_name = cloths.name
                        cloths_desc = cloths.description
                        cloths_img = cloths.images
                        cloths_img1 = cloths.images1
                        cloths_img2 = cloths.images2
                        cloths_category = cloths.category 
                        cloths_subcategory = cloths.subcategory 
                        cloths_offer = cloths.offer 
                        cloths_one_day_offer = cloths.one_day_offer  
                        cloths_brand = cloths.brand  
                        cloths_rat = cloths.rating  
                        cloths_date = cloths.date  

                        # error_message = None
                        # if not quantitys:
                        #     error_message = 'Enter quantity of product'
                        # elif quantitys <= 0:
                        #     error_message = 'Quantity of product should not be "zero" or less than that.'
                        # elif not addresss:
                        #     error_message = 'Please enter Address.'
                        # elif len(addresss) <= 10:
                        #     error_message = 'Address is invalid , Address Should be More Than 10 Words.'
                        # elif not mobiles:
                        #     error_message = 'Please Enter Mobile Number.'
                        # elif len(mobiles) < 10 or len(mobiles) > 10:
                        #     error_message = 'Mobile Number Should 10 Digits.'
                        # elif not pincodes:
                        #     error_message = 'Please Enter Pincode Number.'
                        # elif len(pincodes) < 6 or len(pincodes) > 6:
                        #     error_message = 'Mobile Number Should 6 Digits.'
                        
                        # if not error_message:
                        product_info = Product(id=id,name=cloths_name,offer=cloths_offer,description=cloths_desc,images=cloths_img,price=cloths_price,quantity=cloths_quantity,category=cloths_category, subcategory=cloths_subcategory ,one_day_offer=cloths_one_day_offer,brand=cloths_brand,rating=cloths_rat,images1=cloths_img1,images2=cloths_img2,date=cloths_date)  
                        product_info.save()                         
                        details.save()
                        available = Product.objects.all()
                        q = request.session.get('q') 
                        if q:
                            q = request.session.get('q')
                            print(q)
                            print('very near',product.id)
                            k = 0
                            for i in q:
                                print(i)
                                for key in i:
                                    print(key)
                                    k = k + 1
                                    print(k)
                                    if int(key) == int(product.id):
                                        print(k)
                                        n = k - 1
                                        print('hhh')
                                        del q[n]
                            print(q)
                            request.session['q'] = q  
                        else:
                            pass  
                        print('qqqqqq',q) 
                        user__id = request.session.get('ii')
                        print('user__id',user__id)
                        cache.set('user_cartt', q, 60*60*5 ,version=user__id)
                        mn = cache.get('user_cartt',version=user__id)
                        print('cache_set',mn)

                        # if 'carts' in request.session:
                        #     carts = request.session.get('carts')
                            # print('cart',carts)
                            # for cart in carts:
                            #     print('product_id',id) 
                            #     print('cart',cart) 
                            # llll = request.session['carts'].keys()
                            # print(llll)
                            # print(request.session.get('carts'))
                            # print(request.session['carts'])
                            # for key in request.session['carts']:
                            #     print(key)
                            #     if int(key) == int(product.id):
                            #         print('hellllllo')
                            #         a = request.session['carts']['key']
                            #         del a
                            # del request.session['carts']
                        detail = Userorder.objects.all()
                        return render(request,'store/order.html',{'products':detail,'nm':names,'categories':category,'availables':available, 'subcates':subcates})
                    else:
                        messages.warning(request,'not available')
                else:
                    messages.warning(request,'not available') 
                # else:
                #     return render(request,'store/buy.html',{'products':detail,'nm':names,'categories':category,'error_message':error_message}) 


        else:
            cus_id = request.session.get('customer_id')
            print(cus_id)
            custo = User.objects.get(pk=cus_id)
            print(custo)
            fm = Userorderform()
        return render(request,'store/buy.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

def orders(request):            
    category = Category.objects.all()
    cus_id = request.session.get('customer_id')
    custo = User.objects.get(pk=cus_id)
    names = custo
    print(names)
    detail = Userorder.objects.all()
    return render(request,'store/order.html',{'products':detail,'nm':names,'categories':category, 'subcates':subcates})
    # for i in detail:
    #     if i.customer == custo:
    #         return render(request,'store/order.html',{'products':detail,'nm':names,'categories':category})
    #     else:
    #         nm = False
    #         return render(request,'store/order.html',{'nm':nm})

def top_offer(request):
    products = Product.objects.all()
    category = Category.objects.all()
    about = 'Offer Products'
    product_offer = []
    for product in products:
        if product.offer > 0:
            product_offer.append(product)
    return render(request,'store/top_offer.html',{'products':product_offer,'categories':category,'about':about, 'subcates':subcates})

def best_battery(request):
    products = Product.objects.all()
    category = Category.objects.all()
    about = 'Best Battery Mobiles'
    product_battery = []
    for product in products:
        if product.battery > 4000:
            product_battery.append(product)
    return render(request,'store/top_offer.html',{'products':product_battery,'categories':category,'about':about, 'subcates':subcates})

def top_rated(request):
    products = Product.objects.all()
    category = Category.objects.all()
    about = 'Top Rated Products'
    product_rated = []
    for product in products:
        if product.rating > 4:
            product_rated.append(product)
    return render(request,'store/top_offer.html',{'products':product_rated,'categories':category,'about':about, 'subcates':subcates})

def buyquantity(request,id):
    product = Product.objects.get(pk=id)
    category = Category.objects.all()
    if request.method == "POST":
        fm = Userorderform()
        quantity = request.POST['quantity']
        print(quantity)
        a = int(product.price) * int(product.offer)
        print(a)
        b = a/100
        print(b)
        c = int(product.price) - int(b)
        print(c)
        products = int(quantity) * c
        print(products)
        return HttpResponseRedirect('/onlinebuy/')
    else:
        return render(request,'store/buyquantity.html',{'product':product,'categories':category, 'subcates':subcates})

def onlinebuy(request):
    return render(request,'store/onlineby.html')

def subfilter(request,id):
    product = Product.objects.filter(subcategory = id)
    subcates = SubCategory.objects.all()
    category = Category.objects.all()


    for products in product:
        cate = products.category
        print('catteeeeeeeeee',cate)
        break
    
    for products in product:
        subcate = products.subcategory
        print(subcate)
        break

    g = []
    if request.GET.get('ywc'):
        g.append(request.GET.get('ywc'))
    if request.GET.get('samsung'):
        g.append(request.GET.get('samsung'))
    if request.GET.get('iphone'):
        g.append(request.GET.get('iphone'))
    if request.GET.get('realme'):
        g.append(request.GET.get('realme'))
    if request.GET.get('redmi'):
        g.append(request.GET.get('redmi'))
    if request.GET.get('nike'):
        g.append(request.GET.get('nike'))
    if request.GET.get('Monte_Carlo'):
        g.append(request.GET.get('Monte_Carlo'))
    if request.GET.get('Louis_Philippe'):
        g.append(request.GET.get('Louis_Philippe'))
    if request.GET.get('Peter_England'):
        g.append(request.GET.get('Peter_England'))
    if request.GET.get('Allen_Solly'):
        g.append(request.GET.get('Allen_Solly'))
    if request.GET.get('fastrack'):
        g.append(request.GET.get('fastrack'))
    if request.GET.get('sony'):
        g.append(request.GET.get('sony'))
    four = request.GET.get('four')
    ranges = request.GET.get('range')
    three = request.GET.get('three')
    two = request.GET.get('two')
    one = request.GET.get('one')
    print(g)

    filter_product = []
    offer = request.GET.get('offer')
 
    if four or three or two or one or offer or ranges or g:
        filter_product = forfilter(g,four,ranges,three,two,one,offer,filter_product,product)
        return render(request,'store/filter.html',{'cate':subcate,'products':filter_product,'categories':category, 'subcates':subcates})
    else:   
        return render(request,'store/filter.html',{'products':product,'categories':category, 'cate':subcate,'subcates':subcates})

def forfilter(g,four,ranges,three,two,one,offer,filter_product,product):
    if g:
        for products in product:
            for i in g:
                if i == products.brand:
                    
                    if product in filter_product:
                        pass
                    else:
                        filter_product.append(products)
    if four:
        for products in product:
            if products.rating >= 4:
                if products in filter_product:
                    pass
                else:
                    filter_product.append(products)
                print(filter_product)
    if three:
        for products in product:
            if products.rating >= 3:
                if products in filter_product:
                    pass
                else:
                    filter_product.append(products)
    if two:
        for products in product:
            if products.rating >= 2:
                if products in filter_product:
                    pass
                else:
                    filter_product.append(products)
    if one:
        for products in product:
            if products.rating >= 1:
                if products in filter_product:
                    pass
                else:
                    filter_product.append(products)
    if offer:
        for products in product:
            if int(offer) <= products.offer:
                if products in filter_product:
                    pass
                else:
                    filter_product.append(products)

    if ranges:
        for products in product:
            offers = products.offer
            offer_price = products.price
            print(offers)
            if offers != 0:
                a = offer_price * offers
                # a =int(a)
                b = a/100
                # b = int(b)
                c = offer_price - b
                # c = int(c)
            else:
                c = products.price 
            if int(ranges) >= c:
                print('hello')
                if products in filter_product:
                    print('hiii')
                    pass
                else:
                    print('please')
                    filter_product.append(products)
    return filter_product

def delete(request,id):
    subcates = SubCategory.objects.all()
    category = Category.objects.all()

    return render(request, 'store/delete.html', {'categories':category, 'subcates':subcates ,'id':id})

def del_account(request,id):
    custo = User.objects.get(pk = id).delete()
    return HttpResponseRedirect('/')

class pdfdetail(PDFTemplateResponseMixin,DetailView):
    template_name = 'store/pdf.html'
    context_object_name = 'order'
    model = Userorder

def addcategory(request):
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    if request.method == "POST":
        fm = Productcategory(request.POST)
        if fm.is_valid():
            print('name',fm.cleaned_data['name'])
            fm.save()
            fm = Productcategory()
    else:
        fm = Productcategory()
        print('fm')
    return render(request,'store/addcategory.html',{'form':fm,'categories':category,'subcategories':subcategory})

def addsubcategory(request):
    if request.method == "POST":
        fm = Productsubcategory(request.POST)
        if fm.is_valid():
            print('name',fm.cleaned_data['name'])
            fm.save()
            fm = Productsubcategory()
    else:
        fm = Productsubcategory()
        print('fm')
    return render(request,'store/addsubcategory.html',{'form':fm})

def addproduct(request):
    if request.method == "POST":
        fm = Productform(request.POST,request.FILES)
        if fm.is_valid():
            print('name',fm.cleaned_data['name'])
            fm.save()
            fm = Productform()
    else:
        fm = Productform()
        print('fm')
    return render(request,'store/addproduct.html',{'form':fm})

