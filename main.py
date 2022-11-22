import pandas as pd
import panel as pn
import numpy as np
pn.extension('tabulator')
import hvplot.pandas
import pymongo
from pymongo import MongoClient
import datetime as dt
from bokeh.models import HoverTool

params=pd.read_excel('DCS Parameters.xlsx')
params['Date_Exact'] =params['Date'].apply(lambda date: date.strftime("%d/%m/%Y"))
params['Date']=pd.to_datetime(params['Date'])
params['Run Hour']=params['Run_HR']
params["Production MT"]=(params['Production'])
params['Power KW']=(params['Power'])
params['Month']=params['Date'].dt.month
params

yaxis_params = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=["Production MT", 'Run Hour','Power KW'],
    button_type='primary'
)

iparams=params.interactive()
month_slider = pn.widgets.IntSlider(name='Month', start=9, end=12, value=9)
month_slider

a=iparams.groupby(['Month','Section'])[yaxis_params].sum()
a.round(decimals = 2)

options = ['Crusher', 'RM1', 'RM2', 'Kiln', 'Coal Mill']
params_pipeline = (
    iparams[(iparams.Month == month_slider) & (iparams.Section.isin(options))].groupby(['Month', 'Section'])[
        yaxis_params].sum().to_frame())  # .reset_index())

params_pipeline=params_pipeline.round(decimals = 2)

params_table = params_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size = 10, sizing_mode='stretch_width')
params_table

yaxis_params1 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=["Production MT", 'Run Hour','Power MW'],
    button_type='primary'
)

options = ['Crusher','RM1','RM2','Kiln','Coal Mill']
params1=params[['Section','Date','Month','Production MT','Run Hour','Power KW']]
params1['Production MT']=(params1['Production MT'])/1000
params1['Power MW']=(params1['Power KW'])/1000
iparams1=params1.interactive()
params_pipeline1 = (iparams1[(iparams1.Section.isin(options))].groupby(['Section','Date'])[yaxis_params1]
                    .sum().to_frame().reset_index())
params_pipeline1

yaxis_section1 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['Crusher','RM1','RM2','Kiln','Coal Mill'],
    button_type='primary'
)

params_pipeline1=params_pipeline1[params_pipeline1['Section']==yaxis_section1]
params_pipeline1=params_pipeline1.round(decimals=2)
params_pipeline1

params_line_plot = params_pipeline1.hvplot(kind='line',
                                                     x='Date',
                                                     y=yaxis_params1,color='#319F6A',
                                                     title='Sectionwise Parameters (Daily)')
params_line_plot

yaxis_params2 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=["Production MT", 'Run Hour','Power MW'],
    button_type='primary'
)

options = ['Crusher', 'RM1', 'RM2', 'Kiln', 'Coal Mill']
params_pipeline3 = (iparams1[(iparams1.Section.isin(options))].groupby(['Section', 'Month'])[
                        yaxis_params2].mean().to_frame().reset_index())

yaxis_section2 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['Crusher','RM1','RM2','Kiln','Coal Mill'],
    button_type='primary'
)

params_pipeline3=params_pipeline3[params_pipeline3['Section']==yaxis_section2]
params_pipeline3=params_pipeline3.round(decimals=2)
params_pipeline3

params_bar_plot = params_pipeline3.hvplot(kind='bar',
                                                     x='Month',
                                                     y=yaxis_params2,color='#319F6A',
                                                     title='Average Peformance',use_index = True).opts(width=300)
params_bar_plot

plant_selection = pn.widgets.Select(name='Plant', options=['Mukutban', 'Maihar', 'Chanderia','Durgapur','Satna',
                                                           'Raebareli','Kundanganj','Butibori'])

plant_selection

jpg=pn.pane.JPG('logo.jpg',width=150,height=100)
jpg

options = ['Crusher','RM1','RM2','Kiln','Coal Mill']
params_pipeline4 = (iparams1[(iparams1.Section.isin(options))].groupby(['Section','Date']).sum().reset_index())

yaxis_section4 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['Crusher','RM1','RM2','Kiln','Coal Mill'],
    button_type='primary'
)

params_pipeline5=params_pipeline4[params_pipeline4['Section']==yaxis_section4]
params_pipeline5=params_pipeline5.round(decimals=2)
params_pipeline5=params_pipeline5[['Production MT', 'Run Hour','Power MW','Date']]

from bokeh.models import HoverTool
params_line_plot1 = params_pipeline5.hvplot(x='Date',
                                           title='Sectionwise Production Parameters',yformatter = '%.0f',
                                            hover_cols=['Production MT', 'Run Hour','Power MW'],group_label='Parameters')
params_line_plot1

