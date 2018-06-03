 /*  ------------------------------
    Copyright <2018> [Tim Hu]
    email: timtingwei@hotamail.com    
   ------------------------------
   File:spaceOrder.cpp
   Date:Wed May 16 15:49:38 CST 2018
   compile: g++ -std=c++11 spaceOrder.cpp -lGLEW -lGL -lGLU -lglfw3 -lX11 -lXxf86vm -lXrandr -lpthread -lXi -ldl -lXinerama -lXcursor
   -----------------------------
*/
// GLEW
#define GLEW_STATIC
#include <GL/glew.h>
// GLFW
#include <GLFW/glfw3.h>


#include <time.h>
#include <math.h>
#include <cassert>
#include <iostream>
#include <vector>
#include <initializer_list>
#include "circle.h"


// const double PI = 3.1415926f;

typedef int Rank;                   // 秩
#define DEAFAULT_CAPACITY 3         // 默认初始容量3



/*
struct Room {
v  double positionX = 0.0;
  double positionY = 0.0;
  double area;
};

struct Circle {
  double x, y, r;

  void moveCircle(const double angle, const double dist);
};


struct Circle_lst {
  Circle circles[50];
  int n = 0;
  Circle coverCircle;

  void appendCircle(Circle);
  void appendCircles(Circle_lst);
  void getCoverCircle();
  void moveCircles(double angle, double dist);
  Circle getFarthestCircle(const Circle P);

  void printCircles();
  void drawCircles(int childrenColor);
};

struct Circle_tree {
  Circle_lst clsts_arr[50];
  int n = 0;

  void appendClst(Circle_lst);

  void printTreeCircles();
};

class ParentCircle : public Circle {
 public:
  // 构造函数
  ParentCircle() = default;
  ParentCircle(double p_x, double p_y, double p_r) {
    x = p_x, y = p_y, r = p_r;
  }

  // 
 private:
  const int _resourceCount = 20;             // 等分成20份资源
  std::vector<int> _resourceOccupy_vec = {};     // 每个资源对应圆的索引列表
  Circle_lst _childrenClst;                  // 对应的所有的子空间
};

class ChildCircle : public Circle {
 public:
  // 构造函数
  ChildCircle() = default;
  ChildCircle(double p_x, double p_y, double p_r) {
    x = p_x, y = p_y, r = p_r;
  }

  ParentCircle parentCircle;     // 该子空间的父空间
  std::vector<int> rsrcIndex = {};     // 子空间占父空间的资源序列
};

class ChildrenCircle_lst : public Circle_lst {
 public:
  // ...
 private:
  // Circle_lst circles
  std::vector<std::vector<int> > _rsrcIndex_vec = {};
};
*/

double getRandData(int min, int max);
int celling(const double a, const double b);
int floor(const double a, const double b);
void getPosition(Circle room1, Circle& room2,
                 double angle, double dist);

void rotateCircle(Circle& room1, Circle room2,
                  double theta);

void surround(Circle circle, Circle_lst& clst,
              double* area_arr, int n,
              double direction, double dist);

double orientate(Circle room1, Circle& room2,
                 double direction_basic, double offset,
                 double dist);

int judgeCircleRelationship(double r1, double r2, double dist);

void orientate_surround_combine(
    Circle room1,
    Circle_lst& clst, double* area_arr, int n,
    double direction, double dist, double offset);


double getDistance(double* pos1, double* pos2);

double getDistance(Circle c1, Circle c2);

double getShareDegree(double* room1, double* room2);

double getRadian(double area, double dist);

double getRadian(Circle c1, Circle c2);

double getDirection(double* room1_pos, double* room2_pos);
double getDirection(Circle c1, Circle c2);


// vector是否为从小到大顺序
bool is_sortedVec(std::vector<int> i_vec);
// 对vec冒泡排序
void sortedVec(std::vector<int>& i_vec);
// 从vec1中减去vec2
void removeVec(std::vector<int> vec1, std::vector<int> vec2, std::vector<int>& vec3);
// vector中重复元素只保留一个
void setVector(std::vector<int> vec, std::vector<int>& vec_union);
// 将双重vec拍平成普通vec
void flattenDoubleVec(std::vector<std::vector<int>> doubleVec,
                      std::vector<int>& resultVec);
void printVector(std::vector<int> vec);

bool is_unboard(Circle c, Circle c1, Circle c2);
void reviseUnboard(Circle c, Circle c1, Circle& c2);   // 三者若遮挡修改c2位置
void collide(Circle c1, Circle c2, Circle& c2_new);
void getUnboardRooms(Circle c1, Circle_lst& unboardRooms, const int room_count);

void collide_cluster(Circle_lst clst1, Circle_lst& clst2);

void angleResourceArrange(std::vector<std::vector<int> >& i_vec,
                          Circle parentCircle,
                          Circle_lst& childCircles,
                          double* area_arr, double* dist_arr, int arr_n);

void searchAngleResource(std::vector<std::vector<int>>& restIndex_vec,
                         int resourceCount,
                         std::vector<int > usedAngleIndex_vec);




// 得到c2对于c1所占用的资源
void getResourceIndex(Circle c1,Circle c2, std::vector<int>& resourceIndex_vec);

// 判断资源区间是否有重复
int getGapResourceIndex(std::vector<int> ivec1,
                         std::vector<std::vector<int>> ivec2,
                        std::vector<int>& gapIndex_vec);

// 父空间之间检测遮挡并修改P2占用角度资源
void reviseParentUnboard(Circle P1, Circle_lst C1,
                         Circle& P2, Circle_lst& C2,
                         std::vector<std::vector<int> >& i_vec1);

// 父空间与子空间之间, 检测遮挡并修改C2_i占用角度资源
void reviseChildUnboard(Circle P1, Circle_lst C1,
                        Circle P2, Circle& C2_i, int index,
                        std::vector<std::vector<int> > i_vec1,
                        std::vector<std::vector<int> >& i_vec2,
                        bool& mobility);


// 通过资源区间来获得角度
double getAngleFromResourceIndex(Circle c1,
                                 Circle c2,
                                 Circle c,
                                 std::vector<int> c1_vec,
                                 std::vector<int> c2_vec,
                                 const double unitRadian);
void angleResourceDynamicWeight(Circle& P1, Circle& P2,
                                Circle_lst& C1, Circle_lst& C2,
                                std::vector<std::vector<int>> i_vec1,
                                std::vector<std::vector<int>>& i_vec2,
                                std::vector<Circle>& P2_vec,
                                std::vector<std::vector<std::vector<int>>>& i_vec2_resultWeight);

void getWorkableResourceIndexArrangement(
    std::vector<std::vector<std::vector<int> > > setVec,
    std::vector<std::vector<std::vector<int> > >& workableResouceIndex_3vec);
void getWorkableResourceIndexArrangementForParent(
    ParentCircle& P1, ParentCircle& P2,
    ChildCircle& C,
    std::vector<std::vector<int> >& workableResouceIndex_2vec);


void test_surround(Circle_lst& clst);
void test_shareDegree(Circle_lst &clst);
void test_orientate(Circle_lst &clst);
void test_orientate_surround_combine(Circle_lst &clst);
void test_coverDegree(Circle_lst& clst);
void test_unboard(Circle_lst& clst);
void test_align(Circle_lst& clst);
void test_align_surround(Circle_lst& clst);
void test_collide(Circle_lst& clst);
void test_moveCircles(Circle_lst& clst);
void test_clusterConnection(Circle_tree& ctre);
void test_angleResourceArrange(Circle_tree& ctre);
void test_newObject(Circle_tree& ctre);
void test_getWorkableResourceIndexArrangement(Circle_tree& ctre);
void test_getWorkableResourceIndexArrangementForParent(Circle_tree& ctre);

void drawPoint();
void drawLine();
void drawCircle(double x, double y, double radius, int color);
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
int main_draw(Circle_tree ctre);


double getDistance(double* pos1, double* pos2) {
  // 两点距离
  double dist = sqrt(pow((pos1[0] - pos2[0]), 2) +
                    (pow((pos1[1] - pos2[1]), 2)));
  return dist;
}

double getDistance(Circle c1, Circle c2) {
  double dist = sqrt(pow((c1.x - c2.x), 2) +
                    (pow((c1.y - c2.y), 2)));
  return dist;
}

void getPosition(Circle room1, Circle& room2,
                 double angle, double dist) {
  /* 通过已经确定的空间, 与x轴逆时针角度, 距离, 确定下一个空间的位置 */
  room2.x = room1.x + cos(angle) * dist;
  room2.y = room1.y + sin(angle) * dist;
}

int judgeCircleRelationship(double r1, double r2, double dist) {
  double R, r;
  if (r1 > r2) { R = r1, r = r2;
  } else {R = r2, r = r1;}

  if (dist == 0) {
    return 0;                                 // 同心圆
  } else if ((0 < dist)&&(dist < R-r)) {
    return 1;                                 // 不相交, 内离
  } else if (dist == R-r) {
    return 2;                                 // 内切
  } else if (dist == R+r) {
    return 3;                                 // 外切
  } else if ((R-r < dist)&&(dist < R+r)) {
    return 4;                                 // 相交于两点
  } else if (dist > R+r) {
    return 5;                                 // 不相交
  }
}


void appendCircles(Circle_lst& clst, Circle_lst clst_new) {
  for (int i = 0; i < clst_new.n; i++) {
    clst.circles[clst.n + i] = clst_new.circles[i];    // 逐个添加圆
    std::cout << "clst.n + i = " << clst.n + i << std::endl;
  }
  clst.n += clst_new.n;               // 储存圆数量改变
}


// 空间环绕算法
// =====================
void surround(Circle circle, Circle_lst& clst,
              double* area_arr, int n,
              double direction, double dist) {
  // 围绕某一确定空间布置剩余空间, 要求环绕的空间与确定空间的距离dist相同,
  // 且这些环绕空间互相不碰撞, 已知这些空间的面积area,
  const int size = 50;              // 数组的规模量
  // 判断初始距离能否放下已知面积的空间
  double angle_sum = 0;
  double beta, alpha;
  for (int i = 0; i < n; i++) {
    alpha = atan(sqrt(area_arr[i]/PI) / dist);
    beta = 2 * alpha;
    angle_sum += beta;
  }
  // 不能放下, 计算并更新出最小的dist值,
  if (angle_sum > 2*PI) {
    std::cout << "angle_sum > 2*PI" << std::endl;
    // 角度的总和大于给出方向区间, 代表当前距离无法放下, 计算最小距离并更新
  }
  // 可以放下
  // 每个环绕的圆相切, 将面积转换成弧度, 确定每个圆心对应的弧度
  double alpha_arr[size] = {};
  for (int i = 0; i < n; i++) {
    alpha = atan(sqrt(area_arr[i]/PI) / dist);   // 基准方向
    alpha_arr[i] = alpha;
  }
  // 转换成对应弧度的列表
  double angle_arr[size] = {};

  angle_arr[0] = direction + alpha_arr[0];   // 第一个圆对应的弧度为direction

  for (int i = 1; i < n; i++) {
    double angle_i = angle_arr[i-1] + alpha_arr[i-1] + alpha_arr[i];
    angle_arr[i] = angle_i;
  }

  for (int i = 0; i < n; i++) {
    Circle c_new;
    double r = sqrt(area_arr[i]/PI);
    c_new.r = r;
    double angle = angle_arr[i];
    // 得到环绕圆的坐标
    getPosition(circle, c_new, angle, dist);
    // 将生成圆的信息储存起来
    clst.appendCircle(c_new);
  }
}

// 影响度算法 由方向和切线扇形遮挡程度
// ===================================
double getDirection(double* room1_pos, double* room2_pos) {
  // 得到两个房间相对的方向
  double alpha = atan((room2_pos[1]-room1_pos[1])/(room2_pos[0]-room1_pos[0]));
  return alpha;
}

double getDirection(Circle c1, Circle c2) {
  // c2相对于c1的角度
  double delta_x = c2.x - c1.x;
  double delta_y = c2.y - c1.y;
  double alpha = atan(delta_y/delta_x);
  if ((delta_x > 0) && (delta_y > 0)) { return alpha;    // 第一象限
  } else if ((delta_x < 0) && (delta_y > 0)) { return PI+alpha;   // 2
  } else if ((delta_x < 0) && (delta_y < 0)) { return alpha + PI;   // 3
  } else if ((delta_x > 0) && (delta_y < 0)) {return 2*PI+alpha;
  }
}

