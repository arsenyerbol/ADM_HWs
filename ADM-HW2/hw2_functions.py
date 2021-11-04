import pandas as pd
import matplotlib as mlp
import operator
import matplotlib.pyplot as plt
#------------------------ RQ1 -----------------------------

def complete_funnel_rate(df):
    # checking user_ids interested by each of the three events
    view=df[df.event_type=='view'].groupby([df.user_id]).count().index.tolist()
    cart=df[df.event_type=='cart'].groupby([df.user_id]).count().index.tolist()
    purchase=df[df.event_type=='purchase'].groupby([df.user_id]).count().index.tolist()

    # intersecting indexes of each of the three dataframes with no repetition
    complete_funnels=len((set(cart)).intersection(set(purchase)).intersection(set(view)))

    # counting numbers of user_id which were involved in all three event_types
    tot_ids=len(df.groupby(df.user_id).count().index)
    print(f'Rate of complete funnels: {round(complete_funnels/tot_ids*100,2)}%')

def event_types(df):
    # checking mean occurrence of the three event_types for user_session
    view_mean=df[(df.event_type == "view")].groupby(['user_session']).event_type.count().mean()
    cart_mean=df[df.event_type == "cart"].groupby(['user_session']).event_type.count().mean()
    purchase_mean=df[df.event_type == "purchase"].groupby(['user_session']).event_type.count().mean()

    # creating a dictionary with 3 values and plotting
    events={'view':view_mean,'cart':cart_mean,'purchase':purchase_mean}
    bars=pd.DataFrame(events,index=['event_type'])
    bars.plot(kind='bar',figsize=(3,5),rot=0,colormap='Pastel2');
    print('Operation that users repeat more on average within a session: ',bars.idxmax(axis=1)[0])

def views_before_cart(df):
    # creating two dataframes filtered for event type
    cart_df=df[df.event_type=='cart'].groupby([df.user_id,df.product_id]).count()
    view_df=df[df.event_type=='view'].groupby([df.user_id,df.product_id]).count()

    # filtering dataframe for user_id that added a product to cart
    view_df=cart_df.merge(view_df,how='inner',left_index=True,right_index=True,suffixes=('_cart','_view'))

    # counting how many times in avarage users who also add a product to cart have viewed the product
    mean_views=view_df['event_time_view'].mean()

    print (f'In avarage a user views a product {round(mean_views,2)} times before adding it to cart')

def rate_cart_and_purchase(df):
    # Checking avarage occurence of cart event_type grouped by user_id and product_id
    cart=df[df.event_type=='cart'].groupby([df.user_id,df.product_id]).event_type.count().mean()
    
    # Avarage occurrence of purchase event_type grouped by user_id an product_id
    purchase=df[df.event_type=='purchase'].groupby([df.user_id, df.product_id]).event_type.count().mean()
    print (f'A user who adds a product to cart buys that product in the {round(purchase/cart,2)*100}% of cases')


def take_first(x):
    return x[0]  
    
def interval_from_firstview(df):
    # Extracting event_time grouped by user_id and product_id for the event types cart and view
    df_cart=df[df.event_type=='cart'].groupby([df.product_id,df.user_id]).event_time.unique().to_frame()
    df_view=df[df.event_type=='view'].groupby([df.product_id,df.user_id]).event_time.unique().to_frame()

    # Keeping only combinations of user_id and product_id common to the two events type 
    df_view = df_view.merge(df_cart,how='inner',left_index=True,right_index=True,suffixes=('_view','_cart'))
    df_cart=0
    # Extracting first time stamp for event type (we want to consider time interval from the first visualization)  
    df_view = df_view.applymap(take_first)

    #applying parsing
    df_view['event_time_view']=pd.to_datetime(df_view.event_time_view)
    df_view['event_time_cart']=pd.to_datetime(df_view.event_time_cart)

    # Calculating time interval between two time stamps and calculating the mean
    df_view['interval'] = df_view['event_time_cart'] - df_view['event_time_view']
    mean_time = df_view['interval'].mean()
    print(f' On avarage a product is added to cart {mean_time} after the first view')

