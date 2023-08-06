import numpy as np
import copy, os
from .GUI_ClassFun import *
from .CPU_Agents import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Panel_Output(QWidget):
    def __init__(self, img_raw, img_bin, map, anchors):
        '''
        '''
        super().__init__()
        self.field = Field(img_raw=img_raw, img_bin=img_bin, map=map, anchors=anchors)
        self.layout = QHBoxLayout()
        '''left side'''
        self.pn_left = QWidget()
        self.lo_left = QGridLayout()
        self.wg_img = Widget_Seg(field = self.field)
        self.bt_1 = QPushButton("RGB (J)")
        self.bt_2 = QPushButton("Binary (K)")
        '''right side'''
        self.pn_right = QWidget()
        self.lo_right = QGridLayout()
        self.wg_data = Widget_Data()
        self.lb_project = QLabel()
        self.fd_project = QLineEdit()
        self.lb_output = QLabel()
        self.fd_output = QLineEdit()
        self.bt_output = QPushButton()
        '''ui'''
        self.initUI()
    def initUI(self):
        # button
        self.bt_1.pressed.connect(self.wg_img.switch_raw)
        self.bt_1.released.connect(self.wg_img.switch_seg)
        self.bt_2.pressed.connect(self.wg_img.switch_bin)
        self.bt_2.released.connect(self.wg_img.switch_seg)
        # project
        font = self.fd_project.font()
        font.setPointSize(25)
        fm = QFontMetrics(font)
        self.fd_project.setFixedHeight(fm.height())
        self.fd_output.setFixedHeight(fm.height())
        self.lb_project.setText("Prefix")
        self.fd_project.setText("GRID")
        self.lb_output.setText("Output Path")
        self.fd_output.setText(os.path.expanduser("~"))
        self.bt_output.setText("Browse")
        self.bt_output.clicked.connect(self.assign_PathOut)
        '''layout'''
        # left
        self.lo_left.addWidget(self.wg_img, 0, 0, 1, 2)
        self.lo_left.addWidget(self.bt_1, 1, 0)
        self.lo_left.addWidget(self.bt_2, 1, 1)
        self.pn_left.setLayout(self.lo_left)
        # right
        self.lo_right.addWidget(self.wg_data, 0, 0, 1, 3)
        self.lo_right.addWidget(self.lb_project, 1, 0)
        self.lo_right.addWidget(self.fd_project, 1, 1)
        self.lo_right.addWidget(self.lb_output, 2, 0)
        self.lo_right.addWidget(self.fd_output, 2, 1)
        self.lo_right.addWidget(self.bt_output, 2, 2)
        self.pn_right.setLayout(self.lo_right)
        # policy
        policy_right = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy_right.setHorizontalStretch(1)
        self.pn_right.setSizePolicy(policy_right)
        policy_left = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy_left.setHorizontalStretch(2)
        self.pn_left.setSizePolicy(policy_left)
        # assemble
        self.layout.addWidget(self.pn_left)
        self.layout.addWidget(self.pn_right)
        self.setLayout(self.layout)
        self.show()
    def assign_PathOut(self):
        path = QFileDialog().getExistingDirectory(self, "", "", QFileDialog.ShowDirsOnly)
        self.fd_output.setText(path)
    def paint_grid(self, qimg):
        """
        """
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.red)
        painter = QPainter(qimg)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        for row in range(self.field.nrow):
            for col in range(self.field.ncol):
                agent = self.field.get_agent(row, col)
                rect = agent.get_rect()
                # pt_x, pt_y = agent.get_coordinate()
                # draw_cross(pt_x, pt_y, painter)
                painter.drawRect(rect)
        painter.end()
    def out_raw(self, path):
        """
        """
        img = self.wg_img.img_raw[:,:,:3].copy()
        self.wg_img.make_rgb_img(img)
        qimg = self.wg_img.qimg
        self.paint_grid(qimg)
        save_img(qimg, path+"_raw")
        self.wg_img.switch_seg()
    def out_seg(self, path):
        """
        """
        self.wg_img.make_rgb_img(self.wg_img.img_seg)
        qimg = self.wg_img.qimg
        self.paint_grid(qimg)
        save_img(qimg, path+"_seg")
        self.wg_img.switch_seg()
    def out_bin(self, path):
        """
        """
        self.wg_img.make_bin_img(self.wg_img.img_bin)
        qimg = self.wg_img.qimg
        self.paint_grid(qimg)
        save_img(qimg, path+"_kmean")
        self.wg_img.switch_seg()
    def output(self):
        """
        """
        path_out = self.fd_output.text()+"/"+self.fd_project.text()
        # figure
        self.out_raw(path=path_out)
        self.out_seg(path=path_out)
        self.out_bin(path=path_out)
        # dataframe
        df = self.field.get_DF()
        if self.wg_data.item1s[0][0].checkState()==Qt.Checked:
            idx = self.field.get_index(ch_1=3, ch_2=0, isContrast=True, name_index="NDVI")
            df = pd.merge(df, idx, on='var', how='left')
        if self.wg_data.item1s[1][0].checkState()==Qt.Checked:
            idx = self.field.get_index(ch_1=3, ch_2=1, isContrast=True, name_index="GNDVI")
            df = pd.merge(df, idx, on='var', how='left')
        if self.wg_data.item1s[2][0].checkState()==Qt.Checked:
            idx = self.field.get_index(ch_1=1, ch_2=0, isContrast=True, name_index="NDGI")
            df = pd.merge(df, idx, on='var', how='left')
        if self.wg_data.item1s[3][0].checkState()==Qt.Checked:
            idx = self.field.get_index(ch_1=3, ch_2=0, ch_3=1, isThree=True, name_index="CNDVI")
            df = pd.merge(df, idx, on='var', how='left')
        if self.wg_data.item1s[4][0].checkState()==Qt.Checked:
            idx = self.field.get_index(ch_1=3, ch_2=0, isRatio=True, name_index="RVI")
            df = pd.merge(df, idx, on='var', how='left')
        if self.wg_data.item1s[5][0].checkState()==Qt.Checked:
            idx = self.field.get_index(ch_1=3, ch_2=1, isRatio=True, name_index="GRVI")
            df = pd.merge(df, idx, on='var', how='left')
        df.to_csv(path_out+"_data.csv", index=False)