double getCoverDegree(double* room1_pos, double* room2_pos, double r2) {
  // 得到room2对room1从扇形方向角度考虑的影响程度
  double dist = sqrt((room2_pos[0]-room1_pos[0])*(room2_pos[0]-room1_pos[0])
                    + (room2_pos[1]-room1_pos[1])*(room2_pos[1]-room1_pos[1]));
  // std::cout << "dist = " << dist << std::endl;
  if (r2 < dist) {
    double beta = 2*asin(r2/dist);
    // std::cout << "beta = " << beta << std::endl;
    double degree = beta/(2*PI);
    return degree;
  } else {
    std::cerr << "error!!! distance smaller than r2 " << std::endl;
  }
}

// 空间朝向算法
// =====================
double orientate(Circle room1, Circle& room2,
                 double direction_basic, double offset,
                 double dist) {
  // 通过某一空间, 在direction_basic的偏移值内布置另一空间
  srand((unsigned)time(NULL));
  double r = ((double)(rand()%10)) / 10;
  // std::cout << "r = " << r << std::endl;
  double angle = direction_basic-offset + 2*offset*r;
  // std::cout << "angle = " << angle << std::endl;
  getPosition(room1, room2, angle, dist);
  room2.r = 150;                  // 半径
  /*
  std::cout << "room2.x = " << room2.x << '\n'
            << "room2.y = " << room2.y << '\n'
            << "room2.r = " << room2.r << std::endl;
  */
  return angle;                   // 返回当前方向的弧度
}

// 空间共享度算法
double getShareDegree(Circle room1, Circle room2) {
  // 通过两个确定房间, 计算空间共享程度

  // 得到圆心distance
  double pos1[2] ={room1.x, room1.y};
  double pos2[2] ={room2.x, room2.y};
  double dist = getDistance(pos1, pos2);

  // 判断两个圆之间的关系
  // 0, 1, 2 最小圆面积
  // 3, 5, 共享面积0
  // 4,    部分重合
  int t = judgeCircleRelationship(room1.r, room2.r, dist);
  std::cout << "t = " << t << std::endl;
  double area_share;
  double area_room1 = PI*room1.r*room1.r, area_room2 = PI*room2.r*room2.r;
  if ((t == 0) || (t == 1) || (t == 2)) {
    // 最小圆面积
    if (room1.r < room2.r) {       // 比较半径
      area_share = area_room1;
    } else {area_share = area_room2;}

  } else if ((t == 3) || (t == 5)) {
    area_share = 0;
  } else if (t == 4) {
    // 部分重合
    // 计算共享面积所占夹角theta
    double height = room1.r - (room2.r + room1.r - dist)/2;
    double theta = acos(height / room1.r);
    // 计算共享圆锥面积
    // 声明扇形, 三角形, 圆锥面积
    double area_sector, area_triangle;
    area_sector = room1.r * room1.r * theta;
    area_triangle = room1.r * sin(theta) * height;
    area_share = 2 * (area_sector - area_triangle);
  }

  double degree1, degree2;
  degree1 = area_share / area_room1;
  degree2 = area_share / area_room2;
  std::cout << "area_share = " << area_share
            << "\ndegree1 = " << degree1
            << "\ndegree2 = " << degree2 << std::endl;
  /*
  std::cout << "room1_r = " << room1[2] << " room2_r = " << room2[2]
            << "\narea_sector = " << area_sector
            << "\narea_triangle = " << area_triangle
            << "\narea_share = " << area_share
            << "\ndistance = " << dist
            << "\nheight = " << height
            << "\ntheta = "  << theta
            << "\ndegree1 = " << degree1
            << "\ndegree2 = " << degree2 << std::endl;
  */

  return degree1;
}


// 关联排序和关联方向的组合
void orientate_surround_combine(
    Circle room1,
    Circle_lst& clst, double* area_arr, int n,
    double direction, double dist, double offset) {

  Circle room2;
  double orient_direc = orientate(room1, room2, direction, offset, dist);
  
  double direction_basic = orient_direc+getRadian(room2.r*room2.r*PI, dist)/2;

  // 弧度转换存在精度问题
  Circle_lst clst_new;
  surround(room1, clst_new, area_arr, n, direction_basic, dist);
  
  clst.appendCircle(room2);      // ERROR: 两个append存在点问题
  clst.appendCircles(clst_new);
}

double getRadian(double area, double dist) {
  // 获得圆a相对于另外圆b切线对应的弧度, 输入a面积area和圆心距离dist
  double radian = 2 * atan(sqrt(area/PI)/dist);
  return radian;
}

double getRadian(Circle c1, Circle c2) {
  // 重载输入两个圆c2对于c1所占的弧度
  double pos1[2] = {c1.x, c1.y};
  double pos2[2] = {c2.x, c2.y};
  double dist = getDistance(pos1, pos2);
  double area = pow(c2.r, 2)*PI;
  return 2 * atan(sqrt(area/PI)/dist);
}



void Circle_lst::appendCircle(Circle c_new) {
  circles[n] = c_new;
  ++n;                                       // 圆的总数量增加1
}

void Circle_lst::appendCircles(Circle_lst clst_new) {
  for (int i = 0; i < clst_new.n; i++) {
    circles[n + i] = clst_new.circles[i];    // 逐个添加圆
  }
  n += clst_new.n;                           // 储存圆数量改变
}

bool is_unboard(Circle c, Circle c1, Circle c2) {
  // 测试是否存在遮挡                   // 写入对象的方法中
  double c_pos[2] = {c.x, c.y};
  double c1_pos[2] = {c1.x, c1.y}, c2_pos[2] = {c2.x, c2.y};
  double d1 = getDistance(c, c1), d2 = getDistance(c, c2);
  if (d1 > d2) {            // c2 在 c1和c中间
    Circle c3 = c1;
    c1 = c2, c2 = c3;       // c1与c2交换位置, 使得并用一个算法
  }
  double alpha1 = getDirection(c, c1);
  double alpha2 = getDirection(c, c2);
  double theta1 = getRadian(c, c1)/2;
  double theta2 = getRadian(c, c2)/2;
  // if (d1 <= d2) {   // 外, c2 不会遮挡 c1, 确保c1 不遮挡 c2
  bool result = (alpha2 <= alpha1 + theta1) && (alpha2 >= alpha1 - theta1);
  // std::cout << "alpha1_angle = " << alpha1*180/PI << '\n'
  //           << "alpha2_angle = " << alpha2*180/PI << '\n'
  //           << "(alpha2 <= alpha1 + theta1) = "
  //           << (alpha2 <= alpha1 + theta1) << '\n'
  //           << "(alpha2 >= alpha1 - theta1) = "
  //           << (alpha2 >= alpha1 - theta1) << std::endl;
  return result;
}

void reviseUnboard(Circle c, Circle c1, Circle& c2) {
  // 遮挡问题处理, 前提是存在遮挡
  // c, c1确定, 修改所已经生成的c2, 得到c2不对c1产生遮挡(相对于c)
  double dist1 = getDistance(c, c1), dist2 =  getDistance(c, c2);
  double alpha1 = getDirection(c, c1);    // c1相对于c的角度
  double alpha2 = getDirection(c, c2);
  double alpha2_right, alpha2_left;       // alpha满足条件的极值
  // std::cout << "alpha1 = " << alpha1 * (180/PI)
  //           << " alpha2 = " << alpha2 * (180/PI) << std::endl;
  if (dist1 <= dist2) {    // 对于c, c1挡住c2, c2在外
    double theta1 = asin(c1.r/dist1);
    alpha2_right = alpha1 + theta1;   // 计算在外的两个区间极值
    alpha2_left = alpha1 - theta1;
    // 取区间中点, 判断在中点的哪个方向
    alpha2 = (alpha2 >= (alpha2_right + alpha2_left)/2)
        ? (alpha2_right):(alpha2_left);
    /*
    std::cout << "(alpha2_right + alpha2_left)/2 = "
              << (alpha2_right + alpha2_left)/2 *(180/PI) << '\n'
              << "alpha2_right = " << alpha2_right * (180/PI) << '\n'
              << "alpha2_left = " << alpha2_left * (180/PI) << '\n'
              << "alpha2 = " << alpha2 * (180/PI) << std::endl;
    */
  } else {                 // 对于c, c2挡住c1, c1在内
    double theta2 = asin(c2.r/dist2);
    alpha2_right = alpha1 + theta2;
    alpha2_left = alpha1 - theta2;
    alpha2 = (alpha2 >= (alpha2_right + alpha2_left)/2)
             ? (alpha2_right):(alpha2_left);
    /*
    std::cout << "(alpha2_right + alpha2_left)/2 = "
              << (alpha2_right + alpha2_left)/2 *(180/PI) << '\n'
              << "alpha2_right = " << alpha2_right * (180/PI) << '\n'
              << "alpha2_left = " << alpha2_left * (180/PI) << '\n'
              << "alpha2 = " << alpha2 * (180/PI) << std::endl;
    */
  }

  double delta_alpha = alpha2 - getDirection(c, c2);
  // c2以c为圆心, 旋转delta_alpha
  rotateCircle(c2, c, delta_alpha);
}

void align(Circle circle, Circle_lst& clst,
           double* area_arr, int n,
           double direction, double dist) {
  // 以空间circle为基准, 从距离dist处开始向direction方向依次排列n个circles
  Circle_lst clst_new;
  double r_arr[50] = {};
  double dist_arr[50] = {};
  for (int i = 0; i < n; i++) {
    r_arr[i] = sqrt(area_arr[i]/(2*PI));
  }
  // dist_arr[0] = circle.r + r_arr[0] + dist;     // 初始圆的圆心距离
  dist_arr[0] = dist;

  for (int i = 1; i < n; i++) {
    Circle ci;
    double dist_ci = dist_arr[i-1] + r_arr[i-1] + r_arr[i];
    dist_arr[i] = dist_ci;
    std::cout << "dist_ci = " << dist_ci << std::endl;
  }

  for (int i = 0; i < n; i++) {
    Circle ci;
    double dist_ci = dist_arr[i];
    getPosition(circle, ci, direction, dist_ci);
    ci.r = r_arr[i];
    clst_new.appendCircle(ci);
  }

  clst.appendCircles(clst_new);
}



void rotateCircle(Circle& room1, Circle room2,
                  double theta) {
  // room1 绕着 room2的中心点, 旋转theta
  room1.x = (room1.x - room2.x) * cos(theta) -
      (room1.y - room2.y) * sin(theta) + room2.x;
  room1.y = (room1.x - room2.x) * sin(theta) +
      (room1.y - room2.y) * cos(theta) + room2.y;
  // room1.r = room1.r;           // 旋转后半径与旋转前相同
}

double getRandData(int min, int max) {
  // srand((unsigned)time(NULL));
  double m1 = (double)(rand()%101)/101;    // 计算 0，1之间的随机小数,得到的值域近似为(0,1)
  min++;                // 将区间变为(min+1,max),
  double m2 = (double)((rand()%(max-min+1))+min);    // 计算 min+1,max 之间的随机整数，得到的值域为[min+1,max]
  m2 = m2-1;             // 令值域为[min,max-1]
  return m1+m2;          // 返回值域为(min,max),为所求随机浮点数
}

void collide(Circle c1, Circle c2, Circle& c2_new) {
  // 检测碰撞并得到新的c2
  int relationship = judgeCircleRelationship(c1.r, c2.r, getDistance(c1, c2));
  // std::cout << "relationship = " << relationship << std::endl;
  if (relationship == 4) {         // 相交才存在碰撞
    double alpha = getDirection(c1, c2);
    double move_dist = c1.r + c2.r;
    // 沿着原来的方向alpha, 距离c1圆心距离move_dist
    getPosition(c1, c2_new, alpha, move_dist);
    c2_new.r = c2.r;
  }
}

