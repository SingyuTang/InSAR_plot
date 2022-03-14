'''
本程序用于绘制时空基线图，默认为绘制bperp_file中的所有基线，无阈值限制。程序需设置以下值：
1.bperp_filepath：bperp_file文件的路径，该文件由gamma软件生成时无后缀，需更名为txt文件
2.bperb_pic_savepath:绘制时空基线图的存储路径
3.pic_title:时空基线图的标题
4.xtick_step:生成的基线图中日期的间隔数
5.filetype：bperp_file文件的类型，可选择ps和sbas，即是由什么脚本生成的bperp_file文件
'''



import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from datetime import datetime

bperp_filepath=r'C:\Users\tang xingyou\PycharmProjects\InSAR_plot\bperb_data\ps\bperp_file.txt'#bperp_file文件路径，需改名为txt文件
bperb_pic_savepath=r'.\ps_bj20_21.jpg'#生成的时空基线图保存路径
pic_title= '20201112-20211026时空基线分布图'#自定义标题
xtick_step=5#x轴刻度线两相邻的的影像日期间隔，值越大刻度线越稀
filetype='ps'#可选择sbas或者‘ps’

plt.rcParams['font.sans-serif']=['FangSong']#显示中文标签
plt.rcParams['axes.unicode_minus']=False
class bperb_file_sbas:
    '''
    绘制sbas中的bperp_file基线图
    '''
    num=[];date1=[];date2=[];bperp=[];deltaT=[];date1_ref=[];date2_ref=[];bperp1_ref=[];bperp2_ref=[]#解释如下
    datefilter_xy = []  #str
    xy_filterindex=[] #int
    def __init__(self,bperb_filepath:str,bperbpic_savepath:str,xtick_step:int):
        self.bperb_filepath=bperb_filepath
        self.savepath=bperbpic_savepath
        self.xtick_step=xtick_step
    def read_bperb_file(self):
        '''
        读取bperp_file中的数据并更新类成员数据
        :return:
        '''
        path=self.bperb_filepath
        with open(path) as f:
            line=f.readline()
            while line!='': #判断文件结尾
                # print(line,end='')#line中含有换行符，print里面也有换行符，这里去掉print里面的
                #行数据解释，第1列：编号；2①图初始时间；3②图终止时间；4空间基线长度；5时间基线长度；6①图距离主影像的时间；7②图距主影像的时间
                #8①图距主影像的空间基线长度；9②图距主影像空间基线长度。          注：计算空间基线和时间基线都用②图数据减①图数据
                listtmp=line.split()
                self.num.append(listtmp[0])
                self.date1.append(listtmp[1]);self.date2.append(listtmp[2])
                self.bperp.append(listtmp[3]);self.deltaT.append(listtmp[4])
                self.date1_ref.append(listtmp[5]);self.date2_ref.append(listtmp[6])
                self.bperp1_ref.append(listtmp[7]);self.bperp2_ref.append(listtmp[8])
                line=f.readline()
    def datetrans(self,datelist:list):
        '''
        将字符串格式的日期转化为date格式，返回YYYY-MM-DD格式的日期列表，分为str类型和date类型
        :param datelist:
        :return:strYMD:YYYY-MM-DD,str类型，dateYMD:date类型，datenun：数值类型
        '''
        strYMD=[];dateYMD=[]
        for x in datelist:
            Y=int(x[0:4]);M=int(x[4:6]);D=int(x[6:8])
            dt0=date(Y,M,D)
            dt1=date.isoformat(date(Y,M,D))
            strYMD.append(dt1)
            dateYMD.append(dt0)
        return strYMD,dateYMD
    def get_dateall_xy(self):
        '''
        筛选出不覆盖的影响日期并得出其x，y坐标和对应的影像日期，和更新影像编号(datefilter_xy)
        :return:
        '''

        dateall=self.date1+self.date2   #日期
        date_ref_all=self.date1_ref+self.date2_ref  #等价于x
        bperb_ref_all=self.bperp1_ref+self.bperp2_ref   #等价于y
        itab=range(len(bperb_ref_all))  #all index
        for i in itab:
            tmp =[]
            dateall_tmp=dateall[i]
            bperb_tmp=bperb_ref_all[i]
            dateref_tmp=date_ref_all[i]
            tmp.append(dateall_tmp);tmp.append(dateref_tmp);tmp.append(bperb_tmp)
            if tmp not in self.datefilter_xy:
                self.datefilter_xy.append(tmp)
        for i in range(len(self.datefilter_xy)):
            self.xy_filterindex.append(i)
    def awk_elementlist_equidistance(self,anylist:list):
        '''
        等间距取列表元素
        :param anylist:
        :param step:
        :return:
        '''
        nn=len(anylist)
        index=0
        equidistance_list=[]
        while index<nn:
            equidistance_list.append(anylist[index])
            index=index+self.xtick_step
        return equidistance_list
    def plot_point_bperp(self,strtitle:str):
        '''
        根据date1_ref（x1）、date2_ref（x2）、bperp1_ref（y1）、bperp2_ref（y2）绘制点（x，y），x代表影像对应的生成时间，y代表相对主影像的空间基线长度
        :return:
        '''
        X1=np.asarray(self.date1_ref,dtype='f4')
        X2=np.asarray(self.date2_ref,dtype='f4')
        Y1=np.asarray(self.bperp1_ref,dtype='f4')
        Y2=np.asarray(self.bperp2_ref,dtype='f4')
        self.xy_filterindex=[]#重置该数组
        self.get_dateall_xy()
        xtick1=list(np.array(self.datefilter_xy).T[0])#所有的xtick点
        pos_x1=list(np.array(self.datefilter_xy,dtype='f4').T[1])
        pos_y1=list(np.array(self.datefilter_xy,dtype='f4').T[2])
        pos_x2=self.awk_elementlist_equidistance(pos_x1)
        xtick2=self.awk_elementlist_equidistance(xtick1) #在xtick1中等距取点：2021XXXX
        date_filter=self.datetrans(xtick2)
        xtick3=date_filter[0]   #YYYY-MM-DD
        for tmp, index in zip(self.datefilter_xy, self.xy_filterindex):
            date1, x, y = tmp[0], float(tmp[1]), float(tmp[2])
            point_index = index
            fig=plt.plot(x,y,marker='o',mfc='#DAA520',mec='#000000',markersize=10)
            plt.text(x+0.5,y+0.5,point_index+1)
        for x1,y1,x2,y2 in zip(X1,Y1,X2,Y2):
            xpoints=np.array([x1,x2])
            ypoints=np.array([y1,y2])
            plt.plot(xpoints,ypoints,color='#191970',linestyle='-',linewidth=1.5,alpha=0.7)
        ax = plt.gca
        plt.xticks(pos_x2,xtick3)
        plt.title(strtitle,loc='center')
        plt.xlabel('日期',loc='center')
        plt.ylabel('垂直基线/m',loc='center')
        # plt.grid() #添加格网
        # plt.minorticks_on()#显示次刻度线
        # plt.tick_params(which='minor',direction='in')#设置次刻度线朝向，in，out，inout
        plt.tick_params(direction='in')  # 设置主坐标轴刻度线朝向
        plt.tick_params(top=True,bottom=True,left=True,right=True)#在哪些轴显示刻度线
        plt.savefig(self.savepath)
        print('sbas时空基线已绘制完成。')
        plt.show()
        plt.close()