#------------------------ RQ2 -----------------------------

def trending_categories(df):
    # sorting categories according to counts
    sort_cat=df[df.event_type=='purchase'].groupby('category_code').category_code.count().sort_values(ascending=False).head(10)
    sort_cat.plot(figsize=(20,4),kind='bar',title='Product categories',fontsize=10,colormap='Set3')

def top10_prods_for_category(df):
    cat_list=df[df.event_type=='purchase'].groupby('category_code').event_type.count().sort_values(ascending=False).head(10).index.tolist()
    # Iterating through top 10 categories interested by the purchase event
    for category in cat_list:
        # creating a list with best 10 products for each category
        p_id=df[(df.event_type=='purchase') & (df.category_code==category)].groupby(df.product_id).event_type.count().sort_values(ascending=False).head(10).index.tolist()
        print (f'\nCategory: {category}')
        print (*p_id)

# -----------------------RQ_3-------------------------
# We filter by purchase and by category selected (parameter of 1).
# We group by brands in the category
# We calculate the average price ( .price.mean()) for each brand in the category
# We plot out results
def f1(df,category,month):
    res = df[(df.event_type == 'purchase') & (df.category_code == category)].groupby([df.brand]).price.mean()
    plt.subplot(2,1,1)
    res.plot.bar(figsize = (17 , 14) , color = "orange")
    plt.title(f"Average price of Products sold for Brand - {month}", color = "orange", fontsize = 18)
    plt.xlabel("Brands", color = "orange", fontsize = 18)
    plt.ylabel("Average Price in $", color = "orange", fontsize = 18)
    return res

# In order to find the brand with the highest average price for the selecter category:
# We filter by "purchase" our database
# We group by brand and for each brand in the category we calculate the average price with "price.mean()"
# We sort values and take the highest value
def f2(df,category):
    res= df[(df.event_type == 'purchase') & (df.category_code == category)].groupby([df.brand]).price.mean().sort_values(ascending = False).head(1)
    print(f'\n {res} is the brand with the highest average price')
    

# In[ ]:
# In[ ]:


#--------------------------------------------------------RQ_4----------------------------------------------------------------

# We filter by purchase and group by Brand. Then we can calculate the total amount of sold product and obtain the earnings of the month.
def f3(brand_selected,df):
    res = df[(df.event_type == 'purchase') & (df.brand == brand_selected)].price.sum()
    print('\n' + brand_selected + " earned in total ($)")
    print(res)

   
def f4(df): 
    # We sort in 2 different ways to take the highest and lowest brand, with function .head(1)
    # We save the Brand with the highest average price, regardless the category
    maxim = df[df.event_type == 'purchase'].groupby([df.brand]).price.mean().sort_values(ascending = False).head(1)
    minim = df[df.event_type == 'purchase'].groupby([df.brand]).price.mean().sort_values().head(1)
    lista_prezzi = df[df.event_type == 'purchase'].groupby([df.brand]).price.mean().sort_values().tolist()
    print('\n',maxim) 
    print('\n',minim)
    # We print the difference in price between the 2 brands.
    print('\nDelta price' , lista_prezzi[-1] - lista_prezzi[0])
    

# In order to kwow the percentage loss in earnings in 2 months, we filter by purchases both datasets
def f5(df1,df2):
    df1 = df1[df1.event_type == 'purchase']
    df2 = df2[df2.event_type == 'purchase']
    thisdict = {}

    # For each brand we compute the earnings in 2 months
    for brand_selected in df1['brand'].unique() :
        res = df1[df1.brand == brand_selected].price.sum() #month 1
        res2 = df2[df2.brand == brand_selected].price.sum() #month 2
        if res2 < res :
            delta = res - res2 #delta is a difference($) between earnings in the 2 months
            percentage_loss = (delta * 100)/ res
            thisdict[brand_selected] = percentage_loss
    #Let's create a dict{key:value -----> Brand:Percentage_loss}
    #Transform the dict in a dataframe
    df = pd.DataFrame(thisdict.items() , columns=['Brand', 'Percentage_loss'])
    df = df.sort_values(by =  'Percentage_loss' , ascending = False)
    print(df.head(3))