void collide_cluster(Circle_lst clst1, Circle_lst& clst2) {
  // 检测碰撞并得到新的c2
  Circle c1 = clst1.coverCircle, c2 = clst2.coverCircle;
  int relationship = judgeCircleRelationship(
      c1.r, c2.r, getDistance(c1, c2));
  // std::cout << "relationship = " << relationship << std::endl;
  if ((relationship == 0)
      || (relationship == 1)
      || (relationship == 2)
      || (relationship == 4)) {         //   //  0同心圆 1不相交内离 2内切 4相交
    double alpha = getDirection(c1, c2);
    // std::cout << "alpha = " << alpha*(180/PI) << std::endl;
    double move_dist = c1.r + c2.r - getDistance(c1, c2);
    // 沿着原来的方向alpha, 距离c1圆心距离move_dist
    clst2.moveCircles(alpha, move_dist);
  }
}

void Circle_lst::getCoverCircle() {
  double right = 0, left = 0, up = 0, down = 0;
  for (int i = 0; i < n; i++) {
    if ((circles[i].x + circles[i].r) > right)
      right = circles[i].x + circles[i].r;
    if ((circles[i].x - circles[i].r) < left)
      left = circles[i].x - circles[i].r;
    if ((circles[i].y + circles[i].r) > up)
      up = circles[i].y + circles[i].r;
    if ((circles[i].y - circles[i].r) < down)
      down = circles[i].y - circles[i].r;
  }

  coverCircle.x = (left + right)/2;
  coverCircle.y = (up + down)/2;
  coverCircle.r = sqrt(pow((right - left), 2) + pow((up - down), 2)) / 2;
  /*
  std::cout << "right = " << right << ','
            << "left = " << left << ','
            << "up = " << up << ','
            << "down = " << down << '\n'
            << "coverCircle.x" << coverCircle.x << ", "
            << "coverCircle.y" << coverCircle.y << ", "
            << "coverCircle.r" << coverCircle.r << std::endl;
  */
}

void Circle_lst::moveCircles(double angle, double dist) {
  // 群落整体移动
  Circle new_coverCircle;
  new_coverCircle.r =  coverCircle.r;
  getPosition(coverCircle, new_coverCircle, angle, dist);
  coverCircle = new_coverCircle;             // 用移动好的圆替换

  for (int i = 0; i < n; i++) {
    Circle ci = circles[i];
    Circle new_ci;
    new_ci.r = ci.r;
    getPosition(ci, new_ci, angle, dist);
    circles[i] = new_ci;
  }
}

void Circle_lst::printCircles() {
  for (int i = 0; i < n; i++) {
    std::cout << i << ".x = " << circles[i].x << ", "
              << i << ".y = " << circles[i].y << ", "
              << i << ".r = " << circles[i].r << std::endl;
  }
}

Circle Circle_lst::getFarthestCircle(const Circle P) {
  // 得到距离最远的圆
  double dist = getDistance(circles[0], P);
  Circle farthestCircle = circles[0];
  for (int i = 1; i < n; i++) {
    double dist_i = getDistance(circles[i], P);
    if (dist_i > dist) {
      // 存在比当前dist对应圆 更远的距离的圆
      farthestCircle = circles[i];
      dist = dist_i;
    }
  }
  return farthestCircle;
}
void Circle_lst::drawCircles(int childrenColor) {
  // 自定义UI
  // 让clst的首个圆green显示
  const int GREEN = 0;
  const int RED = 1;
  const int YELLOW = 2;
  
  int color = GREEN;
  drawCircle(circles[0].x, circles[0].y, circles[0].r, color);
  for (int i = 1; i < n; i++) {
    color = childrenColor;
    drawCircle(circles[i].x, circles[i].y, circles[i].r, color);
  }
}

void Circle_tree::appendClst(Circle_lst clst) {
  clsts_arr[n] = clst;
  ++n;                                       // 圆的总数量增加1
}

void Circle_tree::printTreeCircles() {
  std::cout << "====== print circles in tree =======" << std::endl;
  for (int i = 0; i < n; i++) {
    std::cout << "clst[" << i << "] :" << std::endl;
    clsts_arr[i].printCircles();             // 打印i聚落圆信息
  }
}

void getUnboardRooms(Circle c, Circle_lst& unboardRooms, const int room_count) {
  // 生成并修改多个互不遮挡的空间
  // 生成数据
  Circle c0;
  c0.x = getRandData(-1000, 1000), c0.y = getRandData(-1000, 1000);
  c0.r = getRandData(100, 300);
  unboardRooms.appendCircle(c0);
  // std::cout << "0, " << c0.x << ", "
  //           << "1, " << c0.y << ", "
  //           << "2, " << c0.r << std::endl;
  for (int i = 1; i < room_count; i++) {
    // std::cout << "i = " << i << std::endl;
    Circle ci;
    // srand((unsigned)time(NULL));
    ci.x = getRandData(-1000, 1000), ci.y = getRandData(-1000, 1000);
    ci.r = getRandData(100, 300);
    bool result = false;
    int j = 0;
    Circle ci_new;
    while ((j < unboardRooms.n) || (result == true)) {
      result = is_unboard(c, unboardRooms.circles[j], ci);
      // std::cout << "j = " << j << ", result = " << result << std::endl;
      if (result) {            // 如果ci与已经生成的圆产生遮挡
        // 修改ci产生新的满足条件的圆
        reviseUnboard(c, unboardRooms.circles[j], ci);
        // ci = ci_new;           // 新的圆替换旧的圆
        result = false;        // ci与cj,c之间无遮挡
        j = 0;                 // 从头开始检测
      } else {++j;}
    }   // 退出while循环
    /*
    std::cout << "i = " << i
              << ", ci.x = " << ci.x
              << ", ci.y = " << ci.y
              << ", ci.r = " << ci.r << std::endl;
    */
    unboardRooms.appendCircle(ci);
    // 打印ci信息
    // std::cout << "======= print ci information =====" << std::endl;
    // std::cout << i << ", "
    //           << unboardRooms.circles[i].x << ", "
    //           << unboardRooms.circles[i].y << ", "
    //           << unboardRooms.circles[i].r << std::endl;
  }
}

void getUnboardRooms(Circle c, Circle_lst& unboardRooms, Circle_lst& restRooms) {
  // 根据聚落中已经有的空间unboardRooms, 修改剩余空间restrooms, 生成不遮挡的空间
  // ..
  for (int i = 0; i < restRooms.n; i++) {
    bool result = false;
    int j = 0;
    while ((j < unboardRooms.n) || (result == true)) {
      result = is_unboard(c, unboardRooms.circles[j],
                          restRooms.circles[i]);
      if (result) {            // 如果ci与已经生成的圆产生遮挡
        // 修改ci产生新的满足条件的圆
        reviseUnboard(c, unboardRooms.circles[j],
                          restRooms.circles[i]);
        result = false;        // ci与cj,c之间无遮挡
        j = 0;                 // 从头开始检测
      } else {++j;}
    }     // 退出循环, 当前restRoom无遮挡
    unboardRooms.appendCircle(restRooms.circles[i]);
  }
}


void angleResourceArrange(std::vector<std::vector<int> >& i_vec,
                          Circle parentCircle,
                          Circle_lst& childCircles,
                          double* area_arr, double* dist_arr, int arr_n) {
  // 对c各个角度资源进行分配
  // 计算单位角度资源
  int resourceCount = 20;
  const double unitRadian = 2*PI/resourceCount;
  // 得到各个圆所对应的资源序号
  int countSum = 0;
  int resource_index = 0;
  std::vector<double> radian_vec = {};
  for (int i = 0; i < arr_n; i++) {
    double radian = getRadian(area_arr[i], dist_arr[i]);
    radian_vec.push_back(radian);   // 用于之后求得对应圆心角度
    // 当前圆所占资源数量
    int resource_count_i = celling(radian, unitRadian);
    // std::cout << "resource_count_i = " << resource_count_i << std::endl;
    countSum += resource_count_i;
    if (countSum > resourceCount) {  // 分配资源溢出
      // ..
      std::cout << "ERROR::resource overflow!!!" << std::endl;
    } else {
      // resource_count_i_arr[i] = resource_count_i;
      // 依次紧密排列
      std::vector<int> tmp_vec =  {};
      for (int index = 0; index < resource_count_i; index++) {
        tmp_vec.push_back(resource_index++);
      }
      // 添加入存放资源序号数组的数组
      i_vec.push_back(tmp_vec);
    }
  }

  // 检测
  std::cout << "==== print i_vec ================ " << "\n";
  for (int i = 0; i < i_vec.size(); i++) {
    for (int j = 0; j < i_vec[i].size(); j++) {
      std::cout << i_vec[i][j] << ", ";
    }
    std::cout << "\n";
  }
  std::cout << "================================= " << std::endl;


  // 得到每个资源序号对应的初始角度
  double firstAngle_arr[50] = {};
  for (int i = 0; i < resourceCount; i++) {
    firstAngle_arr[i] = i * unitRadian;
  }

  // 根据所占资源序号得到子空间
  std::cout << "========= print circle kernel point angle ======" << std::endl;
  for (int i = 0; i < arr_n; i++) {
    Circle childCircle;
    // 得到圆心对应角度
    double angle = i_vec[i][0] * unitRadian + radian_vec[i] / 2;
    std::cout << i << " ,angle = " << angle
              << ",  i_vec[i][0] = "
              << i_vec[i][0]  << std::endl;
    getPosition(parentCircle, childCircle, angle, dist_arr[i]);
    // 得到对应半径
    childCircle.r = sqrt(area_arr[i]/(2*PI));
    childCircles.appendCircle(childCircle);
  }
  std::cout << "================================================ " << std::endl;
  /*
  // test searchAngleResource()
  std::vector<std::vector<int>> restAngleIndex_vec = {};
  int restCount = 4;
  // std::vector<int> usedAngleIndex_vec = {0, 1, 4, 5, 9, 10, 11};
  std::vector<int> usedAngleIndex_vec = {0, 4, 1, 9, 5, 11, 10};
  // int usedCount = 7;
  // searchAngleResource(restAngleIndex_vec, restCount,
  //                      usedAngleIndex_vec);

  // test restAngleIndex_vec
  std::cout << "test restAngleIndex_vec" << std::endl;
  for (int i = 0; i < restAngleIndex_vec.size(); i++) {
    for (int j = 0; j < restAngleIndex_vec[i].size(); j++) {
      std::cout << restAngleIndex_vec[i][j] << " ";
    }
    std::cout << std::endl;
  }
  */
  
  /*
  int testArr[100][20] = {{3, 5, 8},{1, 2}, {7, 6, 9}, {10, 11, 4}};
  int n = 4;
  int m[100] = {3, 2, 3, 3};
  arr_n = 5;
  int result_arr[100] = {};
  flattenDoubleVec(testArr, n, m,
                   result_arr, arr_n);
  for (int i = 0; i < arr_n; i++) {
    std::cout << "result_arr[" << i << "] = " << result_arr[i] << std::endl;
  }
  */
  /* 测试std::vector
  std::vector<int> i_vec = {0, 1, 2, 3};
  std::cout << "i_vec.size() = " << i_vec.size() << std::endl;
  for (int i = 0; i < i_vec.size(); i++) {
    
    std::cout << "i = " << i << std::endl;
  }

  std::vector<Circle> cir_vec = {parentCircle};
  cir_vec.push_back(parentCircle);
  std::cout << "cir_vec.size() = " << cir_vec.size() << std::endl;

  std::vector<std::vector<int>> i_vec_double = {};
  i_vec_double.push_back(i_vec);
  std::cout << "i_vec_double[0].size() = " << i_vec_double[0].size() << std::endl;

  std::vector<int> r1 = {0, 1, 2}, r2 = {3, 4}, r3 = {0}, r4 = {8, 7};
  std::vector<std::vector<int>>
      c_r1 = {r1, r2, r3, r4},
      c_r2 = {r2, r4, r1};

  std::vector<std::vector<std::vector<int>>> result_vec = {};
  result_vec.push_back(c_r1);
  result_vec.push_back(c_r2);
  for (int i = 0; i < result_vec.size(); i++) {
    for (int j = 0; j < result_vec[i].size(); j++) {
      for (int x = 0; x < result_vec[i][j].size(); x++) {
        std::cout << result_vec[i][j][x] << ", ";
      }
      std::cout << "|";
    }
    std::cout << std::endl;
    
  }

  std::cout << "result_vec.size() = " << result_vec.size() << std::endl;
  
  */

  /*
  // 测试Vector类

  Vector<int> i_vec;
  i_vec.push_back(5);
  i_vec.push_back(6);
  std::cout << "i_vec.size() = " << i_vec.size() << std::endl;
  std::cout << "i_vec[1] = " << i_vec[1] << std::endl;

  int c = 10, s = 0;
  Circle v = parentCircle;
  Vector<Circle> cir_vec(c, s, v);
  cir_vec.push_back(parentCircle);
  std::cout << "cir_vec.size() = " << cir_vec.size() << std::endl;

  int r1_arr[10] = {0, 1, 2};
  int r1_c = 10, r1_s = 3;
  // Vector<int> r1(r1_c, r1_s, r1_arr);
  Vector<int> r1 = {0, 1, 2}, r2 = {3, 4}, r3 = {0}, r4 = {8, 7};

  Vector<int> r_test = {0, 1, 2, 3};
  std::cout << "r_test.size() = " << r_test.size() << std::endl;

  Vector<Vector<int>> c_r1 = {r1, r2, r3, r4};
  // Vector<Vector<int>> c_r2 = {r2, r4, r1};
  // Vector<Vector<Vector<int>>> result_vec = {c_r1, c_r2};
  // result_vec.push_back(c_r1);
  // result_vec.push_back(c_r2);

  // std::cout << "result_vec.size() = " << result_vec.size() << std::endl;
  */
}

