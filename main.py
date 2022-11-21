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
params["Production MT"]=(params['Production'])/1000
params['Power MW']=(params['Power'])/1000
params['Month']=params['Date'].dt.month
params

yaxis_params = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=["Production MT", 'Run Hour','Power MW'],
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
options = ['Crusher', 'RM1', 'RM2', 'Kiln', 'Coal Mill']
params_pipeline1 = (iparams[(iparams.Section.isin(options))].groupby(['Section', 'Date'])[yaxis_params1]
                    .sum().to_frame().reset_index())

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
params_pipeline3 = (iparams[(iparams.Section.isin(options))].groupby(['Section', 'Month'])[
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
params_pipeline4 = (iparams[(iparams.Section.isin(options))].groupby(['Section','Date']).sum().reset_index())
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
params_spc['spc']=(params_spc['Power MW']/params_spc['Production MT'])
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
params_spc1['spc1']=(params_spc1['Power MW']/params_spc1['Production MT'])
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
    title='Production Dashboard',
    sidebar=[pn.pane.JPG('logo.jpg', sizing_mode='scale_both'),
             pn.pane.Markdown("# RCCPL Mukutban"),
             pn.pane.Markdown("### This Web-based Dashboard shows plant's performance based on logsheet data from DCS  "),
             ],
    main=[pn.Row(pn.Column(jpg, margin=(0,25)),pn.Column(pn.Spacer(background='#F7F7F7', width=200, height=100)),pn.Column(plant_selection),pn.Column(pn.Spacer(background='#F7F7F7', width=100, height=100)),pn.Column(month_slider)),
          pn.Row(pn.Column(yaxis_section4,params_line_plot1.panel(width=700), margin=(0,25)),pn.Column(yaxis_params,params_table.panel(width=500))),
            pn.Row(pn.Column(yaxis_params2,yaxis_section2,params_bar_plot.panel(width=300),margin=(0,25))),
          pn.Row(pn.Column(yaxis_section7,spc_plot1.panel(width=700),margin=(0,25)),pn.Column(yaxis_section6,spc_bar_plot.panel(width=300),margin=(0,35)))],
    accent_base_color="#0F6FA2",
    header_background="#0E4474",
)
template3.servable();
#template3.show()