class Widget_Seg(Widget_Img):
    def __init__(self, field):
        '''
        '''
        super().__init__(field.img_raw)
        self.setMouseTracking(True)
        self.zoom = 1
        '''attr'''
        # basic
        self.field = field
        self.agents_reset = copy.deepcopy(self.field.agents)
        self.img_raw = field.img_raw
        self.img_bin = field.img_bin
        # painter
        self.is_fit_width = False
        self.pt_st_img = 0
        self.ratio = 0
        # mouse
        self.agent_click = None
        self.dir = None
        # ui
        self.initUI()
    def initUI(self):
        '''generate seg image'''
        img_temp = self.img_bin.reshape(self.img_bin.shape[0], self.img_bin.shape[1], 1)
        self.img_seg = np.multiply(self.img_raw[:,:,:3], img_temp).copy()
        self.img_seg[(self.img_seg.mean(axis=2)==0), :] = self.img_seg.max()
        self.switch_seg()
        self.show()
    def mousePressEvent(self, event):
        pos = event.pos()
        for row in range(self.field.nrow):
            for col in range(self.field.ncol):
                agent = self.field.get_agent(row, col)
                rect = agent.get_rect()
                if self.is_fit_width:
                    self.ratio = self.width()/self.qimg.width()
                    rec_agent = QRect(rect.x()*self.ratio, rect.y()*self.ratio+self.pt_st_img, rect.width()*self.ratio, rect.height()*self.ratio)
                else:
                    self.ratio = self.height()/self.qimg.height()
                    rec_agent = QRect(rect.x()*self.ratio+self.pt_st_img, rect.y()*self.ratio, rect.width()*self.ratio, rect.height()*self.ratio)
                if rec_agent.contains(pos):
                    bd_W = rec_agent.x()
                    bd_N = rec_agent.y()
                    bd_E = bd_W + rec_agent.width()
                    bd_S = bd_N + rec_agent.height()
                    dis_W = abs(pos.x()-bd_W)
                    dis_N = abs(pos.y()-bd_N)
                    dis_E = abs(pos.x()-bd_E)
                    dis_S = abs(pos.y()-bd_S)
                    print("W:%.2f, N:%.2f, E:%.2f, S:%.2f" %(dis_W, dis_N, dis_E, dis_S))
                    dir_idx = np.argmin(np.array([dis_N, dis_W, dis_S, dis_E]))
                    if dir_idx==0:
                        self.dir = Dir.NORTH
                    elif dir_idx==1:
                        self.dir = Dir.WEST
                    elif dir_idx==2:
                        self.dir = Dir.SOUTH
                    elif dir_idx==3:
                        self.dir = Dir.EAST
                    self.agent_click = agent
                    break
        # mag module
        if event.button() == Qt.RightButton:
            self.zoom = (self.zoom+1)%3
            self.mouseMoveEvent(event)
    def mouseMoveEvent(self, event):
        pos = event.pos()
        if event.buttons() == Qt.LeftButton:
            # adjust the border
            if self.is_fit_width:
                if self.dir==Dir.NORTH or self.dir==Dir.SOUTH:
                    value = (pos.y()-self.pt_st_img)/self.ratio
                elif self.dir==Dir.WEST or self.dir==Dir.EAST:
                    value = pos.x()/self.ratio
            else:
                if self.dir==Dir.NORTH or self.dir==Dir.SOUTH:
                    value = pos.y()/self.ratio
                elif self.dir==Dir.WEST or self.dir==Dir.EAST:
                    value = (pos.x()-self.pt_st_img)/self.ratio
            self.agent_click.set_border(self.dir, value)
        # mag module
        if self.zoom!=0:
            magnifying_glass(self, pos, area=300, zoom=self.zoom*4)
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
        self.repaint()
    def paintEvent(self, paint_event):
        painter = QPainter(self)
        super().paintImage(painter)
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        for row in range(self.field.nrow):
            for col in range(self.field.ncol):
                agent = self.field.get_agent(row, col)
                rect = agent.get_rect()
                pt_x, pt_y = agent.get_coordinate()
                if self.is_fit_width:
                    self.ratio = self.width()/self.qimg.width()
                    rec_agent = QRect(rect.x()*self.ratio, rect.y()*self.ratio+self.pt_st_img, rect.width()*self.ratio, rect.height()*self.ratio)
                    draw_cross(pt_x*self.ratio, pt_y*self.ratio+self.pt_st_img, painter)
                else:
                    self.ratio = self.height()/self.qimg.height()
                    rec_agent = QRect(rect.x()*self.ratio+self.pt_st_img, rect.y()*self.ratio, rect.width()*self.ratio, rect.height()*self.ratio)
                    draw_cross(pt_x*self.ratio+self.pt_st_img, pt_y*self.ratio, painter)
                painter.drawRect(rec_agent)
        painter.end()
    def switch_raw(self):
        img = self.img_raw[:,:,:3].copy()
        super().make_rgb_img(img)
        self.repaint()
    def switch_bin(self):
        super().make_bin_img(self.img_bin)
        self.repaint()
    def switch_seg(self):
        super().make_rgb_img(self.img_seg)
        self.repaint()
    def reset(self):
        self.field.agents = None
        self.field.agents = copy.deepcopy(self.agents_reset)
        self.repaint()