int celling(const double a, const double b) {
  // 天花板除法
  int r = (a / b) + 1;
  // std::cout << "r = " << r
  //           << ", a / b = " << a / b << std::endl;
  return r;
}

int floor(const double a, const double b) {
  // 地板板除法
  int r = a / b;
  // std::cout << "r = " << r
  //           << ", a / b = " << a / b << std::endl;
  return r;
}


void searchAngleResource(std::vector<std::vector<int>>& restIndex_vec,
                         int resourceCount,
                         std::vector<int> usedAngleIndex_vec) {
  std::cout << "=== into searchAngleResource() ====" << std::endl;
  int allResourceCount = 20;
  std::cout << "allResourceCount = " << allResourceCount << std::endl;
  // test usedAngleIndex_vec
  for (int i = 0; i < usedAngleIndex_vec.size(); i++) {
    std::cout << usedAngleIndex_vec[i] << " ";
  }
  std::cout << std::endl;
  std::cout << "resourceCount = " << resourceCount << std::endl;

  int usedCount = usedAngleIndex_vec.size();     // 已占用资源数量
  if (!is_sortedVec(usedAngleIndex_vec)) {
    std::cout << "!is_sorted()" << std::endl;
    sortedVec(usedAngleIndex_vec);                  // 对乱序编号进行排序
  }
  std::cout << "usedCount = " << usedCount << std::endl;
  // 考虑尾部未占用空间
  usedAngleIndex_vec.push_back(allResourceCount);
  for (int i = 1; i < usedCount + 1; i++) {
    int gapLength = usedAngleIndex_vec[i] - usedAngleIndex_vec[i-1] - 1;
    std::cout << "gapLength = " << gapLength << std::endl;
    if (gapLength != 0) {    // 已使用过资源存在空隙
      if (gapLength >= resourceCount) {
        std::cout << "into gapLength >= resourceCount, "
                  << "gapLength = " << gapLength << ", "
                  << "resourceCount = " << resourceCount
                  << std::endl;
        for (int x = 0; x < (gapLength-resourceCount+1); x++) {
          std::cout << "x = " << x << std::endl;
          int y_index = usedAngleIndex_vec[i-1] + 1 + x;
          std::vector<int> pair_i_vec = {};
          for (int y = 0; y < resourceCount; y++) {
            // restIndex_vec[rest_n++][y] = y_index++;
            pair_i_vec.push_back(y_index++);
            std::cout << "y = " << y << ", "
                      << "y_index = " << y_index
                      << std::endl;
          }
          restIndex_vec.push_back(pair_i_vec);
        } 
      } 
    }
  }
  std::cout << "restIndex_vec.size() = " << restIndex_vec.size() << std::endl;
  std::cout << "=== end searchAngleResource() ====" << std::endl;
}

bool is_sortedVec(std::vector<int> i_vec) {
  // ..
  // std::cout << "is_sortedVec() i_vec.size() = " << i_vec.size() << std::endl;
  for (int i = 1; i < i_vec.size(); i++) {
    // std::cout << "is_sortedVec() i = " << i << std::endl;
    if (i_vec[i] < i_vec[i-1]) { return false;}
  }
  return true;
}

void sortedVec(std::vector<int>& i_vec) {
  if (!is_sortedVec(i_vec)) {        // vector无序
    // std::cout << "sortedVec() !is_sortedVec(i_vec)" << std::endl;
    for (int i = 0; i < i_vec.size()-1; i++) {
      for (int j = i + 1; j < i_vec.size(); j++) {
        if (i_vec[j] < i_vec[i]) {
          // swap(i_vec[j], i_vec[i]);
          int tmp = i_vec[j];
          i_vec[j] = i_vec[i]; i_vec[i] = tmp;
        }
      }
    }
  }

  /*// 检测
  for (int i = 0; i < i_vec.size(); i++) {
    std::cout << i_vec[i] << " ";
  }
  std::cout << std::endl;
  */
}

void flattenDoubleVec(std::vector<std::vector<int>> doubleVec,
                      std::vector<int>& resultVec) {
  // 拍平双重vec成单向vec
  for (int i = 0; i < doubleVec.size(); i++) {
    for (int j = 0; j < doubleVec[i].size(); j++) {
      resultVec.push_back(doubleVec[i][j]);
    }
  }

  /*
  // test flattenDoubleVec()
  std::cout << "test flattenDoubleVec()" << std::endl;
  for (int i = 0; i < resultVec.size(); i++) {
    std::cout << resultVec[i] << " ";
  }
  std::cout << std::endl;
  */
}


int getGapResourceIndex(std::vector<int> ivec1,
                         std::vector<std::vector<int>> ivec2,
                         std::vector<int>& gapIndex_vec) {
  // 判断资源区间是否有重复
  for (int i = 0; i < ivec1.size(); i++) {
    for (int j = 0; j < ivec2.size(); j++) {
      for (int x = 0; x < ivec2[j].size(); x++) {
        if (ivec1[i] == ivec2[j][x]) {
          gapIndex_vec.push_back(j);
          std::cout << "is_include() ivec1[" << i
                    << "] == ivec2[" << j
                    << "][" << x << "]"
                    << " ,j = " << j
                    << std::endl;
        }
      }
    }
  }
  // test gapIndex_vec
  for (int i = 0; i < gapIndex_vec.size(); i++) {
    std::cout << gapIndex_vec[i] << " ";
  }
  std::cout << std::endl;
  return gapIndex_vec.size();
}

void removeVec(std::vector<int> vec1, std::vector<int> vec2, std::vector<int>& vec3) {
  // 从vec1中减去vec2
  // std::vector<int> vec3;
  for (int i = 0; i < vec1.size(); i++) {
    bool push = true;
    for (int j = 0; j < vec2.size(); j++) {
      if (vec1[i] == vec2[j]) {
        push = false;
      }
    }
    if (push) {vec3.push_back(vec1[i]);}
  }


  // 检测
  std::cout << "----------- test  removeVec -----" << std::endl;
  std::cout << "vec1:" << "\n";
  for (int i = 0; i < vec1.size(); i++) {
    std::cout << vec1[i] << " ";
  }
  std::cout << std::endl;

  std::cout << "vec2:" << "\n";
  for (int i = 0; i < vec2.size(); i++) {
    std::cout << vec2[i] << " ";
  }
  std::cout << std::endl;

  std::cout << "vec3:" << "\n";
  for (int i = 0; i < vec3.size(); i++) {
    std::cout << vec3[i] << " ";
  }
  std::cout << std::endl;

}

void yield(const Circle P1, Circle& P2, Circle_lst& C2, const double unit_dist) {
  // P2退让, 拉开距离, C2整体改变
  double angle = getDirection(P1, P2);
  P2.moveCircle(angle, unit_dist);
  C2.moveCircles(angle, unit_dist);
}

// /*
void angleResourceDynamicWeight(Circle& P1, Circle& P2,
                                Circle_lst& C1, Circle_lst& C2,
                                std::vector<std::vector<int>> i_vec1,
                                std::vector<std::vector<int>>& i_vec2,
                                std::vector<Circle>& P2_vec,
                                std::vector<std::vector<std::vector<int>>>& i_vec2_resultWeight) {
  // 储存P2与所有C2的vector
  // std::vector<std::vector<std::vector<int>>> i_vec2_resultWeight = {};
  // std::vector<Circle> P2_vec = {};

  // ================ 为P2寻找相对于P1的角度资源 ===============
  Circle P2_tmp = P2;
  reviseParentUnboard(P1, C1, P2, C2, i_vec1);

  // ===================== test =============================

  // 改变P2, 所有C2位置, 保持角度分配和距离不变
  // double rotateAngle;
  // rotateAngle = (restIndexP2_vec[0][0] - resourceIndexP1P2[0]) * unitRadian;

  // rotateCircle(P2, P1, rotateAngle);

  double c2_move_angle = getDirection(P2, P2_tmp);
  double c2_move_dist = getDistance(P2, P1);
  std::cout << "c2_move_angle = " << c2_move_angle
            << "c2_move_dist = " << c2_move_dist << std::endl;
  C2.moveCircles(c2_move_angle, c2_move_dist);

  // P1固定, 子空间C2根据P1, P2角度资源进行动态分配
  // ===================== 修改至此 ===============
  double lowThreshold = P1.r + P2.r + 2e3;
  double highThreshold;
  // 得到两个相对于父空间最远的圆
  Circle farC1 = C1.getFarthestCircle(P1), farC2 = C2.getFarthestCircle(P1);
  // 可明显优化成对象类来写, 继承关系, 私有属性
  highThreshold = farC1.r + farC2.r +
      getDistance(P1, farC1) + getDistance(P2, farC2);
  // highThreshold = 2e3 * 8;
  std::cout << "highThreshold = " << highThreshold << std::endl;
  double dist = lowThreshold;
  double unit_dist = 2e3;
  while (dist < highThreshold) {     // 在退让到最高阈值之前
    std::cout << "--- in while{} dist = " << dist << "----------- "
              << std::endl;
    int i = 0;   // 防止最后一个c2出错
    for (i = 0; i < C2.n; i++) {      // 对P2的子空间逐一遍历
      bool mobility = true;
      reviseChildUnboard(P1, C1, P2, C2.circles[i],
                         i, i_vec1, i_vec2, mobility);
      if (!mobility) {   // 虽然资源占据重叠, 但无法排下C2_i
        // P2退让, C2整体移动
        yield(P1, P2, C2, unit_dist);
        // 强制退出当前for循环
        break;
      }
    }
    std::cout << "i = " << i << std::endl;
    if (i == C2.n) {     // 循环已对所有C2遍历更改
      std::cout << "i == c2.n" << std::endl;
      // 记录当前P2, 以及C2所占的资源数组
      i_vec2_resultWeight.push_back(i_vec2);
      P2_vec.push_back(P2);
      // yield(P1, P2, C2, unit_dist);
    }
    yield(P1, P2, C2, unit_dist);

    dist = getDistance(P1, P2);
  }
}


void getResourceIndex(Circle c1,Circle c2, std::vector<int>& resourceIndex_vec) {
  // c1为主圆, 得到c2相对于c1所占的资源列表
  const double unitRadian = 2*PI/20;
  double radian = getRadian(PI*pow(c2.r, 2), getDistance(c1, c2));
  double angle = getDirection(c1, c2);
  int first_i = floor(angle, unitRadian);      // 首个资源序号, 向下整除
  int resource_count = celling(radian, unitRadian);    // 当前圆所占资源数量
  std::cout << "resource_count = " << resource_count << std::endl;

  for (int i = 0; i < resource_count; i++) {
    resourceIndex_vec.push_back(first_i++);
  }
}


