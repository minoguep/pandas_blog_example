import pandas as pd
import time


def special_offer(discount):
    if discount > 0.5:
        return 1
    else:
        return 0

### READ IN THE 3 DATA SETS ###
# dataset containing some information on orders/sales from the store
orders = pd.read_excel('./data/input_data/superstore.xls', sheet_name='Orders')
# dataset containing information on returned orders
returns = pd.read_excel('./data/input_data/superstore.xls', sheet_name='Returns')
# dataset containing information on the managers for each region in the orders dataset
people = pd.read_excel('./data/input_data/superstore.xls', sheet_name='People')

###  Merge the datasets together ###
print('--------------------MERGING DATA-------------------------')

merged_df = (orders.merge(returns, how='left', on='Order ID')
            .merge(people, on='Region'))
merged_df.to_csv('data/output_data/merged_data.csv', index=False)

print('Merged data output to data/output_data/merged_data.csv')
print('---------------------------------------------------------')

### FILTERING EXAMPLES ###
print('----------FILTERING EXAMPLE 1: NOT RETURNED--------------')

not_returned_df = merged_df.loc[merged_df['Returned'].isna(), :]

not_returned_df.to_csv('data/output_data/filtering_example_1.csv', index=False)

print('Result output to data/output_data/filtering_example_1.csv')
print('---------------------------------------------------------')

print('----------FILTERING EXAMPLE 2: NOT RETURNED IN JAX--------------')

not_returned_jax = merged_df.loc[(merged_df['Returned'].isna())
                                 & (merged_df['City'] == 'Jacksonville'), :]

not_returned_jax.to_csv('data/output_data/filtering_example_2.csv', index=False)

print('Result output to data/output_data/filtering_example_2.csv')
print('----------------------------------------------------------------')


### AGGREGATION?GROUPBY EXAMPLES ###


print('----------AGGREGATION EXAMPLE 1: MEAN()-----------------')

agg_example_1 = not_returned_df.groupby(by='Region')['Profit'].mean()

print(agg_example_1)

print('---------------------------------------------------------')


print('------------AGGREGATION EXAMPLE 2: AGG()-----------------')

agg_example_2 = not_returned_df.groupby(by='Region').agg({'Profit':'mean',
                                            'Sales':'median'})

print(agg_example_2)

print('---------------------------------------------------------')

### PIVOT EXAMPLE ###

print('-------------------PIVOT EXAMPLE------------------------')

# first lets group by person and category
data_for_pivot = not_returned_df.groupby(by=['Person', 'Category'])['Profit'].sum().reset_index()

data_for_pivot = pd.DataFrame(data_for_pivot.pivot(index='Category', columns='Person', values='Profit').to_records())

print(data_for_pivot)

print('---------------------------------------------------------')

### UNPIVOT EXAMPLE ###

print('--------------------UNPIVOT EXAMPLE----------------------')

unpivoted_data = data_for_pivot.melt(id_vars=['Category'])
unpivoted_data.columns = ['category', 'person', 'profit']

print(unpivoted_data)

print('---------------------------------------------------------')

### CUSTOM FUNCTIONS AND TIME ###

print('----------------CUSTOM FUNCTION COMPARISON---------------')
start_time_apply = time.time()
not_returned_df.loc[:, 'special_offer'] = not_returned_df.apply(lambda row: special_offer(row['Discount']), axis=1)
print ("Time to run apply method:", time.time() - start_time_apply)


start_time_loc = time.time()
not_returned_df.loc[:, 'special_offer'] = 0
not_returned_df.loc[not_returned_df['Discount'] > 0.5, 'special_offer'] = 1

print ("Time to run .loc method:", time.time() - start_time_loc)

not_returned_df.to_csv('data/output_data/custom_function_example.csv', index=False)

print ("Custom function example output to  data/output_data/custom_function_example.csv")
print('---------------------------------------------------------')

### CREATE ONE HOT ENCODINGS ###

print('-------------------ONE HOT ENCODING----------------------')

dummy_variables = pd.get_dummies(not_returned_df['Category']).head()
not_returned_df = pd.concat([not_returned_df, dummy_variables], axis=1)

dummy_variables.to_csv('data/output_data/dummy_variables.csv')

print('Dataframe with dummy variables output to data/output_data/data_with_dummies.csv')
print('---------------------------------------------------------')

### PLOTS ###

print('-------------------SALES DISTRIBUTION-------------------')
ax = not_returned_df.loc[not_returned_df['Sales'] < 1000, 'Sales'].plot.hist(bins=50)
fig = ax.get_figure()
fig.savefig('./data/output_data/histogram.png')

print('Plot saved at data/output_data/histogram.png')
print('---------------------------------------------------------')

print('--------------------SALES V DISCOUNT----------------------')
ax = not_returned_df.plot.scatter(x='Sales', y='Discount')
fig = ax.get_figure()
fig.savefig('./data/output_data/scatter.png')

print('Plot saved at data/output_data/scatter.png')
print('---------------------------------------------------------')