# In[ ]:

#--------------------------------------------------------RQ_5----------------------------------------------------------------

# We filter by views because is the most mainingful event_type to understand the amount of people that go on the online store
# We group by hours and count the event_type (only views) that we find hour by hour
# We sort them
def f6(df):
    df['event_time']=pd.to_datetime(df.event_time)
    df = df.loc[df.event_type == 'view']
    visite_orarie = df.groupby([df.event_time.dt.hour , 'event_type']).event_type.count().sort_values(ascending = False)
    print('This is the part of the day (hour) in which there are more visits:')
    print(visite_orarie.head(1))


# We filter by views because is the most mainingful event_type to understand the amount of people that go on the online store   
def f7(df):
    x = ['Lun', 'Mar' ,'Mer', 'Gio', 'Ven', 'Sab' , 'Dom']
    df['event_time']=pd.to_datetime(df.event_time)
    df = df.loc[df.event_type == 'view']
    y = []
    #Let's compute the hourly_average on days of week, thanks to the function .dt.dayofweek
    for i in range (0,7):
        df_M = df[df.event_time.dt.dayofweek == i ]#Lun = 0 .... Dom = 6
        hourly_average_M = (df_M.event_type.count())/24 #total views / 24 hours --> for the average
        y.append(hourly_average_M)
    #plt.subplot(1,2,1)
    plt.plot(x, y, linewidth = 1.0, ls = '-', marker = "o", markersize = 10 )
    plt.show()

#--------------------------- RQ6 ---------------------------------

def overall_conversion_rate(df):    
    # look to mean count of viewed and purchases rate of products
    purchase_rate = df[df.event_type=='purchase'].shape[0]
    views = df[df.event_type=='view'].shape[0]
    # conversion rate = (number of puchases / number of views) * 100
    conversion_rate = (purchase_rate / views) * 100
    print('The overall conversion rate is:',round(conversion_rate,3), '%')

def purchase_rate_category(df):
   # found the all purchases and views of each category in dataframe
    purchased_category_df = df.iloc[:,[1,3]][df.iloc[:,[1,3]].event_type == 'purchase'].groupby(df['category_code']).count().iloc[:,1].to_dict()
    viewed_category_df = df.iloc[:,[1,3]][df.iloc[:,[1,3]].event_type == 'view'].groupby(df['category_code']).count().iloc[:,1].to_dict()
    # count conversion rate for each category
    conversion_category_rate = {i: round(purchased_category_df[i]/viewed_category_df[i] * 100,3) for i in purchased_category_df.keys() & viewed_category_df}
    conversion_category_rate = sorted(conversion_category_rate.items(), key=operator.itemgetter(1),reverse=True)
    print ('conversion rate in decreasing order: \n ')
    print(*conversion_category_rate[:10],sep='\n')

    #count purchase rate for each category
    purchase_rate = df[df.event_type=='purchase'].shape[0]
    plot = {k: round((v / purchase_rate)*100,2) for k, v in purchased_category_df.items()}
    plot = {key: value for key, value in plot.items() if value >= 0.2}
    # draw the plot
    labels = plot.items()
    sizes = plot.values()
    plot = list(plot)
    fig = plt.gcf()
    fig.set_size_inches(20, 16)
    plt.barh(plot, sizes, align='center', alpha=0.5, color = 'orange')
    plt.yticks(plot, labels)
    plt.ylabel('Categories')
    plt.title('Purchase rate of each category')
    plt.show()

#--------------------------- RQ7 ---------------------------------

def pareto(parameter,df):
    all_money = df[df.event_type == 'purchase'].groupby(df[parameter]).price.sum().sort_values(ascending=False).tolist() 
    minor_money = all_money[0 : int(len(all_money) * .2)]
    pareto = (sum(minor_money)/sum(all_money)) * 100
    print('The 20 percent of',parameter, 'gave',round(pareto,2),'% of profit')