void reviseParentUnboard(Circle P1, Circle_lst C1,
                         Circle& P2, Circle_lst& C2,
                         std::vector<std::vector<int> >& i_vec1) {
  const double unitRadian = 2*PI/20;
  const double unit_dist = 2e3;
  // 父空间之间检测遮挡并修改P2占用角度资源
  // 储存P2占用P1的资源所有可能的情况
  std::vector<std::vector<int>> restIndexP2_vec = {};
  // 得到当前未修改前P2占用P1的资源
  std::vector<int> resourceIndexP1P2 = {};
  getResourceIndex(P1, P2, resourceIndexP1P2);   // 得到P2占P1的资源序
  // 得到P1子空间C1中与当前P2资源冲突的空间序号
  std::vector<int> gapIndex_vec = {};
  int gapCount = getGapResourceIndex(resourceIndexP1P2,
                                     i_vec1,
                                     gapIndex_vec);
  std::cout << "reviseParentUnboard() gapCount = " << gapCount << std::endl;
  if (gapCount) {
    // C2_i与C1所占的角度资源重复, 并找出资源重复的C1_i
    for (int gapIndex_i = 0; gapIndex_i < gapCount; gapIndex_i++) {
      // 考虑到当前空间可能与多个C1空间资源冲突
      // 对每一个资源重复占用的圆进行遍历
      if (getDistance(P2, P1)
          <= getDistance(C1.circles[gapIndex_vec[gapIndex_i]]
                         , P1)) {   // 当前空间遮挡C1_i与P1
        // P2所占用的资源数量
        int restCount = resourceIndexP1P2.size();
        // 从vec1中减去vec2, 得到已经被使用过的资源
        std::vector<int> i_vec1_flatten = {};
        flattenDoubleVec(i_vec1, i_vec1_flatten);
        searchAngleResource(restIndexP2_vec, restCount, i_vec1_flatten);
        // 只要有一个C1_i与之冲突, 得到修改可能性后, 退出循环
        break;
      }
    }
    if (restIndexP2_vec.size() != 0) {
      // P2所占资源的第一种情况, 添加入P1资源列表 ==> 可变化
      i_vec1.push_back(restIndexP2_vec[0]);
      std::cout << "restIndexP2_vec[0][0] = " << restIndexP2_vec[0][0]
                << ", restIndexP2_vec[0][1] = " << restIndexP2_vec[0][1]
                << std::endl;
      // 改变P2的位置
      double rotateAngle_P2 = getAngleFromResourceIndex(
          P2, P2, P1, resourceIndexP1P2, restIndexP2_vec[0], unitRadian);
      std::cout << "rotateAngle_P2 = " << rotateAngle_P2 << std::endl;
      rotateCircle(P2, P1, rotateAngle_P2);
    } else {
      // 退让
      yield(P1, P2, C2, unit_dist);
      std::cout <<
          "error::reviseParentUnboard() restIndexP2_vec.size() = 0"
                << std::endl;
    }
  } else {         // 不存在资源重复
    i_vec1.push_back(resourceIndexP1P2);
  }
}



void reviseChildUnboard(Circle P1, Circle_lst C1,
                        Circle P2, Circle& C2_i, int index,
                        std::vector<std::vector<int> > i_vec1,
                        std::vector<std::vector<int> >& i_vec2,
                        bool& mobility) {
  // 父空间与子空间之间, 检测遮挡并修改C2_i占用角度资源
  const double unitRadian = 2*PI/20;
  // 储存C2_i占用P1的资源所有可能的情况
  std::vector<std::vector<int>> restIndexC2_i_vec = {};
  // 得到当前未修改前C2_i占用P1的资源
  std::vector<int> resourceIndexP1C2_i = {};
  getResourceIndex(P1, C2_i, resourceIndexP1C2_i);

  std::vector<int> gapIndex_vec = {};
  int gapCount = getGapResourceIndex(resourceIndexP1C2_i,
                                     i_vec1,
                                     gapIndex_vec);
  std::cout << "reviseChildUnboard() gapCount = " << gapCount << std::endl;
  if (gapCount) {
    // C2_i与C1所占的角度资源重复, 并找出资源重复的C1_i
    // 考虑到一个C2圆可能与多个C1圆重叠
    for (int gapIndex_i = 0; gapIndex_i < gapCount; gapIndex_i++) {
      // 对每一个资源重复占用的圆进行遍历
      std::cout << getDistance(C2_i, P1) << " "
                << getDistance(C1.circles[gapIndex_vec[gapIndex_i]], P1)
                <<std::endl;
      if (getDistance(C2_i, P1)
          <= getDistance(C1.circles[gapIndex_vec[gapIndex_i]]
                         , P1)) {   // C2_i遮挡C1_i与P1

        // 相对于P2的占用, 寻找资源
        int restCount = resourceIndexP1C2_i.size();   // c2_i所占用的资源数量
        std::cout << "restCount = " << restCount << std::endl;
        // 从P2所占资源中减去C2_i占用的资源, 得到已经被使用过的资源
        std::vector<int> i_vec2_flatten = {};
        flattenDoubleVec(i_vec2, i_vec2_flatten);
        
        std::vector<int> usedAngleIndex_vec = {};
        removeVec(i_vec2_flatten, i_vec2[index], usedAngleIndex_vec);
        // searchAngleResource(restIndexC2_i_vec, restCount,
        //                     usedAngleIndex_vec);
        // std::cout << "restIndexC2_i_vec.size() = "
        //           << restIndexC2_i_vec.size() << std::endl;
        // 只要有一个C1_i与之冲突, 得到修改可能性后, 退出循环
        break;
      }
    }
    if (restIndexC2_i_vec.size() != 0) {    // 存在满足资源
      std::cout << "restIndexC2_i_vec.size() != 0" << std::endl;
      // 替换i_vec2资源列表index对应的资源, 先选择第一种
      i_vec2[index] = restIndexC2_i_vec[0];
      // 从位置角度更新C2_i
      double rotateAngle_C2_i = getAngleFromResourceIndex(
          C2_i, C2_i, P2, resourceIndexP1C2_i, restIndexC2_i_vec[0], unitRadian);
      rotateCircle(C2_i, P2, rotateAngle_C2_i);
    } else {   // 虽然资源占据重叠, 但无法排下C2_i
      // P2退让, 拉开距离, C2整体改变
      mobility = false;
      // yield(P1, P2, C2, unit_dist);
      // 退出当前函数, 强制退出当前for循环, continue是跳过当前一次循环
      // return; break;
    }
  }
  // 若不存在资源重复占用, 不会改动
}

double getAngleFromResourceIndex(Circle c1,
                                 Circle c2,
                                 Circle c,
                                 std::vector<int> c1_vec,
                                 std::vector<int> c2_vec,
                                 const double unitRadian) {
  // c1变换到c2，对于c旋转过的角度
  double angle =
      (c2_vec[0] * unitRadian + getRadian(c2, c) / 2)
      -
      (c1_vec[0] * unitRadian + getRadian(c1, c) / 2);
  return angle;
}

void angleResourceDynamicWeight(Circle_tree& ctre) {
  // 动态权重问题
  // 初始数据
  ParentCircle parentCircle1;
  Circle_lst childCircles1;
  std::vector<std::vector<int> > i_vec1 = {};

  parentCircle1.x = 0, parentCircle1.y = 0, parentCircle1.r = 2e3;
  // 子空间资源分配列表
  double area_arr1[100] = {10e6, 15.5e6, 14e6,
                           10.3e6, 5e6, 13.2e6};
  double dist_arr1[100] = {5e3,   13.2e3, 9e3,
                          6.4e3, 15.3e3, 10.2e3};
  int arr_n1 = 6;
  angleResourceArrange(i_vec1, parentCircle1, childCircles1,
                       area_arr1, dist_arr1, arr_n1);

  printVector(i_vec1[0]);


  ParentCircle parentCircle2;
  Circle_lst childCircles2;
  parentCircle2.x = 3e3, parentCircle2.y = 5e3, parentCircle2.r = 3e3;
  // 子空间资源分配列表
  double area_arr2[100] = {10e6,  20.5e6, 14e6,
                          7e6 , 30.2e6, 5e6};
  double dist_arr2[100] = {5e3,   13.2e3, 15.3e3,
                          13.2e3, 10.2e3, 5.2e3};
  int arr_n2 = 6;

  /* 得到子空间C2对于P1可以放的所有位置*/

  std::vector<std::vector<std::vector<int> > > set_vec3;
  int c2_count = arr_n2;
  for (int i = 0; i < c2_count; i++) {
    std::vector<std::vector<int> > set_vec2;
    // ..
    ChildCircle C;
    C.r = sqrt(area_arr1[i]/PI), C.dist = dist_arr1[i];
    getWorkableResourceIndexArrangementForParent(
        parentCircle1, parentCircle2,
        C,
        set_vec2);

    set_vec3.push_back(set_vec2);
  }


  /* 对子空间C2对于P1可以放的所有资源位置进行运算, 得到对于P2也成立的资源组合 */
  /*
  set_vec3 = {
    { {0, 1, 2}, {2, 3, 4}, {6, 7, 8} },
    { {2, 3}, {6, 7}, {8, 9}, {10, 11} },
    { {3}, {5}, {6}, {10}, {11} }
  };
  */
  std::vector<std::vector<std::vector<int> > > workableResouceIndex_3vec = {};
  getWorkableResourceIndexArrangement(set_vec3, workableResouceIndex_3vec);

  std::vector<std::vector<int> > final_vec2 = workableResouceIndex_3vec[0];
    angleResourceArrange(final_vec2, parentCircle2, childCircles2,
                       area_arr2, dist_arr2, arr_n2);

  Circle_lst clst1, clst2;

  clst1.appendCircle(parentCircle1);
  clst1.appendCircles(childCircles1);
  ctre.appendClst(clst1);
  clst2.appendCircle(parentCircle2);
  clst2.appendCircles(childCircles2);
  // */
  ctre.appendClst(clst2);

}