class bperb_file_ps:
    '''
    绘制StaMPS中生成的时空基线图
    '''
    def __init__(self,bperb_filepath:str,bperbpic_savepath:str,xtick_step:int):
        self.bperb_filepath=bperb_filepath
        self.savepath=bperbpic_savepath
        self.xtick_step=xtick_step
    def get_xy(self):
        '''
        获取绘图所需要的x（第5列数据）和y（第4列数据）和日期（第3列数据）
        :return:
        '''
        self.data=np.loadtxt(self.bperb_filepath,dtype='f8')
        self.slavex=self.data[..., 4]
        self.slavey=self.data[..., 3]
        self.masterx=self.data[0,6]
        self.mastery=0
        self.master_date=self.data[0,1]
        self.slave_date=self.data[...,2]
        self.allx=list(self.slavex)
        self.ally=list(self.slavey)
        self.alldate=list(self.slave_date)
        insert_index=0
        for x in self.allx:
            if self.masterx<x:
                self.allx.insert(insert_index,self.masterx)
                self.ally.insert(insert_index,self.mastery)
                self.alldate.insert(insert_index,self.master_date)
                break
            insert_index=insert_index+1
        self.allx=np.asarray(self.allx)#将主影像和从影像数据合并
        self.ally=np.asarray(self.ally)
        self.alldate=np.asarray(self.alldate)
        print(self.alldate)
    def awk_elementlist_equidistance(self,anylist:list):
        '''
        等间距取列表元素
        :param anylist:
        :param step:
        :return:
        '''
        nn=len(anylist)
        index=0
        equidistance_list=[]
        while index<nn:
            equidistance_list.append(anylist[index])
            index=index+self.xtick_step
        return equidistance_list
    def plot_bperp_point(self,strtitle:str):
        plt.plot(self.masterx,self.mastery,marker='o',mfc='#DAA520',mec='#000000',markersize=8)
        plt.text(self.masterx+0.5,self.mastery+0.5,'1')
        point_num=2
        for x,y in zip(self.slavex,self.slavey):
            xpoint=np.array([self.masterx,x])
            ypoint=np.array([self.mastery,y])
            plt.plot(xpoint,ypoint,color='#191970',linestyle='-',linewidth=1.5,alpha=0.7)
            plt.plot(x,y,marker='o',mfc='#DAA520',mec='#000000',markersize=10)
            plt.text(x+0.5,y+0.5,point_num)
            point_num=point_num+1
        awk_slavedate=self.awk_elementlist_equidistance(self.alldate)
        awk_slavex=self.awk_elementlist_equidistance(self.allx)#xtick上的标签所对应的位置
        awk_slavedate_xtick=[]#在x轴上的标签，筛选后
        # print(len(awk_slavedate),awk_slavedate)
        # print(len(awk_slavex),awk_slavex)
        for tmp in awk_slavedate:#float类型的日期转为datetime类型
            ttmp=str(int(tmp))
            date1=datetime.strptime(ttmp,"%Y%m%d")#字符串转为datetime格式
            date2=date1.strftime("%Y/%m/%d")#datetime格式转为str类型
            awk_slavedate_xtick.append(date2)
        plt.xticks(awk_slavex,awk_slavedate_xtick)
        plt.title(strtitle, loc='center')
        plt.xlabel('日期', loc='center')
        plt.ylabel('垂直基线/m', loc='center')
        plt.tick_params(direction='in')  # 设置主坐标轴刻度线朝向
        plt.tick_params(top=True, bottom=True, left=True, right=True)  # 在哪些轴显示刻度线
        plt.savefig(self.savepath)
        print('ps时空基线已绘制完成。')
        plt.show()

def plot_bperp_sbas(bperb_filepath,bperb_pic_savepath,title,xtick_step):
    bp = bperb_file_sbas(bperb_filepath, bperb_pic_savepath,xtick_step)
    bp.read_bperb_file()
    bp.dateall = bp.date1 + bp.date2
    bp.bperb_ref_all = bp.bperp1_ref + bp.bperp2_ref
    bp.plot_point_bperp(title)

def plot_bperp_ps(bperb_sbasfile_path, bperb_pic_savepath, pic_title, xtick_step):
    ps = bperb_file_ps(bperb_sbasfile_path, bperb_pic_savepath, xtick_step)
    ps.get_xy()
    ps.plot_bperp_point(pic_title)

def plot_bperp_file(bperp_filepath,bperb_pic_savepath,filetype,xtick_step,pic_title):
    if filetype=='ps':
        plot_bperp_ps(bperp_filepath,bperb_pic_savepath,pic_title,xtick_step)
    elif filetype=='sbas':
        plot_bperp_sbas(bperp_filepath,bperb_pic_savepath,pic_title,xtick_step)

plot_bperp_file(bperp_filepath,bperb_pic_savepath,filetype,xtick_step,pic_title)

