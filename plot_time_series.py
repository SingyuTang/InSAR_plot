'''
该文件用于读取gamma软件的vu_disp_2生成的点文件并绘制时序图。需设置以下值：
1.pointfolder:时序图所在的文件夹路径，该路径只能含gamma生成的点文件
2.time_series_title:生成的时序图自定义标题
3.savepath：生成的时序图的存储路径
4.xspace：绘制xtick时的日期间隔
5.plt_legend:为时序图的更改图例名称（该项可不设置）。默认图例名称为文件名名称
如要自己设置图例，则根据文件的排序自行拟定图例列表，具体样式可查看第19行，并在设置完成后，在121行中的主函数中将legendlist参数为plt_legend
'''
import numpy as np
import  matplotlib.pyplot  as plt
from datetime import date,datetime
import time
import os
pointfolder=r'.\point'
time_series_title='20181111-20201031北京地面沉降时序图'#标题
savepath=r'.\time_series.jpg'
global xspace; xspace=2#日期数据的间隔
# plt_legend=['p1304_1139','p1415_970','p1425_965']#图例
plt.rcParams['font.sans-serif']=['FangSong']#显示中文标签
plt.rcParams['axes.unicode_minus']=False
def get_filepathlist(folderpath):
    '''
    读取文件夹下的所有文件名并返回所有文件的文件路径
    :return:
    '''
    filepathlist = []
    filelist = os.listdir(folderpath)
    for file in filelist:
        path = os.path.join(folderpath, file)
        filepathlist.append(path)
    return filepathlist
def get_legendlist(folderpath):
    '''
    利用文件名为图例命名，获取文件名的主文件名
    :param folderpath:
    :return: 返回文件名列表，list类型
    '''
    filelist=get_filepathlist(folderpath)
    legendlist=[]
    for name in filelist:
        legend_tmp=os.path.basename(name).split('.')[0]
        legendlist.append(legend_tmp)
    return legendlist
def read_pointfile(filepath):
    '''
    读取时序点文件中的日期和形变值并返回
    :param filepath: 文件路径
    :return: 返回日期和形变数据组成的元组，（日期，形变）。形变（deform）为ndarray类型，里面的元素为float64类型；日期为一个列表，里面的元素为datetime类型
    '''
    data=np.genfromtxt(filepath,skip_header=9,delimiter='',dtype='U20')#dtype为浮点不能读取时间（字符串）
    # print(type(data),data)
    datearray,deform=data[...,1],data[...,4]
    deform=deform.astype('f8')#更改array数据类型为float64
    datelist=list(datearray)
    YMDlist=[]
    for tmp in datelist:
        YMDs=tmp[0:10]
        YMDt=datetime.strptime(YMDs,'%Y-%m-%d')
        YMDlist.append(YMDt)
    return YMDlist,deform
def awk_elementlist_equidistance(anylist:list,xspace=1):
    '''
    等间距取列表元素，返回一个列表
    :param anylist:
    :param step:
    :return:
    '''
    nn=len(anylist)
    index=0
    equidistance_list=[]
    while index<nn:
        equidistance_list.append(anylist[index])
        index=index+xspace
    return equidistance_list
def plot_time_series1(filepath):
    '''
    根据单个文件绘制单条曲线，不执行close函数，可在一个figure上连续绘制曲线
    :param filepath:
    :return:
    '''
    pointdata = read_pointfile(filepath)
    date1, deform = pointdata[0], pointdata[1]
    # print(len(date1),date1)
    # print(deform)
    awk_date=awk_elementlist_equidistance(date1,xspace)
    awk_deform=np.asarray(awk_elementlist_equidistance(list(deform),xspace))
    # print(awk_date)
    # print(awk_deform)
    plt.plot(date1,deform*100,linewidth=0.8)
    for x,y in zip(date1,deform):
        plt.plot(x,y*100,marker='.',markersize=1.5,color='r')
    awk_xtick_label=[]
    for tmp in awk_date:
        datestr = tmp.strftime("%Y/%m/%d")  # datetime格式转为str类型
        awk_xtick_label.append(datestr)
    plt.xticks(awk_date,awk_xtick_label,fontsize=14)
    plt.yticks(fontsize=14)
legendlist=get_legendlist(pointfolder)
def plot_time_series_multi(folderpath,title,legendlist=legendlist):
    '''
    批量绘制时序图
    :param folderpath:
    :param title:
    :return:
    '''
    filelist=get_filepathlist(folderpath)
    for name in filelist:
        print(name)
        plot_time_series1(name)
    plt.legend(legendlist,fontsize=15)
    plt.title(title,fontsize=18)
    plt.xlabel('日期', fontsize=15)
    plt.tick_params(direction='in')  # 设置主坐标轴刻度线朝向
    plt.tick_params(top=True, bottom=True, left=True, right=True)  # 在哪些轴显示刻度线
    plt.ylabel('形变量(cm)',fontsize=15)
    plt.savefig(savepath)
    print('时序图绘制完成。保存路径：{}'.format(savepath))
    plt.show()
    plt.close()
plot_time_series_multi(pointfolder,time_series_title)