// 得到一个子空间C对于已排列资源P1的资源占据可能性
void getWorkableResourceIndexArrangementForParent(
    ParentCircle& P1, ParentCircle& P2,
    ChildCircle& C,
    std::vector<std::vector<int> >& workableResouceIndex_2vec) {
  P1.x = 0, P1.y = 0, P1.r = 2e3;
  P2.x = 3e3, P2.y = 5e3, P2.r = 3e3;
  double area = 15e6, dist = 5e3;
  C.r = sqrt(area/PI), C.dist = dist;
  // ChildCircle C1_1, C1_2, C1_3;
  // C1_1.x = 2e3, C1_1.y = 3e3, C1_1.r = 3e3, C1_1.parentCircle = P1;
  // C1_2.x = -3e3, C1_2.y = 3e3, C1_2.r = 3e3, C1_2.parentCircle = P1;
  // C1_3.x = -8e3, C1_3.y = -6e3, C1_3.r = 3e3, C1_3.parentCircle = P1;
  // ChildrenCircle_lst childrenClst;
  // childrenClst.childCircles[0] = C1_1;
  // childrenClst.childCircles[1] = C1_2;
  // childrenClst.childCircles[2] = C1_3;
  // C1_1.getCircleDataFromParent(P1);
  // C1_2.getCircleDataFromParent(P1);
  // C1_3.getCircleDataFromParent(P1);
  // P1.resourceOccupy_2vec.push_back(const value_type& __x)
  // std::vector<std::vector<int> > parentOccupy_2vec = P1.getResourceOccupy_2vec();
  // std::cout << "parentOccupy_2vec.size()" << parentOccupy_2vec.size() << std::endl;
  std::vector<std::vector<int> > p1_Occupy_2vec = {
        {0, 1, 2},
        {5, 6},
        {9, 10, 11},
        {13, 14, 15},
        {17} };
  std::vector<double> p1_dist_vec = {
    20e3,
    35e3,
    44e3,
    25e3,
    16e3
  };


  // C对于P2进行计算
  C.parentCircle = P2;
  int resourceOccupyCount = C.getResourceOccupyCount();
  std::cout << "resourceOccupyCount = " << resourceOccupyCount << std::endl;

  std::cout << "C.resourceCount = " << C.resourceCount << std::endl;
  // 生成C2对P2, 没有P1限制时所有可能的资源序号
  std::vector<std::vector<int> > rsrcIndex_2vec = {};
  for (int i = 0; i < C.resourceCount - resourceOccupyCount + 1; i++) {
    bool accessible = true;
    std::vector<int> rsrcIndex_vec = {};
    for (int j = 0; j < resourceOccupyCount; j++) {
      rsrcIndex_vec.push_back(i+j);
      // std::cout << i+j << " ";
    }

    rsrcIndex_2vec.push_back(rsrcIndex_vec);
    // std::cout << std::endl;
    // 根据资源序列修改当前圆
    C.reviseCircleFromRsrcIndex(rsrcIndex_vec);

    std::cout << "C.x = " << C.x << " "
              << "C.y = " << C.y << " "
              << "C.r = " << C.r << std::endl;

    // 使得当前圆按照P1的子空间进行性计算,
    // 得到当前圆对于P1所占的资源和距离
    C.getCircleDataFromParent(P1);

    // /*
    
    std::vector<std::vector<int> > vec2_added = {};
    // 此时占用资源与P1的子空间所占用的资源和距离进行计算
    for (int x = 0; x < p1_Occupy_2vec.size(); x++) {
      std::vector<int> vec_added = C.rsrcIndex_vec;
      // printVector(vec_added);
      
      for (int y = 0; y < p1_Occupy_2vec[x].size(); y++) {
        vec_added.push_back(p1_Occupy_2vec[x][y]);
      }
      printVector(vec_added);
      vec2_added.push_back(vec_added);
    }

    
    for (int x = 0; x < vec2_added.size(); x++) {
      std::vector<int> vec_added = vec2_added[x];
      std::vector<int> vec_union = {};
      // printVector(vec_added);
      setVector(vec_added, vec_union);
      // std::cout << "vec_added.size() = " << vec_added.size()
      //           << "vec_union.size() = " << vec_union.size()
      //           << std::endl;
      
      // printVector(vec_union);
      std::cout << "C.dist = " << C.dist
                << "p1_dist_vec[x] = " << p1_dist_vec[x]
                << std::endl;
      
      if (
              (vec_added.size() != vec_union.size() &&
               (C.dist < p1_dist_vec[x]))
          ) {   // 在这个圆距离之内 以及 资源有重合
        // printVector(vec_added);
        // printVector(C.rsrcIndex_vec);
        accessible = false;
        break;
        std::cout << "break" << std::endl;
        
        // workableResouceIndex_2vec.push_back(rsrcIndex_vec);
      }
    }

    if (accessible) {
      std::cout << "workableResouceIndex_2vec.push_back(rsrcIndex_vec)" << std::endl;
      workableResouceIndex_2vec.push_back(rsrcIndex_vec);
    }

      // /*
      
      
      // */
  }
   // 留下满足条件, C对于P2的rsrcIndex_vec
  // if (false) {
  //    workableResouceIndex_2vec.push_back(rsrcIndex_vec);
  //  }
  /*
  std::vector<int> rsrcIndex_vec = {};
  C.rsrcIndex_vec = rsrcIndex_vec;
  C.reviseCircleFromRsrcIndex(rsrcIndex_vec);
  printVector(C.rsrcIndex_vec);

  C.getCircleDataFromParent(P1);
  printVector(C.rsrcIndex_vec);
  */
}


void getWorkableResourceIndexArrangement(
    std::vector<std::vector<std::vector<int> > > setVec,
    std::vector<std::vector<std::vector<int> > >& workableResouceIndex_3vec
                                         ) {
  // ..
  setVec = {
    { {0, 1, 2}, {2, 3, 4}, {6, 7, 8} },
    { {2, 3}, {6, 7}, {8, 9}, {10, 11} },
    { {3}, {5}, {6}, {10}, {11} }
  };
  int set_b_count = setVec.size();
  /* 得到集合运算的全部索引 */
  std::vector<std::vector<int> > i_2vec = {};
  // 从全部为0开始, 从最后一位向上递增
  std::vector<int> i_vec(set_b_count, 0);
  // 添加入第一个索引
  i_2vec.push_back(i_vec);
  int i_vec_maxIndex = set_b_count - 1;
  std::cout << "------- into while-----" << std::endl;
  while (i_vec[0] < setVec[0].size()) {
    // 最后一位向上递增
    i_vec[i_vec_maxIndex]++;
    int full_i = i_vec_maxIndex;
    while ( (full_i > 0)&&(i_vec[full_i] >
                          setVec[full_i].size()-1) ) {   // 索引溢出
      // 当前位置换成0
      i_vec[full_i] = 0;
      // 向前进一位
      i_vec[--full_i]++;
    }
    if (i_vec[0] < setVec[0].size()) {   // 保证不添加最后一个无效数据
      std::cout << i_vec[0] << " "
                << i_vec[1] << " "
                << i_vec[2] << " " <<  std::endl;
      i_2vec.push_back(i_vec);
    }
  }
  std::cout << "------- quit while-----" << std::endl;

  
  /*将索引对应集合添加到一个集合, 取并集*/
  for (int i = 0; i < i_2vec.size(); i++) {        // 对应索引组合的一种情况
    std::vector<std::vector<int> > vec_added = {};
    for (int j = 0; j < set_b_count; j++) {
      vec_added.push_back(setVec[j][i_2vec[i][j]]);
    }

    // 对添加完毕的索引取并集
    std::vector<int> vec_added_flatten = {};
    flattenDoubleVec(vec_added, vec_added_flatten);
    std::vector<int> vec_union = {};
    setVector(vec_added_flatten, vec_union);
    if (vec_added_flatten.size() == vec_union.size()) {
      // 运算后没有重复的资源
      // 将当前合集添入到可用结果中
      workableResouceIndex_3vec.push_back(vec_added);
    }
  }

  // test workableresouceindex
  std::cout << "------ test workableresouceindex ------- " << std::endl;
  for (int i = 0; i < workableResouceIndex_3vec.size(); i++) {
    for (int j = 0; j < workableResouceIndex_3vec[i].size(); j++) {
      for (int x = 0; x < workableResouceIndex_3vec[i][j].size(); x++) {
        // ..
        std::cout << workableResouceIndex_3vec[i][j][x] << " ";
      }
      std::cout << ", ";
    }
    std::cout << std::endl;
  }

}

void setVector(std::vector<int> vec, std::vector<int>& vec_union) {
  // std::cout << "------------ test setVector ------------" << std::endl;
  // printVector(vec);
  // vector中重复元素只保留一个
  // vec = {8, 5, 3, 2, 1, 2, 3, 6, 7, 8, 10, 8, 3};
  // 对vector排序
  sortedVec(vec);
  // 逐一检查, 前后是否有重复
  vec_union.push_back(vec[0]);
  for (int i = 1; i < vec.size(); i++) {
    if (vec[i] != vec[i-1]) {
      vec_union.push_back(vec[i]);
    }
  }
  // printVector(vec_union);
  // std::cout << "------------ end test setVector ------------" << std::endl;
}

void printVector(std::vector<int> vec) {
  std::cout << "--------print vector -------" << std::endl;
  for (int i = 0; i < vec.size(); i++)
    std::cout << vec[i] << " ";
  std::cout << std::endl;
}

// void addVector(std::vector<int>& vec1, std::vector<int> vec2) {
//   // vec2添加到vec1之后
// }



// */

int main() {
  Circle_lst clst;
  Circle_tree ctre;
  // test_surround(clst);
  // test_shareDegree(clst);
  // test_orientate(clst);
  // test_orientate_surround_combine(clst);
  // test_coverDegree(clst);
  // test_unboard(clst);
  // test_align(clst);
  // test_align_surround(clst);
  // test_collide(clst);
  // test_moveCircles(clst);
  // test_clusterConnection(ctre);
  // test_angleResourceArrange(ctre);
  // test_getWorkableResourceIndexArrangement(ctre);
  // test_getWorkableResourceIndexArrangementForParent(ctre);
  angleResourceDynamicWeight(ctre);
  std::cout << "clst.n = " << clst.n << std::endl;
  // test_newObject(ctre);

  Circle_lst draw_circles;           // 用于绘图的列表
  draw_circles.appendCircles(clst);

  ctre.printTreeCircles();
  Circle_tree draw_ctre;
  draw_ctre = ctre;
  main_draw(draw_ctre);

  return 0;
}

void test_getWorkableResourceIndexArrangementForParent(Circle_tree& ctre) {
  ParentCircle P1, P2;
  ChildCircle C;
  std::vector<std::vector<int> > workableResouceIndex_2vec;
  P1.x = 0, P1.y = 0, P1.r = 2e3;
  P2.x = 3e3, P2.y = 5e3, P2.r = 3e3;
  double area = 10e6, dist = 5e3;
  C.r = sqrt(area/PI), C.dist = dist;
  getWorkableResourceIndexArrangementForParent(
    P1, P2,
    C,
    workableResouceIndex_2vec);
}


void test_getWorkableResourceIndexArrangement(Circle_tree& ctre) {
  std::vector<std::vector<std::vector<int> > > setVec;
  setVec = {
    { {0, 1, 2}, {2, 3, 4}, {6, 7, 8} },
    { {2, 3}, {6, 7}, {8, 9}, {10, 11} },
    { {3}, {5}, {6}, {10}, {11} }
  };
  std::vector<std::vector<std::vector<int> > > workableResouceIndex_3vec = {};
  getWorkableResourceIndexArrangement(setVec, workableResouceIndex_3vec);
}


void test_angleResourceArrange(Circle_tree& ctre) {


  Circle parentCircle;
  Circle_lst childCircles;
  Circle_lst clst1;
  std::vector<std::vector<int> > i_vec1;
  
  parentCircle.x = 0, parentCircle.y = 0, parentCircle.r = 2e3;
  // 子空间资源分配列表
  /*
  double area_arr[100] = {10e6, 15.5e6, 20.5e6, 14e6,
                          7e6 , 30.2e6, 10.3e6, 8.2e6, 5e6, 13.2e6};
  double dist_arr[100] = {5e3,   13.2e3, 19e3, 9e3, 6.4e3,
                          6.6e3, 8.2e3,  15.3e3, 13.2e3, 10.2e3,
                          };
  int arr_n = 10;
  */
  double area_arr[100] = {10e6, 15.5e6, 14e6,
                           10.3e6, 5e6, 13.2e6};
  double dist_arr[100] = {5e3,   13.2e3, 9e3,
                          6.4e3, 15.3e3, 10.2e3};
  int arr_n = 6;
  angleResourceArrange(i_vec1, parentCircle, childCircles,
                       area_arr, dist_arr, arr_n);


  Circle parentCircle2;
  Circle_lst childrenCircles2;
  Circle_lst clst2;
  std::vector<std::vector<int> > i_vec2;

  parentCircle2.x = 3e3, parentCircle2.y = 5e3, parentCircle2.r = 3e3;
  // 子空间资源分配列表
  double area_arr2[100] = {10e6,  20.5e6, 14e6,
                          7e6 , 30.2e6, 5e6};
  double dist_arr2[100] = {5e3,   13.2e3, 15.3e3,
                          13.2e3, 10.2e3, 5.2e3};
  int arr_n2 = 6;
  angleResourceArrange(i_vec2, parentCircle2, childrenCircles2,
                       area_arr2, dist_arr2, arr_n2);

  

  
  // 动态权重
  // 储存P2与所有C2的vector
  std::vector<std::vector<std::vector<int>>> i_vec2_resultWeight = {};
  std::vector<Circle> P2_vec = {};
  angleResourceDynamicWeight(parentCircle, parentCircle2,
                             childCircles, childrenCircles2,
                             i_vec1,
                             i_vec2,
                             P2_vec,
                             i_vec2_resultWeight);


  clst1.appendCircle(parentCircle);
  clst1.appendCircles(childCircles);
  ctre.appendClst(clst1);
  clst2.appendCircle(parentCircle2);
  clst2.appendCircles(childrenCircles2);

  ctre.appendClst(clst2);
}

void test_newObject(Circle_tree& ctre) {
  std::cout << "============= test_newObject =============" << "\n";
  ParentCircle P(2e3, 2e3, 2e3);
  P.x = 1.6e3, P.y = 2.5e3, P.r = 2e3;
  ChildCircle P_c1(P, 1.3e3, 3.4e3, 2.2e3);
  std::cout << "P_c1.getParentCircle().r = "
            << P_c1.getParentCircle().r << std::endl;

  
  
  std::cout << std::endl;
}