params_spc = params.groupby(['Month', 'Section']).sum().reset_index()
params_spc['spc']=(params_spc['Power KW']/params_spc['Production MT'])
params_spc=params_spc[['spc','Month', 'Section']]
params_spc.replace([np.inf, -np.inf], 0, inplace=True)
params_spc

iparams_spc=params_spc.interactive()

yaxis_section6 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['Crusher','RM1','RM2','Kiln','Coal Mill'],
    button_type='primary'
)

params_pipeline6=iparams_spc[iparams_spc['Section']==yaxis_section6]
params_pipeline6=params_pipeline6.round(decimals=2)
params_pipeline6

spc_bar_plot = params_pipeline6.hvplot(kind='bar',
                                                     x='Month',
                                                     y='spc',color='#319F6A',
                                                     title='Sectionwise Monthly SPC',
                                       ylabel='Specific Power Consumption',use_index = True).opts(width=300)
spc_bar_plot

params_spc1 = params.groupby(['Date', 'Section']).sum().reset_index()
params_spc1['spc1']=(params_spc1['Power KW']/params_spc1['Production MT'])
params_spc1=params_spc1[['spc1','Date', 'Section']]
params_spc1.replace([np.inf, -np.inf], 0, inplace=True)
params_spc1

iparams_spc1=params_spc1.interactive()

yaxis_section7 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['Crusher','RM1','RM2','Kiln','Coal Mill'],
    button_type='primary'
)

params_pipeline7=iparams_spc1[iparams_spc1['Section']==yaxis_section7]
params_pipeline7=params_pipeline7.round(decimals=2)
params_pipeline7

spc_plot1 = params_pipeline7.hvplot(x='Date',
                                           title='Sectionwise Daily SPC',yformatter = '%.0f',
                                            hover_cols=['spc1'],group_label='Sections',
                                   ylabel='Specific Power Consumption')
spc_plot1