class Widget_Data(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QTreeView(self)
        self.model = QStandardItemModel()
        self.initUI()
    def initUI(self):
        self.model.setHorizontalHeaderLabels(['Output', 'Data'])
        self.rootItem = self.model.invisibleRootItem()
        self.buildTree()
        self.view.setModel(self.model)
        layout = QHBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.view.expandAll()
        self.show()
    def buildTree(self):
        item0 = [QStandardItem('Figures'), QStandardItem(' ')]
        self.item0s = []
        self.item0s.append([QStandardItem('Raw'), QStandardItem('Raw image')])
        self.item0s.append([QStandardItem('Segmentation'), QStandardItem('Extraction of area of interest (AOI)')])
        self.item0s.append([QStandardItem('K-mean'), QStandardItem('Visualization of K-mean results')])
        item1 = [QStandardItem('Data Frame'), QStandardItem(' ')]
        self.item1s = []
        self.item1s.append([QStandardItem('NDVI'), QStandardItem('(NIR-Red) / (NIR+Red)')])
        self.item1s.append([QStandardItem('GNDVI'), QStandardItem('(NIR-Green) / (NIR+Green)')])
        self.item1s.append([QStandardItem('NDGI'), QStandardItem('(Green-Red) / (Green+Red)')])
        self.item1s.append([QStandardItem('CNDVI'), QStandardItem('(2NIR-Red-Green) / (NIR+Red+Green)')])
        self.item1s.append([QStandardItem('RVI'), QStandardItem('NIR / Red')])
        self.item1s.append([QStandardItem('GRVI'), QStandardItem('NIR / Green')])
        for i in range(3):
            item0[0].appendRow(self.item0s[i])
            self.item0s[i][0].setCheckable(True)
            self.item0s[i][0].setCheckState(Qt.Checked)
        for i in range(6):
            item1[0].appendRow(self.item1s[i])
            # if (i==0) or (i==2):
            self.item1s[i][0].setCheckState(Qt.Checked)
            self.item1s[i][0].setCheckable(True)
        self.rootItem.appendRow(item0)
        self.rootItem.appendRow(item1)