void test_clusterConnection(Circle_tree& ctre) {
  // ..
  /*
    // 可用1
    clst[0] :
0, -550, -430, 230
1, -928.901, -962.208, 141.386
2, -326.347, 402.455, 221.297
3, 138.168, 191.03, 188.653
clst[1] :
0, 1697.11, 1362.09, 280
1, 1541.82, 1868.61, 226.594
2, 955.416, 303.379, 138.752
clst[2] :
0, -371.733, -239.921, 1110.81
1, 1396.89, 1129.91, 1126.25

  Circle c1_1, c1_2, c1_3, c2_1, c2_2;
  c1.x = -550, c1.y = -430, c1.r = 230;
  c1_1.x = -928.901, c1_1.y = -962.208, c1_1.r = 141.386;
  c1_2.x = -326.347, c1_2.y = 402.455, c1_2.r = 221.297;
  c1_3.x = 138.168, c1_3.y = 191.03, c1_3.r = 188.653;
  c2.x =  1697.11, c2.y = 1362.09, c2.r = 280;
  c2_1.x = 1541.82, c2_1.y = 1868.61, c2_1.r = 226.594;
  c2_2.x = 955.416, c2_2.y = 303.379, c2_2.r = 138.752;
// 可用2
====== print circles in tree =======
clst[0] :
0, -550, -430, 230
1, -307.198, -559.238, 166.634
2, -819.099, -882.089, 242.644
3, -317.703, -301.663, 140.208
clst[1] :
0, 608.848, 538.105, 280
1, 1098.19, -103.192, 172.149
2, 908.393, 1206.17, 151.455
clst[2] :
0, -530.871, -562.366, 773.356
1, 789.591, 541.144, 947.503

  Circle c1_1, c1_2, c1_3, c2_1, c2_2;
  c1.x = -550, c1.y = -430, c1.r = 230;
  c1_1.x = -307.198, c1_1.y = -559.238, c1_1.r = 166.634;
  c1_2.x = -819.099, c1_2.y = -882.089, c1_2.r = 242.644;
  c1_3.x = -317.703, c1_3.y = -301.663, c1_3.r = 140.208;
  
  c2.x =  608.848, c2.y = 538.105, c2.r = 280;
  c2_1.x = 1098.19, c2_1.y = -103.192, c2_1.r = 172.149;
  c2_2.x = 908.393, c2_2.y = 1206.17, c2_2.r = 151.455;

  // 可用2
clst[0] :
0, -550, -430, 230
1, -677.248, 699.871, 226.554
2, 395.525, 844.406, 101.604
3, 485.975, 36.0051, 250.347
clst[1] :
0, 1694.4, 1280.57, 280
1, 1783.6, 1678.5, 185.535
2, 961.497, 857.648, 102.644
clst[2] :
0, -118.233, 143.005, 1123.36
1, 1444.58, 1264.42, 800.162

// 可用2
clst[0] :
0, -550, -430, 230
1, 272.683, -30.5248, 117.396
2, 149.634, -430.779, 194.05
3, -467.98, -9.18812, 260.436
clst[1] :
0, 1885.06, 274.748, 280
1, 1939.04, -753.846, 221.129
2, 1073.46, 213.778, 167.03
clst[2] :
0, -194.96, -204.376, 741.528
1, 1536.54, -210.113, 989.978

   */
  Circle c1, c2;     // 两个护理站
  Circle_lst clst1, clst2;
  int clusterCount = 2;
  srand((unsigned)time(NULL));
  // c1.x = getRandData(-500, 0), c1.y = getRandData(-500, 0);
  // c1.r = getRandData(100, 300);
  // c2.x = getRandData(0, 500), c2.y = getRandData(0, 500);
  // c2.r = getRandData(100, 300);
  c1.x = -550, c1.y = -430;
  c1.r = 230;
  c2.x = 300, c2.y = 280;
  c2.r = 280;

  c1.x = -550, c1.y = -430, c1.r = 230;
  /*
  Circle c1_1, c1_2, c1_3, c2_1, c2_2;
  c1.x = -550, c1.y = -430, c1.r = 230;
  c1_1.x = -307.198, c1_1.y = -559.238, c1_1.r = 166.634;
  c1_2.x = -819.099, c1_2.y = -882.089, c1_2.r = 242.644;
  c1_3.x = -317.703, c1_3.y = -301.663, c1_3.r = 140.208;
  
  c2.x =  608.848, c2.y = 538.105, c2.r = 280;
  c2_1.x = 1098.19, c2_1.y = -103.192, c2_1.r = 172.149;
  c2_2.x = 908.393, c2_2.y = 1206.17, c2_2.r = 151.455;
  
  clst1.appendCircle(c1);
  clst1.appendCircle(c1_1);
  clst1.appendCircle(c1_2);
  clst1.appendCircle(c1_3);
  clst2.appendCircle(c2);
  clst2.appendCircle(c2_1);
  clst2.appendCircle(c2_2);
  */

  // /*
  // 根据c1, c2随机生成数量一定的聚落
  const int room_count1 = 30, room_count2 = 5;
  Circle_lst unboardRooms1, unboardRooms2;
  Circle circle_arr[50] = {};
  Circle_lst unboardRooms_arr[50] = {};
  int count_arr[50] = {};
  

  circle_arr[0] = c1, circle_arr[1] = c2;
  unboardRooms_arr[0] = unboardRooms1;
  unboardRooms_arr[1] = unboardRooms2;
  count_arr[0] = room_count1;
  count_arr[1] = room_count2;
  for (int i = 0; i < clusterCount; i++) {
    getUnboardRooms(circle_arr[i], unboardRooms_arr[i], count_arr[i]);
  }

  clst1.appendCircle(c1);
  clst2.appendCircle(c2);

  clst1.appendCircles(unboardRooms_arr[0]);
  clst2.appendCircles(unboardRooms_arr[1]);
  // */

  clst1.getCoverCircle();
  clst2.getCoverCircle();


  // 两个聚落碰撞问题
  collide_cluster(clst1, clst2);

  // 2, 两个聚落核心空间 通(遮挡)问题
  // 2a, 计算c1, c2, c1_i的关系, c2, c1, c2_i的遮挡

  bool result = false;
  Circle_lst movedRooms1, restRooms1;
  int restRooms1_iarr[50] = {};           // 保存剩余空间索引, 序列顺序不变
  int restRooms1_icount = 0;
  for (int i = 1; i < clst1.n; i++) {
    result = is_unboard(clst1.circles[0], clst2.circles[0],
                          clst1.circles[i]);
    if (result) {            // 如果c1_i与c1, c2产生遮挡
      // 修改c1_i产生新的满足条件的圆
      reviseUnboard(clst1.circles[0], clst2.circles[0],
                          clst1.circles[i]);
      movedRooms1.appendCircle(clst1.circles[i]);
    } else {
      // std::cout << "rest1 i = " << i << std::endl;
      restRooms1.appendCircle(clst1.circles[i]);
      restRooms1_iarr[restRooms1_icount++] = i;     // 保存当前索引
    }
  }

  Circle_lst movedRooms2, restRooms2;
  int restRooms2_iarr[50] = {};
  int restRooms2_icount = 0;
  
  for (int i = 1; i < clst2.n; i++) {
    result = is_unboard(clst2.circles[0], clst1.circles[0],
                          clst2.circles[i]);
    if (result) {            // 如果c1_i与c1, c2产生遮挡
      // 修改c1_i产生新的满足条件的圆
      reviseUnboard(clst2.circles[0], clst1.circles[0],
                          clst2.circles[i]);
      movedRooms2.appendCircle(clst2.circles[i]);
    } else {
      // std::cout << "rest2 i = " << i << std::endl;
      restRooms2.appendCircle(clst2.circles[i]);
      restRooms2_iarr[restRooms2_icount++] = i;     // 保存当前索引
    }
  }

  // /*
  // 2b, 计算clst1与clst2内部的剩余空间restRooms遮挡
  getUnboardRooms(clst1.circles[0], movedRooms1, restRooms1);
  getUnboardRooms(clst2.circles[0], movedRooms2, restRooms2);
  // 按序替换遮挡更新后的空间
  for (int i = 0; i < restRooms1_icount; i++) {
    clst1.circles[restRooms1_iarr[i]] = restRooms1.circles[i];
    // std::cout << "restRooms1_iarr[i] = " << restRooms1_iarr[i] << std::endl;
  }
  for (int i = 0; i < restRooms2_icount; i++) {
    clst2.circles[restRooms2_iarr[i]] = restRooms2.circles[i];
    // std::cout << "restRooms2_iarr[i] = " << restRooms2_iarr[i] << std::endl;
  }

  // */





  // 绘图
  Circle_lst coverClst;
  coverClst.appendCircle(clst1.coverCircle);
  coverClst.appendCircle(clst2.coverCircle);

  ctre.appendClst(clst1);
  ctre.appendClst(clst2);
  ctre.appendClst(coverClst);

  ctre.printTreeCircles();

  // clst.appendCircles(cij_move_lst);
}

void test_moveCircles(Circle_lst& clst) {
  Circle c;
  c.x = -600, c.y = 300, c.r = 273;
  Circle c1, c2;

  int arr_n = 2 * 2;
  double r_arr[50] = {};
  // srand((unsigned)time(NULL));
  for (int i = 0; i < arr_n; i++) {
    Circle ci;
    ci.x = getRandData(-1000, 2000);
    ci.y = getRandData(-1000, 2000);
    ci.r = getRandData(100, 250);
    clst.appendCircle(ci);
  }

  clst.getCoverCircle();
  clst.appendCircle(clst.coverCircle);

  Circle_lst new_clst = clst;

  double angle = 145/(180/PI);
  double dist = 500;
  new_clst.moveCircles(angle, dist);

  clst.appendCircles(new_clst);
}

void test_align(Circle_lst& clst) {
  // 确定圆的坐标和半径
  double X = -1200, Y = -1000, radius = 300;
  Circle circle;
  circle.x = X, circle.y = Y, circle.r = radius;

  int circle_n = 3;                 // 环绕空间的数量
  // double area_arr[size] = {10000, 30050, 300300, 2300, 10000};
  // double area_arr[size] = {35000};
  // double area_arr[size] = {50000, 8000, 8000, 8000, 10000};
  const int size = 50;              // 面积数组规模
  double area_arr[size] = {10000, 35500, 40000};
  double direction = 70/(180/PI);
  double dist = 500;                 // 与确定空间中心点距离
  double offset = 45/(180/PI);

  Circle_lst clst_new;
  align(circle, clst_new, area_arr, circle_n, direction, dist);

  clst.appendCircle(circle);
  clst.appendCircles(clst_new);
}


void test_surround(Circle_lst& clst) {
  // 用于测试空间环绕算法
  // =====================
  // 确定圆的坐标和半径
  double X = -1200, Y = -1000, radius = 300;
  Circle circle;
  circle.x = X, circle.y = Y, circle.r = radius;

  int circle_n = 3;                 // 环绕空间的数量
  // double area_arr[size] = {10000, 30050, 300300, 2300, 10000};
  // double area_arr[size] = {35000};
  // double area_arr[size] = {50000, 8000, 8000, 8000, 10000};
  const int size = 50;              // 面积数组规模
  double area_arr[size] = {10000, 35500, 40000};
  double direction = 70/(180/PI);
  double dist = 480;                 // 与确定空间中心点距离
  double offset = 45/(180/PI);

  Circle_lst clst_new;
  surround(circle, clst_new, area_arr, circle_n, direction, dist);

  clst.appendCircle(circle);
  clst.appendCircles(clst_new);

}

void test_shareDegree(Circle_lst &clst) {
  // 测试共享度问题
  Circle c1, c2;
  c1.x = -1200, c1.y = -1000, c1.r = 300;
  c2.x = -1200, c2.y = -700,  c2.r = 150;
  getShareDegree(c1, c2);

  clst.appendCircle(c1);
  clst.appendCircle(c2);
}

void test_orientate(Circle_lst &clst) {
  // 测试关联方向问题
  double X = -1200, Y = -1000, radius = 300;
  Circle room1;
  room1.x = X, room1.y = Y, room1.r = radius;
  // 用于储存圆位置和半径的数列
  clst.appendCircle(room1);

  double direction = 70/(180/PI);
  double dist = 480;                 // 与确定空间中心点距离
  double offset = 0/(180/PI);

  Circle room2;
  orientate(room1, room2, direction, offset, dist);

  double theta_rotate = 180/(180/PI);
  rotateCircle(room2, room1, theta_rotate);   // 旋转room2

  clst.appendCircle(room1);
  clst.appendCircle(room2);
  // clst.appendCircle(room_rotate);
}