template3 = pn.template.FastListTemplate(
    title='Production Dashboard',logo='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALcAAABaCAYAAAD6tMfDAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH5gsWBB4QwJTsCgAAAAFvck5UAc+id5oAAA1USURBVHja7Z19jORkHcd/HZZrufd0kDmO47g7T7p3oO4h4AEHdxfFrpiWt2PTdQV2eekCkQEN6k67gsS+LKDR/cOYXYUuySScc0ah1YSLRNCIJsaAeqi7Gu6QCNlAZkWOxBY46h/XmXS6nZnOTNtnnX0+ySbTp0+f7+95nu882+nTPgVoglBie4QSe5XbBKHEXi2UWLJZea3CGOIGxhDvbqTNGOI4Y4g74tamdYWgdeWyZnWndWWI1pXVcetjEkIosSuEEntvs44NMbkklNiVneozhsi0qu0ZfX+n2p6pb2pHn9aV01H3HaYBQom9sJ2ODZh8bzvajCGewhji/Z3qM4a4rh19Wle2dapN64qAug8xIQgldqjTzvUZ/IutaDOGuCoubc/gW1vRp3Vlb5z6tK4QqPsT4yGU2Bvj7FzP4PdE0WYM8bS4tT2Db4qiH7exK6DuUwwACCV2dxKd6xm8v5l+Utqu67qMIVKNtGldOScpbVpXWvrvhYkZocRSSZrLdV1XKLHr6+kzhnhd0vr1tGldIZLWpnXlXNR9vGwRSuxY0h1cz2CMIa5IQ5sxxO1h+rSuXI+q7piEEUosmUbnum746M0Y4kha+mH1T0ub1pXzUff1ciMDAJ9NUe+GYMLs8NRjaYkzhlgzyZSm4cpj8pG0tDAnyTxxw9M/TUvsiRuenvZvM4aY9qzeJYHtq1LWx6RIBrH+J1LWu9i/UR6TH0pTHE/Rp0vq5g5Mzbc0ydIps8NTqZo5hC2I9ZcVKEZu/+i1HnUDpAyNOoDlBApzv+f7fAJ1A6QM6tPAZQWKxn7H9/kN1A2A6V5SN/fBgcP+kXsWdQNgupfM4KF+FaH+S6gbANO9ZADgybTEBg/110wYzY1ML7dzbkyKZA4OHP5Dinq/CCb0zozuQd0ImO4kAwAweKifS1po8FD/yMGBw4tG6rmR6edRNwKmO8kAABwcOPyzFLQer7ejd2a0F3VDYLqP6tWSwUP92aREBg/1n31w4HDd2z7nRqbnemdGh1E3BqaLEUrs9rhv9RRK7K6o+owhJn5fuV8vaa0gtK7sQ93HyxqhxG6JqzOFEruzVX3GEO9I0mB+reTtXAs29xJAKLEdP6wrlNg17eozhnhBUgbz66RrbWzuJUU7pyntjNZhMIaYYQzxADY3JlGEEksKJXa/UGKlEDN/XSixrFBiT0tKnzHEsxhD7Hg9FcYQC/5yEZgbP2qGwWAwGAwGg1kEY4gEY4h7IpzPfpoxxJZuoaV1peVVZOucy95L68o5SdQ/ly/25fLFjhfmdF3XzeWL+1D3Jwaqq63e3moHMoZ4D2OIK6JoxGXugNEviqP+uXzx6rhjw+ZeAjCGeF6nHckYYlOTJWFun8nbunqTyxc3JhUTNjdi4ly3jzHEmxtpJWluz+BntVL3XL54cZLxYHMjhDHE2NfNYwzx1np6SZvbdV2X1pUNUeqetLFdF5sbGYwh7kqqUxlDDH3LQhrmdl3XpXWl4W+AJE9F/GBzIyCNlVYZQ1x0r0la5nbdxqusphUDNne6VC7dJb5A+uzw1NsoK0rryuaw9Fy++DmUcWGSI8MY4qmzw1PfTkMsbPROi/KY/M+w9PnJoTSeQsIgIO0ljK9HWVlaV071b+fyRQZlPJhkycwOTz2Vltjs8JSBuL6fDGyn+cXGpMxyW7uuxtzzk0PfQR0QJjlSNzdjiInd992M8pj8LVTamPRBvYQxBpMYKMy9yvcZv+ULkxioz7nfRN0AmO4Ftbn/jroBMN0LanP/EXUDYLqXTO/M6GWoxBcK4++jbgBM95KZG5n+LcoAshPqp1A3AqY7yQAA9M6MDqAKYKEw/kvUjYDpTjIAAHMj04dQBpGdUD+GuiEw3Uf1B2XvzOiZqIJYKIwfyU6od6FuDEx3UTX33Mj0fO/MKLIRdKEw/n3UjYHpLmouBc6NTB/pnRndgSoYgiCI7IT6VdSNgukOFl3nnhuZnu2dGV2LKqCFwvgj2Qn1crTNgukGQidx5kamjxMEQfTOjPahCGqhMP6b7IS6IjuhjiBtHUz3wxjiWsYQr4njIVnGECMtteCH1pWP0LoSyxsX/OWm9WCw7wHhPtR9icFgMBgMBoNZmtC6sonWldviOO+kdWVjK9q5fDGTyxcvj2sZYX/ZaZ9zk5x0YbB+JCctqldYO5CctDMsH8lJa5po3k1y0rpm7Rwh9nPr5Sc5aWfEMgZITsr46rSpWb3rEWy3dky9L+4OpnVlS0RTr87li1+LWx+xufdFMRXJSadHyed18vqI2g3f0hyxjEvrmLuvlfYkOWmFF3vNayFbMPaqkDI/FMwXeimQ1pUzXNd1y2Pysy1/I2Igly9ePT85dHx+cmgChT5qbFOteUKJ5KTtMZT5txjKeD6mKt6cwPF3ND2K1pWL4h6x/DQauXP5IpGkdnB0SForSNSR28u7tlkegMUjt79skpN2BMqsu6RzvThJTtodVn4gf19I2pZALItOI9oZuUlOquuRyn+ECjUjN60rl5TH5N9H/PbESi5fJOYnhz5Aob1EuQsAoJEhm+FYWnC0PruNYla1cUwYf4qpnEYLKQn+jaq5aV3ZWh6TUT64ICPUXnLYpqqTnHSabar/arcM/4+3SrERtZ+tjIa2qT5TSad4+coO6vNkTO3yc188d1O8fMC373F/3gwAAK0rRHlMPhqHeDvk8sXd85ND30Slv1SgePn2QNJXAvubLv9GctIWkpO2kZx0qW2qJwK7ZzsM8eWoGW1TPVbvlIPi5bYejiE56bxA0gwAPBXIc0Xlc+WbfVOHlW4b73Tkd6j0lxjvU7xcvZ/GNtUH/TsdS3u6WQG2qR6zTfXlsB9/jqVFGrkblH2U5KQ43hr34zb1XwokHQCALwTy/KryOUPrSqY8Js/EEHC74PWxaymGJUYZtetB8fIDFC/3tJB/P+HDv8821Vc6qRxBEIRjaS1flw67PGqbqmGbqhGSdysAQA8AXBGh7MSYnxyyUOovNRxLe5/iYSTYaVFGbQAA38h/HABeBYA/O5bmpF0Pipe3Opb2CslJBdtUtUo6yUk7HUv7axtFjkbNaJvqUYLQiB5U17IBAHL5IoVKe4lTBICquSle3h/1QMfSZjoVt031WQA1dB/Fy/e1WNzDAFA1t22qf6F4oMK+cGGXAyle3g0AL9qmqvjSBmHx74ecbarVAYDkpDWR/1UlRB9i/SWJN3rfapvqo972c6hj8vGDFutyguJhq22qxypptqnaBKEREYs4EwC2B8o8GJ615gt5C+oVpzqeeesy3q18cCztsbBz3hBSW0yU4uWsY2lh7zY6EZJWnbNwLO0Vipdv9O8kOWmvP08D3rNNtfo7hOLloQbxfaby2TbV76Y+S+efoczli6m9zSzsklTa2mEzlJjkQH1aggmB5KQNALAOAP7tWNobCWkQALABANYAQNmxtDLqesdO2qMXHrnrmm1dk2NpX96dEbT66uhsbHDMGMlJqwL5D/j23x9SXk0sXtotTWK71vtyJQrqc24MnJx5s031rUZ5bFMtk5y0ydtc0axM21RfJDmp5tXkJCfttU31tQbH6LapvhO46Wm1b/+DIYeFxdJw9QTbVH9im+oHJCedCgmCzY0YkpNyITNv9XgtYj4AALBN9YckJ630dM63TfW5YB6Kl28LOe5YlAccYuD2zouoTyY7obIpVAJTB9tU5/3bFC/v8M8OUry81kvfVG9mL5CfDOze5ekcCeis9WYLH/WO2xaI66046kfx8oOB+Ko3yNmm+r0k2zYDAM90XAqmLUhOqnmzG8XLlzmWVjM54Vjacc+EkUZtx9LeDSStC95b7X1RjgeOO0bx8lWB+JI4L05tRjqzUBj/IDuhRp7axMTKR/0bjqV1fMsxyUlnBJJeB4CLAjr1vijBKf6WnneNyOYEygylcinwUQCYSksUU6XpeS3JSZttU62+tz5sUid4FSjAEQC4IEowJ097amb56CjHNcI21QcoHp6Ek17bZpvqj2JrvSb0AAAsFMZPZAHOLY/J+AVM6bIQIU/bBqN4ea9jaSdIToqiAyQnnRJIehOaP+AQ6cpNnfjOa3ZsJ1SvliwUxv+BX+GROjVXSUhO2hNXwRQvf9yxtF97mzX3dpOcVG+p6s/7NxxLmweAZpNIbS17TfHy7jbvDmwfWleuSHIiA0/i1BKSp8YsJCddHIyf5KS+kLSVIWURDXS2BnT2BPZ/2UtfHUi/znfM+sC+O730ewPp13h/V5KclMR5fEsG35xUB2Nz10JyUrbV+MPM7aVfENC7z7dvYys6/gmWFo5ZHTQ3yUnfQOXj0EmchcL4q95C8NegCmy54FhameLlD0fJS/Hy3iZlvUDxcqGybZvqIyQn7fL2vU7xcqQXC1C8vN6xtPd82yujxOZY2juo2jGMhjOUC4XxpzyTM9kJ9UsxafrfPfl226X8fxL648yxtKMUL5MUL98Ztp/iZYni5bW+c+h3oT4P1wia6gskJ/V4OrMUL6+kePmeOjrXUryccSztP4H4/kvxck+D+Lb5YgOo7de3ELQzAAD8DwXYiK9BjJP6AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIyLTExLTIyVDA0OjI5OjUzKzAwOjAw3h1NrAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMi0xMS0yMlQwNDoyOTo1MyswMDowMK9A9RAAAAAASUVORK5CYII=',
    sidebar=[pn.pane.JPG('logo.jpg', sizing_mode='scale_both'),
             pn.pane.Markdown("# RCCPL Mukutban"),
             pn.pane.Markdown("### This Web-based Dashboard shows plant's performance based on logsheet data from DCS  "),
             pn.pane.Markdown("### Settings"),month_slider,plant_selection],
    main=[pn.Row(pn.Column(yaxis_section4,params_line_plot1.panel(width=700), margin=(0,25)),pn.Column(yaxis_params,params_table.panel(width=500))),
            pn.Row(pn.Column(yaxis_params2,yaxis_section2,params_bar_plot.panel(width=300),margin=(0,25))),
          pn.Row(pn.Column(yaxis_section7,spc_plot1.panel(width=700),margin=(0,25)),pn.Column(yaxis_section6,spc_bar_plot.panel(width=300),margin=(0,35)))],
    accent_base_color="#0F6FA2",
    header_background="#0E4474",
)
template3.servable();
#template3.show()