void test_orientate_surround_combine(Circle_lst &clst) {
  // 测试关联排列和关联方向的组合
  double X = -1200, Y = -1000, radius = 300;
  Circle room1;
  room1.x = X, room1.y = Y, room1.r = radius;

  int circle_n = 3;                 // 环绕空间的数量
  // double area_arr[size] = {10000, 30050, 300300, 2300, 10000};
  // double area_arr[size] = {35000};
  // double area_arr[size] = {50000, 8000, 8000, 8000, 10000};
  const int size = 50;              // 面积数组规模
  double area_arr[size] = {10000, 35500, 40000};
  double direction = 70/(180/PI);
  double dist = 480;                 // 与确定空间中心点距离
  double offset = 45/(180/PI);

  Circle_lst clst_new;
  orientate_surround_combine(room1,
                             clst_new, area_arr, circle_n,
                             direction, dist, offset);

  clst.appendCircle(room1);
  clst.appendCircles(clst_new);
}

void test_coverDegree(Circle_lst& clst) {
  // 测试影响度, 方向, 弧度大小
  Circle c1, c2;
  c1.x = -1200, c1.y = -1000, c1.r = 300;
  c2.x = -1200, c2.y = -300,  c2.r = 350;

  double room1_pos[2] = {c1.x, c1.y};
  double room2_pos[2] = {c2.x, c2.y};
  double room2_r = c2.r;
  
  double myDirec = getDirection(room1_pos, room2_pos)*180/PI;
  double myDegree = getCoverDegree(room1_pos, room2_pos, room2_r);
  double radian = getRadian(c2.r*c2.r*PI, getDistance(room1_pos, room2_pos));

  std::cout << "myDirection = " << myDirec
            << "myDegree = " << myDegree
            << "radian = " << radian*180/PI << std::endl;

  clst.appendCircle(c1);
  clst.appendCircle(c2);
}

void test_unboard(Circle_lst& clst) {
  // 关联环绕排序遮挡问题
  // 确定c和c1, 生成c2
  Circle c;
  c.x = -600, c.y = 300, c.r = 273;
  Circle c1, c2;

  int arr_n = 2 * 2;
  double r_arr[50] = {};
  srand((unsigned)time(NULL));
  for (int i = 0; i < arr_n; i++) {
    r_arr[i] = getRandData(-1000, 2000);
  }
  c1.x = -700, c1.y = -800, c1.r = 200;
  c2.x = -650, c2.y = -350,  c2.r = 175;    // 内用于测试
  // c2.x = -700, c2.y = -350,  c2.r = 175;
  // c2.x = -800, c2.y = -1100,  c2.r = 175;      // 外用于测试
  // c2.x = -700, c2.y = -1100,  c2.r = 175;
  // c2.x = -1100, c2.y = -1100,  c2.r = 175;
  c1.x = r_arr[0], c1.y = r_arr[1], c1.r = getRandData(100, 200);
  c2.x = r_arr[2], c2.y = r_arr[3], c2.r = getRandData(100, 300);

  // bool result = is_unboard(c, c1, c2);
  // std::cout << "result = " << result << std::endl;
  // 单个修改生成后不遮挡的空间
  /*
  if (result) {
    reviseUnboard(c, c1, c2);             // 后馈修改遮挡问题
  }
  */

  // /*

  // 生成并修改多个互不遮挡的空间
  int room_count =  4;
  Circle_lst unboardRooms;
  // 生成数据
  unboardRooms.appendCircle(c1);
  for (int i = 1; i < room_count; i++) {
    // std::cout << "i = " << i << std::endl;
    Circle ci;
    ci.x = getRandData(-1000, 1000), ci.y = getRandData(-1000, 1000);
    ci.r = getRandData(100, 300);
    
    bool result = false;
    int j = 0;
    while ((j < unboardRooms.n) || (result == true)) {
      result = is_unboard(c, unboardRooms.circles[j], ci);
      // std::cout << "j = " << j << ", result = " << result << std::endl;
      if (result) {            // 如果ci与已经生成的圆产生遮挡
        // 修改ci产生新的满足条件的圆
        reviseUnboard(c, unboardRooms.circles[j], ci);
        result = false;        // ci与cj,c之间无遮挡
        j = 0;                 // 从头开始检测
      } else {++j;}
    }   // 退出while循环
    std::cout << "i = " << i
              << ", ci.x = " << ci.x
              << ", ci.y = " << ci.y
              << ", ci.r = " << ci.r << std::endl;
    unboardRooms.appendCircle(ci);
  }
  clst.appendCircles(unboardRooms);

  // 检测是否会遮挡
  // for (int i = 0; i < unboardRooms.n; i++) {
  //   for (int j = 0; j < unboardRooms.n; j++) {
  //     if (i != j) {
  //       Circle ci = unboardRooms.circles[i];
  //       Circle cj = unboardRooms.circles[j];
  //       std::cout << is_unboard(c, ci, cj) << std::endl;
  //     }
  //   }
  // }

  // 打印生成圆的信息
  unboardRooms.printCircles();

  // */
  

  clst.appendCircle(c);

  std::cout << "clst.n = " << clst.n << std::endl;
  // 测试coverCircle
  // clst.getCoverCircle();
  // clst.appendCircle(clst.coverCircle);

  // clst.appendCircle(c1);
  // clst.appendCircle(c2);    // 在if语句中添加
}

void test_align_surround(Circle_lst& clst) {
  // 测试关联定向和环绕问题
  double X = -1200, Y = -1000, radius = 300;
  Circle circle;
  circle.x = X, circle.y = Y, circle.r = radius;
  int circle_n = 3;                 // 环绕空间的数量
  // double area_arr[size] = {10000, 30050, 300300, 2300, 10000};
  // double area_arr[size] = {35000};
  // double area_arr[size] = {50000, 8000, 8000, 8000, 10000};
  const int size = 50;              // 面积数组规模
  double area_arr[size] = {10000, 35500, 40000};
  double direction = 70/(180/PI);
  double dist = 480;                 // 与确定空间中心点距离
  double offset = 45/(180/PI);

  Circle_lst clst_new;
  surround(circle, clst_new, area_arr, circle_n, direction, dist);
  // 以最后一个圆为定位
  Circle lastCircle = clst_new.circles[clst_new.n];
  Circle_lst clst_align;
  srand((unsigned)time(NULL));
  double area_arr_align[50] = {};
  int n_align = (int)(rand()%30);
  double direction_align;
  double dist_align;
  std::cout << "n_align = " << n_align << std::endl;
  for (int i = 0; i < n_align; i++) {
    // 生成用于生成align圆的随机参数
    double area = (double)(rand()%100000);
    
    area_arr_align[i] = area;
    direction_align = (double)(rand()%(3));
    dist_align = (double)(rand()%30);
    std::cout << "area = " << area
              << "direction_align = " << direction_align
              << "dist_align = " << dist_align << std::endl;
  }
  align(lastCircle, clst_align, area_arr_align, n_align,
        direction_align, dist_align);


  clst.appendCircle(circle);
  clst.appendCircles(clst_new);

  clst.appendCircles(clst_align);
}

void test_collide(Circle_lst& clst) {
  // 测试关联方向问题
  Circle c;
  c.x = -600, c.y = 300, c.r = 273;
  Circle c1, c2;

  int arr_n = 2 * 2;
  double r_arr[50] = {};
  srand((unsigned)time(NULL));
  for (int i = 0; i < arr_n; i++) {
    r_arr[i] = getRandData(-1000, 2000);
  }
  c1.x = -300, c1.y = 500, c1.r = 200;
  // c1.x = r_arr[0], c1.y = r_arr[1], c1.r = getRandData(100, 200);
  // c2.x = r_arr[2], c2.y = r_arr[3], c2.r = getRandData(100, 300);

  Circle c1_new;
  collide(c, c1, c1_new);

  clst.appendCircle(c);
  clst.appendCircle(c1);
  clst.appendCircle(c1_new);

  clst.getCoverCircle();
  clst.appendCircle(clst.coverCircle);
}


/* -------------------- 绘图部分 -------------------------------- */
const int SCALE = 2e4;
double zoom = 1;


void scroll_callback(GLFWwindow* window, double xoffset, double yoffset) {
  double scroll_speed = 0.03;
  if (zoom >= 0.0f && zoom <= 45.0f)
    zoom -= yoffset * scroll_speed;
  if (zoom <= 0.0f)
    zoom = 0.0f;
  if (zoom >= 45.0f)
    zoom = 45.0f;
}

void drawPoint() {
  /* Draw a point */
  glClearColor(0.0, 0.0, 0.0, 0.0);
  glClear(GL_COLOR_BUFFER_BIT);
  glPointSize(8.0f);
  glBegin(GL_POINTS);

  glColor3f(1.0, 0.0, 0.0);    // Red
  glVertex2f(0.0f, 0.0f);
  glVertex2f(0.5f, 0.8f);
  glEnd();
}

void drawLine() {
  // Draw a line
  glClearColor(0.0, 0.0, 0.0, 0.0);
  glClear(GL_COLOR_BUFFER_BIT);

  glLineWidth(2);              // 设置线段宽度
  glBegin(GL_LINES);
  glColor3f(1.0, 0.0, 0.0);    // Red
  glVertex2f(0.0f, 0.0f);      // 定点坐标范围
  glVertex2f(0.5f, 0.8f);
  glEnd();

}

void drawCircle(double x, double y, double radius, int color) {
  // 用多点表示圆
  glClearColor(0.0, 0.0, 0.0, 0.0);
  const int n = 100;               // 点数
  // const double r = 60.0f;       // 半径
  glPointSize(1.0f);
  glBegin(GL_LINE_LOOP);
  if (color == 0) {
    glColor3f(0.0f, 1.0f, 0.0f);     // green
  } else if (color == 1) {
    glColor3f(1.0f, 0.0f, 0.0f);     // red
  } else if (color == 2) {
    glColor3f(1.0f, 1.0f, 0.0f);     // yellow
  }
  for (int i = 0; i < n; i++) {
    // glVertex2f(x/(SCALE * zoom) + radius/(SCALE * zoom) * cos(2*PI/n*i),
    //            y/(SCALE * zoom) + radius/(SCALE * zoom) * sin(2*PI/n*i));
    glVertex2f(x/(SCALE * zoom) + radius/(SCALE * zoom) * cos(2*PI/n*i),
               y/(SCALE * zoom) + radius/(SCALE * zoom) * sin(2*PI/n*i));
  }
  glEnd();
  glFlush();
}

int main_draw(Circle_tree ctre) {
  // 绘制主程序
  GLFWwindow* window;

  

  // Initialize the library
  if (!glfwInit())
    return -1;

  // Create a windowed mode window and its OpenGL context
  window = glfwCreateWindow(480, 480, "spaceOrder", NULL, NULL);

  // 注册滚轮回调函数
  glfwSetScrollCallback(window, scroll_callback);

  // 隐藏鼠标
  // glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

  if (!window) {
    glfwTerminate();
    return -1;
  }

  // Make the window's context current
  glfwMakeContextCurrent(window);


  
  // Loop until the user closes the window
  while (!glfwWindowShouldClose(window)) {
    // 当用户按下esc键, 我们设置window窗口的windowShouldCloseni属性为True
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
      glfwSetWindowShouldClose(window, true);
    // your draw
    // drawPoint();
    // drawLine();
    // drawTriangle();
    // 清空颜色
    glClear(GL_COLOR_BUFFER_BIT);
    for (int i = 0; i < ctre.n; i++) {
      // 每个clst一种颜色, 先设定只有两个clst
      // ctre.clsts_arr[i].drawCircles();
      int color = 1;
      ctre.clsts_arr[0].drawCircles(color);
      color = 2;
      ctre.clsts_arr[1].drawCircles(color);
    }

    // Swap front and back buffers
    glfwSwapBuffers(window);

    // Poll for and process events
    glfwPollEvents();
  }

  glfwTerminate();
  return 0;
}

